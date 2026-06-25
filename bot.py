import discord
from discord.ext import commands

TOKEN = "MTUxOTcwNzk5ODI2MjM5NTEwMw.GH0TnY.arNHVGdmKheMQ_ZowQ3qDN7s_C3rq-1yWjobv8"

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
