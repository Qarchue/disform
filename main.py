import argparse
from pathlib import Path
import discord

import sentry_sdk
from discord.ext import commands

from utility import LOG, config


intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True  # Enable message content intent
argparser = argparse.ArgumentParser()


class DiscordFormBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            application_id=config.application_id,
            allowed_contexts=discord.app_commands.AppCommandContext(
                guild=True, dm_channel=True, private_channel=True
            ),
            allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=True),
        )


    async def setup_hook(self) -> None:
        # 載入 jishaku
        await self.load_extension("jishaku")

        # 從 cogs 資料夾載入所有 cog
        for filepath in Path("./cogs").glob("**/*cog.py"):

            parts = list(filepath.parts)
            parts[-1] = filepath.stem
            await self.load_extension(".".join(parts))

        # 同步 Slash commands
        if config.main_server_id is not None:
            test_guild = discord.Object(id=config.main_server_id)
            self.tree.copy_global_to(guild=test_guild)
            await self.tree.sync(guild=test_guild)
        await self.tree.sync()


    async def on_ready(self):
        LOG.System(f"on_ready: You have logged in as {self.user}")
        LOG.System(f"on_ready: Total {len(self.guilds)} servers connected")

        LOG.System(f"{config.reload_form()}")

    async def close(self) -> None:
        await super().close()
        LOG.System("on_close: 機器人已結束")


    async def on_command(self, ctx: commands.Context):
        LOG.CmdResult(ctx)


    async def on_command_error(self, ctx: commands.Context, error):
        LOG.ErrorLog(ctx, error)


client = DiscordFormBot()


@client.tree.error
async def on_error(
    interaction: discord.Interaction, error: discord.app_commands.AppCommandError
) -> None:
    LOG.ErrorLog(interaction, error)
    sentry_sdk.capture_exception(error)


client.run(config.bot_token)
