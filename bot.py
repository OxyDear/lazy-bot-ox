import discord
from discord.ext import commands
import os
import config

client = commands.Bot(command_prefix='.')
client.remove_command('help')


@client.command()
async def load(ctx, extension):
    if ctx.author.id == 764860374893461504:
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Cogs is loaded...')
    else:
        await ctx.send('You are not developer...')


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 764860374893461504:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send('Cogs is unloaded...')
    else:
        await ctx.send('You are not developer...')


@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 764860374893461504:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send('Cogs is loaded...')
    else:
        await ctx.send('You are not developer...')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(config.TOKEN)
