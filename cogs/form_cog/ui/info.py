import discord
from utility import SheetDataNotFoundError, config
from ..embed_message import EmbedMessage
from google_sheets import Sheets
from datetime import datetime  # 用於處理時間

async def send_message(message: discord.Message):
    try:
        try:
            sheets = Sheets()
            embedMessage = EmbedMessage("刪除", icon_url=config.questionnaire_icon_url)
            form_id=message.content.split()[1]
            result: dict | None = sheets.get_form_details(form_id)

            
        except SheetDataNotFoundError:
            await message.channel.send(embed=embedMessage._error_embed(message="錯誤"))

        if result:
            # 建立嵌入消息
            embed = discord.Embed(
                title=f"表單詳情 - {form_id}",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.add_field(name="申請表名稱", value=result.get("申請表名稱", "無"), inline=False)
            embed.add_field(name="申請時間", value=result.get("申請時間", "無"), inline=False)
            embed.add_field(name="審核完成", value=result.get("審核完成", "無"), inline=True)
            embed.add_field(name="審核結果", value=result.get("審核結果", "無"), inline=True)
            embed.add_field(name="Discord 名稱", value=result.get("Discord 名稱", "無"), inline=False)

            # 添加問題及回答
            for key, value in result.items():
                if key not in ["申請表名稱", "申請表ID", "申請時間", "審核完成", "審核結果", "Discord 名稱", "Discord ID"]:
                    embed.add_field(name=f"問題: {key}", value=f"回答: {value or '無'}", inline=False)
            await message.channel.send(embed=embed)
            
        else:
            await message.channel.send(embed=embedMessage._error_embed(message=f"無法找到表單 ID 為 {form_id} 的記錄。"))
            



    except Exception as e:
        print(e)


