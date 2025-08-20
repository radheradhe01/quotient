from discord.ext import commands
import discord

class Basic(commands.Cog):
    """Basic commands for testing"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check if the bot is responsive"""
        await ctx.send(f"🏓 Pong! Latency: {round(self.bot.latency * 1000)}ms")
    
    @commands.command(name="info")
    async def info(self, ctx):
        """Get basic bot information"""
        embed = discord.Embed(
            title="🤖 Quotient Bot Info",
            description="A Discord bot for esports management",
            color=0x00FFB3
        )
        embed.add_field(name="Prefix", value=f"`{ctx.prefix}`", inline=True)
        embed.add_field(name="Commands", value=f"`{len(self.bot.commands)}`", inline=True)
        embed.add_field(name="Cogs", value=f"`{len(self.bot.cogs)}`", inline=True)
        embed.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`", inline=True)
        embed.add_field(name="Guilds", value=f"`{len(self.bot.guilds)}`", inline=True)
        embed.add_field(name="Users", value=f"`{len(self.bot.users)}`", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="test")
    async def test(self, ctx):
        """Basic test command"""
        await ctx.send("🧪 Basic test completed! The bot is working properly.")
        
    @commands.command(name="status")
    async def status(self, ctx):
        """Check bot status"""
        embed = discord.Embed(
            title="🤖 Quotient Bot Status",
            description="All systems operational!",
            color=0x00FFB3
        )
        embed.add_field(name="Commands", value=f"`{len(self.bot.commands)}`", inline=True)
        embed.add_field(name="Cogs", value=f"`{len(self.bot.cogs)}`", inline=True)
        embed.add_field(name="Latency", value=f"`{round(self.bot.latency * 1000)}ms`", inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Basic(bot))
