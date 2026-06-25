import discord
from discord import app_commands
from discord.ext import commands

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"  # <--- PASTE YOUR ACTUAL TOKEN HERE

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ PARADOX Bot online as {bot.user}')

@bot.tree.command(name='ping', description='Check if bot is alive')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('🏓 Pong!')

bot.run(MTUxOTcwNzk5ODI2MjM5NTEwMw.Gh7sw9.q0uSgaUR-e87pmeUIVY756T2UCc54dgAdrTiWI)
