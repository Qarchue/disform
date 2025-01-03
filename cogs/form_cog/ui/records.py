from typing import List, Optional

import discord
from discord.ui import Select, View

from google_sheets import Sheets
# 使用字典來儲存用戶的問卷狀態
user_record = []

class AppNav(View):
    """
    用於控制菜單互動的實際 View 類別

    參數:
        pages (List[discord.Embed], optional): 要循環顯示的頁面列表。預設為 None。
        timeout (Optional[float], optional): 互動有效持續時間。預設為 None。
        ephemeral (Optional[bool], optional): 以短暫消息方式發送。預設為 False。
        allowed_user (Optional[discord.Member], optional): 允許進行互動的用戶。預設為 None。
    """

    index = 0  # 頁面索引

    def __init__(
        self,
        reviewed_embeds: List[discord.Embed] = None,
        unreviewed_embeds: List[discord.Embed] = None,
        timeout: Optional[float] = None,
    ):
        super().__init__(timeout=timeout)
        pages = reviewed_embeds+unreviewed_embeds
        self.pages = pages  # 頁面列表
        self.reviewed_embeds = reviewed_embeds
        self.unreviewed_embeds = unreviewed_embeds
        self.filtered_pages = reviewed_embeds
        self.page_count = len(self.filtered_pages)
        self.show_reviewed = False

        if pages and len(self.pages) == 1:  # 如果只有一頁，移除「上一頁」、「下一頁」和「選擇」按鈕
            self.remove_item(self.previous)
            self.remove_item(self.next)
            self.remove_item(self.select)

        if pages and len(pages) > 1:  # 如果有多頁，為每一頁添加選擇項
            for index, page in enumerate(pages):
                self.select.add_option(
                    label=f"{page.title}",
                    description=f"{page.description[:96]}...".replace("`", ""),
                    value=index,
                )

                
    @discord.ui.button(
        label="上一頁",
        style=discord.ButtonStyle.success,
        row=1,
        custom_id="pretty_help:previous",
    )
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        self.index -= 1  # 頁面索引減一
        await self.update(interaction)  # 更新頁面

    @discord.ui.button(
        label="下一頁",
        style=discord.ButtonStyle.primary,
        row=1,
        custom_id="pretty_help:next",
    )
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        self.index += 1  # 頁面索引加一
        await self.update(interaction)  # 更新頁面

    @discord.ui.button(
        label="切換顯示已審核和未審核",
        style=discord.ButtonStyle.secondary,
        row=1,
        custom_id="pretty_help:toggle_reviewed",
    )
    async def toggle_reviewed(self, interaction: discord.Interaction, button: discord.Button):
        self.show_reviewed = not self.show_reviewed
        self.index = 0
        await self.update(interaction)

    @discord.ui.button(
        label="刪除",
        style=discord.ButtonStyle.danger,
        row=1,
        custom_id="pretty_help:delete",
    )
    async def _delete(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.message.delete()  # 刪除消息
        user_record.remove(interaction.user.id)


    @discord.ui.select(row=2, custom_id="pretty_help:select")
    async def select(self, interaction: discord.Interaction, select: Select):
        self.index = int(select.values[0])  # 設置頁面索引為選擇的值
        if self.pages[self.index].color == discord.Color.green():
            self. show_reviewed = False
            self.index = int(select.values[0])  # 設置頁面索引為選擇的值
        elif self.pages[self.index].color == discord.Color.yellow():
            self. show_reviewed = True
            self.index = int(select.values[0])-len(self.reviewed_embeds)  # 設置頁面索引為選擇的值
        await self.update(interaction)  # 更新頁面

    async def update(self, interaction: discord.Interaction):
        if self.show_reviewed:
            self.filtered_pages = self.unreviewed_embeds
            self.page_count = len(self.filtered_pages)
        else:
            self.filtered_pages = self.reviewed_embeds
            self.page_count = len(self.filtered_pages)

        if self.page_count > 0:
            await interaction.response.edit_message(
                embed=self.filtered_pages[self.index % self.page_count], view=self
            )  # 編輯消息以顯示當前頁面
        else:
            await interaction.response.send_message("沒有關聯的頁面可以顯示", ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True  # 如果沒有設置允許互動的用戶且是刪除操作，允許互動


class AppMenu():
    def __init__(
        self,
        timeout: Optional[float] = None,
    ) -> None:
        self.timeout = timeout

    async def send_pages(
        self,
        message: discord.Message,
        reviewed_embeds: List[discord.Embed],
        unreviewed_embeds: List[discord.Embed],
    ):

        await message.channel.send(
            embed=reviewed_embeds[0],
            view=AppNav(
                reviewed_embeds=reviewed_embeds,
                unreviewed_embeds=unreviewed_embeds,
                timeout=self.timeout,
            ),
        )




# 分頁顯示申請表
async def send_form_pages(message: discord.Message):
    """
    分頁顯示申請表，每 10 個為一頁。

    參數:
        interaction (discord.Interaction): Discord 的互動對象。
    """
    if message.author.id in user_record:
        return
    
    user_record.append(message.author.id)
    sheets = Sheets()
    form_list = sheets.query_from_user(user=message.author)
    reviewed_embeds = []
    unreviewed_embeds = []
    reviewed_list = []
    unreviewed_list = []

    for form in form_list:
        if form['審核完成'] == "TRUE":
            reviewed_list.append(form)
        else:
            unreviewed_list.append(form)

    for i in range(0, len(reviewed_list), 10):
        reviewed_embed = discord.Embed(
            title="申請表列表 (已審核)",
            description=f"顯示第 {i + 1} - {min(i + 10, len(reviewed_list))} 筆",
            color=discord.Color.green(),
        )
        # 添加每個申請表的信息到嵌入消息
        for j, form in enumerate(reviewed_list[i:i + 10], start=i + 1):
            form_name = form['申請表名稱']
            form_id = form['申請表ID']
            review_result = form['審核結果']
            review_status = f"審核結果: {review_result}"
            field_value = f"申請表ID: {form_id}\n{review_status}"

            reviewed_embed.add_field(
                name=f"🌟 {j}. {form_name}",
                value=field_value,
                inline=False
            )
        reviewed_embeds.append(reviewed_embed)


    for i in range(0, len(unreviewed_list), 10):
        unreviewed_embed = discord.Embed(
            title="申請表列表 (未審核)",
            description=f"顯示第 {i + 1} - {min(i + 10, len(unreviewed_list))} 筆",
            color=discord.Color.yellow(),
        )
        
        # 添加每個申請表的信息到嵌入消息
        for j, form in enumerate(unreviewed_list[i:i + 10], start=i + 1):
            form_name = form['申請表名稱']
            form_id = form['申請表ID']
            review_result = form['審核結果']
            review_status = "尚未審核"
            field_value = f"申請表ID: {form_id}\n{review_status}"
            

            unreviewed_embed.add_field(
                name=f"❌ {j}. {form_name}",
                value=field_value,
                inline=False
            )
        unreviewed_embeds.append(unreviewed_embed)

    if len(reviewed_embeds) == 0:
        reviewed_embeds.append(discord.Embed(
            title="申請表列表 (已審核)",
            description="這裡空空如也",
            color=discord.Color.green(),
        ))
    
    if len(unreviewed_embeds) == 0:
        unreviewed_embeds.append(discord.Embed(
            title="申請表列表 (未審核)",
            description="這裡空空如也",
            color=discord.Color.yellow(),
        ))

    # 使用類似於 AppMenu 的功能來分頁顯示
    app_menu = AppMenu(timeout=60.0)
    await app_menu.send_pages(message, reviewed_embeds, unreviewed_embeds)
    




# 分頁顯示申請表
async def send_form_pages_old(message: discord.Message):
    """
    分頁顯示申請表，每 10 個為一頁。

    參數:
        interaction (discord.Interaction): Discord 的互動對象。
    """
    sheets = Sheets()
    form_list = sheets.query_from_user(user=message.author)
    reviewed_embeds = []
    unreviewed_embeds = []
    for i in range(0, len(form_list), 10):
        reviewed_embed = discord.Embed(
            title="申請表列表 (已審核)",
            description=f"顯示第 {i + 1} - {min(i + 10, len(form_list))} 筆",
            color=discord.Color.green(),
        )

        unreviewed_embed = discord.Embed(
            title="申請表列表 (未審核)",
            description=f"顯示第 {i + 1} - {min(i + 10, len(form_list))} 筆",
            color=discord.Color.yellow(),
        )
        
        # 添加每個申請表的信息到嵌入消息
        for j, form in enumerate(form_list[i:i + 10], start=i + 1):
            form_name = form['申請表名稱']
            form_id = form['申請表ID']
            review_result = form['審核結果']
            if form['審核完成'] == "TRUE":
                if review_result:
                    review_status = f"審核結果: {review_result}"
                else:
                    review_status = f"標記完成"
            else:
                review_status = "尚未審核"
            field_value = f"申請表ID: {form_id}\n{review_status}"
            
            if form['審核完成'] == "TRUE":
                reviewed_embed.add_field(
                    name=f"🌟 {j}. {form_name}",
                    value=field_value,
                    inline=False
                )
            else:
                unreviewed_embed.add_field(
                    name=f"❌ {j}. {form_name}",
                    value=field_value,
                    inline=False
                )

        reviewed_embeds.append(reviewed_embed)
        unreviewed_embeds.append(unreviewed_embed)


    if len(reviewed_embeds) == 0:
        reviewed_embeds.append(discord.Embed(
            title="申請表列表 (已審核)",
            description="這裡空空如也",
            color=discord.Color.green(),
        ))
    
    if len(unreviewed_embeds) == 0:
        unreviewed_embeds.append(discord.Embed(
            title="申請表列表 (未審核)",
            description="這裡空空如也",
            color=discord.Color.yellow(),
        ))
    # 使用類似於 AppMenu 的功能來分頁顯示
    app_menu = AppMenu(timeout=60.0)
    await app_menu.send_pages(message, reviewed_embeds + unreviewed_embeds)