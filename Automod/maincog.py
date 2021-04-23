import discord
from redbot.core import Config, commands, checks


class Automod(commands.Cog):
    """Automoderation commands"""
    def __init__(self):
        self.watching = list()
        self.blacklisted_words = list()
        
    @commands.group(name='automod')
    async def automod(self, ctx):
        pass

    @automod.command(name='watch')
    @commands.admin()
    async def watch(self, ctx, channel: discord.TextChannel):
        await self.watching.append(channel)
        await ctx.send(f'Watching {channel.name}')

    @automod.command(name='unwatch')
    @commands.admin()
    async def unwatch(self, ctx, channel: discord.TextChannel):
        del self.watching[channel]
        await ctx.send(f'Stopped watching {channel.name}')
    
    @automod.command(name='block')
    @commands.admin()
    async def watch(self, ctx, word: str):
        await self.blacklisted_words.append(word)
        await ctx.send(f'Blocked `{word}`')

    @automod.command(name='unblock')
    @commands.admin()
    async def unwatch(self, ctx, word: str):
        del self.blacklisted_words[word]
        await ctx.send(f'Unblocked `{word}`')
    
    @automod.command(name='listblocked')
    async def listblocked(self, ctx):
        await ctx.send(f'```{str(self.blacklisted_words)}```')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel in self.watching:
            return

        for word in self.blacklisted_words:
            if message.content in word:
                await message.delete()
