import discord
from utility import SheetDataNotFoundError, config
from ..embed_message import EmbedMessage
from google_sheets import Sheets


async def send_message(message: discord.Message):
    try:
        try:
            sheets = Sheets()
            embedMessage = EmbedMessage("刪除", icon_url=config.questionnaire_icon_url)
            result = sheets.remove_from_id(form_id=message.content.split()[1])
            
        except SheetDataNotFoundError:
            await message.channel.send(embed=embedMessage._error_embed(message="刪除失敗，表單已被審核"))

        if result:
            await message.channel.send(embed=embedMessage._completion_delete_embed(form_id=message.content.split()[1]))

        else:
            await message.channel.send(embed=embedMessage._error_embed(message="刪除失敗，並未找到表單"))
            
    except Exception as e:
        print(e)