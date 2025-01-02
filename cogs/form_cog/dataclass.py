from dataclasses import dataclass
from typing import Callable
import discord
import re

@dataclass
class Question:
    question: str
    description: str
    validation: Callable[[str], bool]


class ClassCheck:
    def __init__():
        pass

    def text_to_func(txt):
        try:
            return {
            "text": ClassCheck.text,
            "image": ClassCheck.image,
            "position": ClassCheck.position
            }.get(txt)
        except:
            return ClassCheck.except_func
    
    def except_func(message: discord.Message):
        return True

    def text(message: discord.Message) -> bool:
        # 假設文本檢查始終返回 True
        value = message.content.strip()
        return value
    
    def image(message: discord.Message) -> bool:
        # 假設圖片檢查始終返回 True
        if len(message.attachments) == 1:
            attachment = message.attachments[0]
            if attachment.content_type.startswith('image/'):
                return attachment.url
        return False
    
    def position(message: discord.Message) -> bool:
        value = message.content.strip()
        # 檢查格式是否為三組數字，數字之間以空白間隔
        pattern = r'^-?\d+\s+-?\d+\s+-?\d+$'
        if re.match(pattern, value):
            # 分割數字並轉換為整數
            x, y, z = map(int, value.split())
            
            # 檢查每個數字是否在指定範圍內
            if not (-10000 <= x <= 10000):  # x 的範圍檢查
                return False
            if not (-64 <= y <= 350):  # y 的範圍檢查
                return False
            if not (-10000 <= z <= 10000):  # z 的範圍檢查
                return False
            return value
        return False
    