import asyncio
import discord
from discord.ext import commands
from google_sheets import Sheets
from utility import config

class Bot_EventCog(commands.Cog, name="機器人事件"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sheets = Sheets()
        
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member):
        """如果使用者被移除自伺服器"""
        if guild.id == config.main_server_id:
            self.sheets.remove_from_user(user=member)


async def setup(client: commands.Bot):
    await client.add_cog(Bot_EventCog(client))

