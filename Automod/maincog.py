import discord
from redbot.core import Config, commands, checks


class Automod(commands.Cog):
    """Automoderation commands"""
    def __init__(self):
        self.watching = list()
        self.blacklisted_words = list()

    @commands.command(name='watch')
    @commands.admin()
    async def watch(self, ctx, channel: discord.TextChannel):
        self.watching.append(channel)
        await ctx.send(f'Watching {channel.name}')

    @commands.command(name='unwatch')
    @commands.admin()
    async def unwatch(self, ctx, channel: discord.TextChannel):
        while channel in self.watching:
            self.watching.remove(channel)
        await ctx.send(f'Stopped watching {channel.name}')
    
    @commands.command(name='block')
    @commands.admin()
    async def block(self, ctx, word: str):
        self.blacklisted_words.append(word)
        await ctx.send(f'Blocked `{word}`')

    @commands.command(name='unblock')
    @commands.admin()
    async def unblock(self, ctx, word: str):
        while word in self.blacklisted_words:
            self.blacklisted_words.remove(word)
        await ctx.send(f'Unblocked `{word}`')
    
    @commands.command(name='listblocked')
    async def listblocked(self, ctx):
        await ctx.send(f'```{str(self.blacklisted_words)}```')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel in self.watching:
            return
        if message.author.bot:
            return

        for word in self.blacklisted_words:
            if word.lower() in message.content.lower():
                await message.delete()
