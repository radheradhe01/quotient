from __future__ import annotations

import discord

from core import Context
from models import Scrim

from ._base import ScrimsButton, ScrimsView
from ._btns import Discard
from ._pages import *

__all__ = ("ScrimsToggle",)


class ScrimsToggle(ScrimsView):
    def __init__(self, ctx: Context, scrim: Scrim):
        self.ctx = ctx
        self.record = scrim

        super().__init__(ctx)

    @property
    async def initial_message(self):
        _e = discord.Embed(color=self.bot.color)
        _e.description = "**Start / Stop scrim registration of {}**".format(self.record)
        _e.set_author(name=f"Page - {' / '.join(await self.record.scrim_posi())}", icon_url=getattr(self.bot.user.avatar, "url", None))
        return _e

    async def refresh_view(self):
        await self._add_buttons()
        try:
            self.message = await self.message.edit(embed=await self.initial_message, view=self)
        except discord.HTTPException:
            await self.on_timeout()

    async def _add_buttons(self):
        self.clear_items()

        if await Scrim.filter(guild_id=self.ctx.guild.id).count() >= 2:
            self.add_item(Prev(self.ctx))
            self.add_item(SkipTo(self.ctx))
            self.add_item(Next(self.ctx))

        self.add_item(StartReg())
        self.add_item(StopReg())
        self.add_item(Discard(self.ctx, "Main Menu", 2))


class StartReg(ScrimsButton):
    def __init__(self):
        super().__init__(label="Start Reg", style=discord.ButtonStyle.green, row=2)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not self.view.record.closed_at and self.view.record.opened_at:
            return await self.view.ctx.error("Registration is already open. To restart, pls stop registration first.", 4)

        try:
            await self.view.record.start_registration()
        except Exception as e:
            return await self.view.ctx.error(e, 10)

        else:
            await self.view.ctx.success(f"Registration opened {self.view.record}.", 5)
            await self.view.record.refresh_from_db()


class StopReg(ScrimsButton):
    def __init__(self):
        super().__init__(label="Stop Reg", style=discord.ButtonStyle.red, row=2)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if not self.view.record.opened_at:
            return await self.view.ctx.error("Registration is already closed.", 5)

        try:
            await self.view.record.close_registration()
        except Exception as e:
            return await self.view.ctx.error(e, 10)

        else:
            await self.view.record.refresh_from_db()
            await self.view.ctx.success(f"Registration closed {self.view.record}.", 5)
