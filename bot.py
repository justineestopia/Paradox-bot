import discord
from discord.ext import commands

TOKEN = "MTUxOTcwNzk5ODI2MjM5NTEwMw.GAWSTA.qyI8DpjPpUPjgL_BmVXoTbaq_jAVN-3BsFDO-k"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run(TOKEN)
