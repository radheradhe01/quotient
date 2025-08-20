from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import Quotient

from discord.ext import tasks

import config
from core import Cog


class QuoTasks(Cog):
    def __init__(self, bot: Quotient):
        self.bot = bot

        self.insert_guilds.start()

    @tasks.loop(count=1)
    async def insert_guilds(self):
        query = "INSERT INTO guild_data (guild_id, prefix, embed_color, embed_footer, dashboard_access, private_channel, is_premium, premium_end_time, made_premium_by, booster) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) ON CONFLICT DO NOTHING"
        for guild in self.bot.guilds:
            await self.bot.db.execute(query, guild.id, config.PREFIX, config.COLOR, config.FOOTER, '{}', None, False, None, None, None)

    @insert_guilds.before_loop
    async def before_loops(self):
        await self.bot.wait_until_ready()
