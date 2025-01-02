__all__ = ["Sheets"]

import gspread  # 用於與 Google Sheets API 互動
import uuid  # 用於生成唯一 ID
from google.oauth2.service_account import Credentials  # 用於 Google Sheets API 認證
from datetime import datetime  # 用於處理時間
import discord  # 用於處理 Discord 與使用者相關操作
from gspread_formatting import DataValidationRule, BooleanCondition, set_data_validation_for_cell_range  # 用於格式化 Google Sheets 單元格
from utility import LOG, config, SheetDataNotFoundError  # 自定義模組，用於記錄和配置

# 設置 Google Sheets API 憑證範圍
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(config.account_file, scopes=SCOPES)



class Sheets:
    def __init__(self):
        """
        初始化 Sheets 類別，用於與 Google Sheets API 互動。
        """
        self.client = gspread.authorize(creds)  # 授權 Google Sheets API
        self.spreadsheet = self.client.open_by_key(config.sheets_key)  # 打開指定的試算表
        # 設置布林類型的驗證規則，供新增行時使用
        self.validation_rule = DataValidationRule(
            BooleanCondition('BOOLEAN', []),
            showCustomUi=True
        )

    ### 工具方法 ###
    def check_worksheet(
            self, 
            form_name: str
    ) -> gspread.worksheet.Worksheet:
        
        """確認是否存在指定的工作表，若不存在則創建，
        Example: `check_worksheet(form_name)`

        Parameters
        ------
        form_name: `str`
            要選擇的工作表名稱，Ex: `經濟產出申請`

        Returns
        ------
        `gspread.worksheet.Worksheet` | `None`:
            根據參數獲得或創建指定的工作表，若無法檢查則回傳 `None`
        """
        try:
            try:
                # 嘗試打開工作表
                sheet = self.spreadsheet.worksheet(form_name)
            except gspread.exceptions.WorksheetNotFound:
                # 如果工作表不存在，創建新工作表
                sheet = self.spreadsheet.add_worksheet(title=form_name, rows=100, cols=20)
                # 回傳取得或創建的工作表
            return sheet
        except Exception as e:
            LOG.Error(f"無法檢查工作表: {e}")
            return None


    def check_headers(
            self, 
            sheet: gspread.worksheet.Worksheet, 
            headers: list
    ) -> None:
        """確認工作表的表頭是否正確，使用方式是先使用 `check_worksheet` 方法取得工作表實例後，再傳入本方法進行確認，
        Example: `check_headers(sheet, ["審核完成", "審核結果", "申請時間", "申請表ID", "Discord 名稱", "Discord ID"])`

        Parameters
        ------
        sheet: `gspread.worksheet.Worksheet`
            要選擇的工作表，Ex: `check_worksheet(form_name)`
        headers: `list`
            表頭，Ex: `["審核完成", "審核結果", "申請時間", "申請表ID", "Discord 名稱", "Discord ID"]`
        """
        if len(sheet.row_values(1)) < len(headers):
            sheet.update("A1", [headers])  # 更新表頭



    ### 表單相關操作 ###

    def submit_form(self, form_name: str, user: discord.Member, answers: dict) -> str:
        """提交表單資料到 Google Sheets，如果找不到工作表則自動創建

        Parameters
        ------
        form_name: `str`
            要選擇的工作表名稱，Ex: `經濟產出申請`
        user: `discord.Member`
            回答的使用者，Ex: `user`
        answers: `dict`
            回答資料，以字典表示，Ex: `{"q1": "r1", "q2": "r2"}`

        Returns
        ------
        `str`:
            回傳提交之後的表單ID
        """

        # 取得工作表
        sheet = self.check_worksheet(form_name)

        # 定義表頭
        headers = ["審核完成", "審核結果", "申請時間", "申請表ID", "Discord 名稱", "Discord ID"]
        headers.extend(answers.keys())  # 添加問題欄位到表頭

        self.check_headers(sheet, headers)  # 確認表頭是否正確

        # 生成唯一的申請表 ID
        form_id = str(uuid.uuid4())

        # 構建表單數據
        form_data = [
            False,  # 審核完成（未審核）
            "",  # 審核結果（空）
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 申請時間
            form_id,  # 表單 ID
            user.name,  # Discord 名稱
            str(user.id),  # Discord ID
        ]
        form_data.extend(answers.values())  # 添加回答內容


        new_row_index = len(sheet.get_all_values())  # 第幾行，下面程式會把該行的第一個欄位設成勾選框
        sheet.append_row(form_data)  # 新增數據

        # 設置勾選框格式到 "審核完成" 欄位
        set_data_validation_for_cell_range(
            sheet, f'A{new_row_index + 1}:A{new_row_index + 1}', self.validation_rule
        )
        return form_id


    def query_from_user(self, user: discord.Member) -> list[dict]:
        """以使用者查詢曾經上傳過的表單

        Parameters
        ------
        user: `discord.Member`
            要查詢的使用者

        Returns
        ------
        `list[dict]`:
            根據使用者選則出發送過的所有申請
        """
        try:
            
            user_forms = []
            worksheets = self.spreadsheet.worksheets()

            # 遍歷所有工作表查找與用戶相關的表單
            for sheet in worksheets:
                all_records = sheet.get_all_records()
                for record in all_records:
                    if record.get("Discord ID") == user.id:
                        
                        user_forms.append({
                            "申請表名稱": sheet.title,
                            "審核完成": record.get("審核完成", ""),
                            "審核結果": record.get("審核結果", ""),
                            "申請表ID": record.get("申請表ID", ""),
                        })
            
            return user_forms
        
        except Exception as e:
            LOG.Error(f"查詢失敗: {e}")
            return []

    def remove_from_id(self, form_id: str) -> bool:
        """根據表單 ID 刪除表單，若表單正在被審核或已審核則無法刪除

        Parameters
        ------
        form_id: `str`
            要查詢的表單ID，Ex: `35ad90b0-3cad-42bf-bf55-6e5e61260fb4`

        Returns
        ------
        `bool`:
            是否刪除成功
        """
        try:
            worksheets = self.spreadsheet.worksheets()
            # 建立錯誤訊息變數，提前準備返回值
            error_message = None

            for sheet in worksheets:
                # 只取得需要的欄位資料以減少傳輸量
                all_records = sheet.get_all_records()
                for i, record in enumerate(all_records):
                    if record.get("申請表ID") == form_id:
                        # 提前檢查審核狀態
                        if record.get("審核完成") == "TRUE":
                            error_message = f"無法刪除表單 {form_id}：表單已被審核"
                            LOG.Debug(error_message)
                            raise SheetDataNotFoundError(error_message)

                        # 未審核則刪除
                        sheet.delete_rows(i + 2)  # 索引從 0 開始且第 1 行為表頭
                        LOG.Debug(f"成功刪除表單 {form_id} 在工作表 {sheet.title} 的第 {i + 2} 行")
                        return True

            LOG.Debug(f"表單 {form_id} 不存在於任何工作表")
            return False
        except Exception as e:
            LOG.Error(f"刪除失敗: {e}")
            return False
        

    def remove_from_user(self, user: discord.Member) -> bool:
        """根據使用者刪除表單，若表單已審核則無法刪除

        Parameters
        ------
        user: `discord.Member`
            要查詢的使用者

        Returns
        ------
        `bool`:
            是否刪除成功
        """
        try:
            worksheets = self.spreadsheet.worksheets()
            deleted_count = 0  # 記錄刪除表單的數量
            for sheet in worksheets:
                try:
                    all_records = sheet.get_all_records()  # 獲取工作表的所有記錄
                    rows_to_delete = []  # 用於記錄需要刪除的行

                    for i, record in enumerate(all_records):
                        if record.get("審核完成") != "TRUE" and record.get("Discord ID") == str(user.id):
                            rows_to_delete.append(i + 2)  # 儲存需要刪除的行索引 (+2 說明見下方)

                    # 刪除行（批量刪除以減少操作次數）
                    for row_index in reversed(rows_to_delete):  # 逆序刪除避免影響索引
                        sheet.delete_rows(row_index)
                        deleted_count += 1
                        LOG.Debug(f"已刪除 {sheet.title} 中第 {row_index} 行的表單")

                except Exception as sheet_error:
                    LOG.Error(f"處理工作表 {sheet.title} 時出現錯誤: {sheet_error}")

            if deleted_count > 0:
                LOG.Debug(f"已成功刪除使用者 {user.id} 的 {deleted_count} 個未審核申請表")
            else:
                LOG.Debug(f"未找到使用者 {user.id} 的未審核申請表")
            return True

        except Exception as e:
            LOG.Error(f"刪除過程中發生錯誤: {e}")
            return False



    def get_form_details(self, form_id: str) -> dict | None:
        """根據表單 ID 獲取表單的詳細資料

        Parameters
        ------
        form_id: `str`
            要查詢的表單ID，Ex: `35ad90b0-3cad-42bf-bf55-6e5e61260fb4`

        Returns
        ------
        `dict` | `None`:
            根據表單 ID 以字典形式回傳該表單的詳細資料
        """
        try:
            worksheets = self.spreadsheet.worksheets()

            # 遍歷所有工作表查找符合的表單 ID
            for sheet in worksheets:
                all_records = sheet.get_all_records()

                # 查找匹配的記錄
                for record in all_records:
                    if record.get("申請表ID") == form_id:
                        record.update({"申請表名稱": sheet.title})
                        return record

            return None

        except Exception as e:
            raise SheetDataNotFoundError(f"無法找到表單 ID 為 {form_id} 的記錄。")
            

    def get_form_details_as_embed(self, form_id: str) -> discord.Embed:
        """根據表單 ID 獲取表單的詳細資料，並將資料包裝成embed回傳

        Parameters
        ------
        form_id: `str`
            要查詢的表單ID，Ex: `35ad90b0-3cad-42bf-bf55-6e5e61260fb4`

        Returns
        ------
        `discord.Embed``:
            根據表單 ID 以embed回傳詳細資料
        """
        try:
            worksheets = self.spreadsheet.worksheets()

            # 遍歷所有工作表查找符合的表單 ID
            for sheet in worksheets:
                all_records = sheet.get_all_records()

                # 查找匹配的記錄
                for record in all_records:
                    if record.get("申請表ID") == form_id:
                        # 建立嵌入消息
                        embed = discord.Embed(
                            title=f"表單詳情 - {form_id}",
                            color=discord.Color.blue(),
                            timestamp=datetime.now()
                        )
                        embed.add_field(name="申請表名稱", value=sheet.title, inline=False)
                        embed.add_field(name="申請時間", value=record.get("申請時間", "無"), inline=False)
                        embed.add_field(name="審核完成", value=record.get("審核完成", "無"), inline=True)
                        embed.add_field(name="審核結果", value=record.get("審核結果", "無"), inline=True)
                        embed.add_field(name="Discord 名稱", value=record.get("Discord 名稱", "無"), inline=False)

                        # 添加問題及回答
                        for key, value in record.items():
                            if key not in ["申請表ID", "申請時間", "審核完成", "審核結果", "Discord 名稱", "Discord ID"]:
                                embed.add_field(name=f"問題: {key}", value=f"回答: {value or '無'}", inline=False)

                        return embed

            # 如果找不到表單，返回錯誤嵌入
            return discord.Embed(
                title="表單未找到",
                description=f"無法找到表單 ID 為 {form_id} 的記錄。",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )

        except Exception as e:
            # 異常處理：返回錯誤嵌入
            return discord.Embed(
                title="發生錯誤",
                description=f"無法檢索表單詳情：{e}",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )


### 範例工作流程 ###
'''
>審核時的流程<
1. 前往該案地點，確認能正常審核（無座標填錯、範圍不明、申請人不符合資格等）。
2. 詳細檢查建築，粗略估算產值。
3. 比對過往審核案例，確保產值排名合理。
4. 若合理，結案；若不合理，調整產值。
'''