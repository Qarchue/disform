import discord
import discord.context_managers
from datetime import datetime
from utility import config
from .dataclass import Question
from typing import List

class EmbedMessage:

    def __init__(self, name: str, icon_url: str | None):
        self.name = name
        self.icon_url = icon_url


    def _create_question_embed(self, question: Question):
        """
        將問題的值打包成embed
        """
        embed = discord.Embed(title=question.question,
                      colour=0x00b0f4,
                      timestamp=datetime.now())

        embed.add_field(name="",
                        value=f"{question.description}",
                        inline=False)
        
        embed.add_field(name="",
                        value="",
                        inline=False)

        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)
        return embed


    def _timeout_embed(self):
        embed = discord.Embed(title="操作逾時",
                      colour=0xf4cf00,
                      timestamp=datetime.now())
        
        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)
        return embed


    def _error_embed(self, message: str = "輸入的格式或指令不正確"): 
        embed = discord.Embed(title=message,
                      colour=0xe30000,
                      timestamp=datetime.now())

        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)
        return embed
    

    def _wait_completion_embed(self):
        embed = discord.Embed(title="正在提交申請...",
                      colour=0x00f462,
                      timestamp=datetime.now())
        
        embed.add_field(name=f"正在提交申請，請稍等...",
                        value=f"",
                        inline=False)

        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)
        return embed
    

    def _completion_embed(self, form_id):
        embed = discord.Embed(title="已提交申請",
                      colour=0x00f462,
                      timestamp=datetime.now())
        
        embed.add_field(name=f"申請表ID: {form_id}",
                        value=f"",
                        inline=False)
        
        embed.add_field(name="",
                        value=f"提交申請後，請耐心等待管理員處裡您的申請事項，請勿多次申請",
                        inline=False)

        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)
        return embed
    

    def _incomplete_embed(self):
        embed = discord.Embed(title="錯誤嘗試過多",
                      colour=0xffdd00,
                      timestamp=datetime.now())

        embed.add_field(name="",
                        value=f"錯誤嘗試過多，已關閉問卷",
                        inline=False)

        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)

        return embed


    def _full_embed(self, questions: List[Question]):
        embed = discord.Embed(title="已填完所有內容",
                      colour=0x00f49f,
                      timestamp=datetime.now())

        embed.add_field(name="",
                        value=f"您已填完申請表，現在你可以使用:",
                        inline=False)
        embed.add_field(name=f"{config.custom_command_prefix}done",
                        value=f"確認提交申請",
                        inline=True)
        
        embed.add_field(name=f"{config.custom_command_prefix}back",
                        value=f"返回上一個項目填寫",
                        inline=True)
        
        embed.add_field(name=f"{config.custom_command_prefix}(數字)",
                        value=f"跳到指定項目重新填寫",
                        inline=True)    
        
        for i, questionq in enumerate(questions, start=1):
            embed.add_field(name="",
                            value=f"",
                            inline=True)            
            embed.add_field(name="",
                        value=f"",
                        inline=True)
            embed.add_field(name="",
                            value=f"> {i}. {questionq.question}",
                            inline=True)   


        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)
        return embed
    

    def _help_embed(self):
        embed = discord.Embed(title="指令列表",
                      colour=0x2d00f4,
                      timestamp=datetime.now())

        embed.add_field(name="-help",
                        value=f"出現現在這個視窗",
                        inline=False)

        embed.set_footer(text=self.name,
                        icon_url=self.icon_url)
        return embed


    def _completion_delete_embed(self, form_id):
        embed = discord.Embed(title="已刪除表格",
                      colour=0x00f462,
                      timestamp=datetime.now())
        
        embed.add_field(name=f"申請表ID: {form_id}",
                        value=f"",
                        inline=False)

        embed.set_footer(text="經濟產出申請",
                        icon_url=self.icon_url)
        return embed