__all__ = ["Questionnaire", "user_questionnaire"]

import discord
import discord.context_managers
from discord.ext import commands
import asyncio


from utility import config
from google_sheets import Sheets
from typing import List


from ..dataclass import Question
from ..embed_message import EmbedMessage
# 使用字典來儲存用戶的問卷狀態
user_questionnaire = []



class Questionnaire(EmbedMessage):
    def __init__(self, bot: commands.Bot, user: discord.Member, name: str, icon_url: str, questions: List[Question]):
        super().__init__(name=name, icon_url=icon_url)
        if user.id in user_questionnaire: return
        user_questionnaire.append(user.id)
        self.bot = bot
        self.name: str = name
        self.questions: list = questions
        self.current_index: int = 0
        self.responses = [None] * len(questions)
        """紀錄問卷填寫的資料"""
        self.last_response_time = None
        self.error_count = 0
        self.executing = True

        self.user = user

        self.completion_message = None

        # asyncio.create_task(self.start())


    async def start(self, user: discord.User | None = None):
        """當開始時"""
        if user == None:
            user = self.user
        
        await self.send_question(user)
        """呼叫發送embed的函式"""

        while self.executing:
            if self.error_count >= 3:
                await user.send(embed=self._incomplete_embed())
                user_questionnaire.remove(user.id)
                raise KeyError

            try:
                response = await self.bot.wait_for(
                    'message',
                    check=lambda msg: (msg.author == user and isinstance(msg.channel, discord.DMChannel) and
                        (self.last_response_time is None or 
                        (discord.utils.utcnow() - self.last_response_time).total_seconds() >= 0.5)  # 設定限制時間
                    ),
                    timeout=config.questionnaire_timeout
                )

                self.last_response_time = discord.utils.utcnow()  # 更新最後回覆時間
                await self.handle_response(response)


            except asyncio.TimeoutError:
                """當超時"""
                await user.send(embed=self._timeout_embed())
                """向使用者發送超時消息"""
                user_questionnaire.remove(user.id)
                raise TimeoutError

       
        """向使用者發送已經填完消息"""
        result = {q.question: value for q, value in zip(self.questions, self.responses)}

        sheets = Sheets()

        try:
            form_id = sheets.submit_form(
                form_name=self.name,
                user=user,
                answers=result
            )
            await self.completion_message.edit(embed=self._completion_embed(form_id))

        except Exception as e:
            await user.send(embed=self._error_embed(f"發生錯誤，請稍後再試  error code:{e}"))
            
        user_questionnaire.remove(user.id)
        return


    async def handle_response(self, message: discord.Message):
        """當取得使用者訊息"""
        current_question: Question
        content = message.content.strip()

        if content.startswith('-') or self.current_index == len(self.responses):
            """第一個字元為-"""
            await self.handle_command(message, content)
            """呼叫指令方法"""

        else:
            current_question = self.questions[self.current_index]
            # 驗證輸入
            is_valid = current_question.validation(message)
            """會傳驗證後的資料是否正確 -> bool"""
            if is_valid:
                """如果正確"""
                self.responses[self.current_index] = is_valid
                """儲存至資料"""

                if None in self.responses:
                    """如果還沒填完"""
                    self._move_index()
                    """用方法來移動索引"""
                    await self.send_question(message.author)
                
                else:
                    self.current_index = len(self.responses)
                    """如果填完，就發送指示訊息"""
                    await message.channel.send(embed=self._full_embed(self.questions))
            
            else:
                """如果不正確"""
                await message.channel.send(embed=self._error_embed())
                self.error_count += 1



    async def handle_command(self, message: discord.Message, command: str):
        """當確認使用者訊息為指令而非資料"""


        if command == f'{config.custom_command_prefix}done':
            if not(None in self.responses):
                self.executing = False
                """直接讓while跳出，反正外面有寫一個執行完畢的消息"""
                self.completion_message = await message.channel.send(embed=self._wait_completion_embed())
            else:
                await message.channel.send(embed=self._incomplete_embed())
                """向使用者發送尚未填完問題的消息"""
                self.error_count += 1



        elif command == f'{config.custom_command_prefix}back':
            if self._set_index(self.current_index-1):
                await self.send_question(message.author)
                """發送目前所引的問題"""

            else:
                """在往後就碰壁啦!"""
                await message.channel.send(embed=self._error_embed("已經是第一個問題，無法再返回。"))
                self.error_count += 1



        elif command.startswith(config.custom_command_prefix) and command[1:].isdigit():
            """否則如果字串開頭為-，且-之後為數字"""
            index = int(command[1:]) - 1
            if self._set_index(index):
                """檢測跳至的問題是否正確"""
                await self.send_question(message.author)
                """發送目前所引的問題"""
            else:
                """不正確的話"""
                await message.channel.send(embed=self._error_embed("無效的問題編號。"))
                self.error_count += 1

        else:
            """如果都不是的話"""
            await message.channel.send(embed=self._error_embed("未知的指令。"))
            self.error_count += 1



    async def send_question(self, user: discord.User):
        """
        發送目前索引的問題
        它不管目前所引的數值是否正確，很霸道吧(?
        """
        question = self.questions[self.current_index]
        embed = self._create_question_embed(question)
        await user.send(embed=embed)





    def _move_index(self):
        """移動目前回答問題索引的函式"""
        # 從 current_index 位置開始尋找下一個 None
        for i in range(self.current_index, len(self.responses)):
            if self.responses[i] is None:
                self.current_index = i
                return

        # 如果後續沒有找到 None，則從頭開始尋找
        for i in range(len(self.responses)):
            if self.responses[i] is None:
                self.current_index = i
                return

        # 如果整個陣列中都不含 None，返回最後一個索引
        self.current_index = len(self.responses) - 1

    def _set_index(self, index):
        """指定目前回答問題索引的函式"""
        if 0 <= index < len(self.responses):
            self.current_index = index
            return True
        else: return False



    

