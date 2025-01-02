import asyncio
import discord
from discord.ext import commands

from utility import config, LOG
from google_sheets import Sheets


from .dataclass import Question, ClassCheck
from .embed_message import EmbedMessage
from .ui import Questionnaire, records, remove, info

# 使用字典來儲存用戶的問卷狀態
user_questionnaire = []


class FormCog(commands.Cog, EmbedMessage, name="問卷系統"):
    def __init__(self, bot: commands.Bot):
        super().__init__(name="問卷選單", icon_url=config.questionnaire_icon_url)
        self.bot = bot
        self.sheets = Sheets()


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user: return
        """如果傳送訊息的是機器人則跳過"""
        if isinstance(message.channel, discord.DMChannel):
            if message.author.id in user_questionnaire: return
            """如果傳送訊息的使用者正在填寫表單則跳過"""
            
            if message.content.startswith(config.custom_command_prefix):
                """如果訊息以設定的命令前綴開頭"""
                CPL = len(config.custom_command_prefix)
                """command_prefix_length"""
                CWCP = message.content[CPL:]
                """content_without_command_prefix"""
                form_data = config.form_datas.get(CWCP)
                if form_data is not None:
                    try:
                        user_questionnaire.append(message.author.id)
                        questions = []
                        
                        for question_data in form_data['questions']:
                            try:
                                questions.append(
                                    Question(
                                        question_data['question'],
                                        question_data['description'],
                                        ClassCheck.text_to_func(question_data['class_check'])
                                    )
                                )
                            except:
                                continue

                        if len(questions):
                            questionnaire = Questionnaire(
                                bot=self.bot,
                                user=message.author,
                                name=form_data['name'],
                                icon_url=config.questionnaire_icon_url,
                                questions=questions,
                            )
                            k = await questionnaire.start()
                        
                    except Exception as e:
                        print(e)
                        user_questionnaire.remove(message.author.id)
                    else:
                        user_questionnaire.remove(message.author.id)


                elif message.content == f"{config.custom_command_prefix}record":
                    await records.send_form_pages(message)


                elif message.content.startswith(f"{config.custom_command_prefix}remove") and len(message.content.split()) == 2:
                    await remove.send_message(message)


                elif message.content.startswith(f"{config.custom_command_prefix}info") and len(message.content.split()) == 2:
                    await info.send_message(message)


async def setup(client: commands.Bot):
    await client.add_cog(FormCog(client))