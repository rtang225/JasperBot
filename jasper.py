import os
import discord
import asyncio

from discord.ext import commands
from BotConfig import BotConfig

intents = discord.Intents.all()
activity = discord.Activity(type = discord.ActivityType.watching, name = 'Over My Fellow Ghosts')
client = commands.Bot(command_prefix = BotConfig.prefix(), help_command = None, intents = intents, activity = activity)

#Start Up Sequences, loading cogs...
async def main():
    async with client:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await client.load_extension(f'cogs.{filename[:-3]}')
                except:
                    print(f'Error with loading cog {filename}')
        await client.start(BotConfig.token())

#Shutdown
@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.message.delete()
    msg = await ctx.send (f'Shutting Down...')
    await asyncio.sleep(3)
    await msg.delete()
    await client.close()
    print(f'\n{client.user} has disconnected from Discord!')

#Quick Shutdown
@client.command()
@commands.is_owner()
async def hsd(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title = 'A Hard Shut Down has been performed', color = 0xFFCB00)
    await ctx.send(embed = embed)
    await client.close()
    print(f'\n{client.user} has disconnected from Discord!')

#Loading Cogs
@client.command()
@commands.is_owner()
async def load(ctx, extension):
    await client.load_extension(f'cogs.{extension}')
    await ctx.message.delete()
    await ctx.send(f'The {extension} cog is loaded!', delete_after = 5.0)

#Unloading Cogs
@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await ctx.message.delete()
    await ctx.send(f'The {extension} cog is unloaded!', delete_after = 5.0)

#Refreshing Cogs
@client.command(aliases=['reload'])
@commands.is_owner()
async def refresh(ctx, extension):
    await client.reload_extension(f'cogs.{extension}')
    await ctx.message.delete()
    await ctx.send(f'The {extension} cog is refreshed!', delete_after = 5.0)
    
asyncio.run(main())