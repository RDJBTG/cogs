import discord
from redbot.core import Config, commands, checks


class Automod(commands.Cog):
    """Automoderation commands"""
    def __init__(self):
        self.config = Config.get_conf(self, identifier=1234567890)

        watching = list()
        self.config.init_custom("ChannelsWatched", 1)
        self.config.register_custom("ChannelsWatched", **watching)
        
        blacklisted_words = list()
        self.config.init_custom("BlacklistedWords", 1)
        self.config.register_custom("BlacklistedWords", **blacklisted_words)
        
    @commands.group(name='automod')
    async def automod(self, ctx):
        pass

    @automod.command(name='watch')
    @commands.admin()
    async def watch(self, ctx, channel: discord.TextChannel):
        await self.config.custom("ChannelsWatched").watching().append(channel)
        await ctx.send(f'Watching {channel.name}')

    @automod.command(name='unwatch')
    @commands.admin()
    async def unwatch(self, ctx, channel: discord.TextChannel):
        watching = await self.config.custom("ChannelsWatched").watching()
        del watching[channel]
        await ctx.send(f'Stopped watching {channel.name}')
    
    @automod.command(name='block')
    @commands.admin()
    async def watch(self, ctx, word: str):
        await self.config.custom("BlacklistedWords").blacklisted_words.append(word)
        await ctx.send(f'Blocked `{word}`')

    @automod.command(name='unblock')
    @commands.admin()
    async def unwatch(self, ctx, word: str):
        blacklisted = await self.config.custom("BlacklistedWords").blacklisted_words()
        del blacklisted[word]
        await ctx.send(f'Unblocked `{word}`')
    
    @automod.command(name='listblocked')
    async def listblocked(self, ctx):
        blacklisted = await self.config.custom("BlacklistedWords").blacklisted_words()
        await ctx.send(f'```{str(blacklisted)}```')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        watching_channels = await self.config.custom("ChannelsWatched").watching()
        blacklisted_words = await self.config.custom("BlacklistedWords").blacklisted_words()
        if not message.channel in watching_channels:
            return

        for word in blacklisted_words:
            if message.content in word:
                await message.delete()
