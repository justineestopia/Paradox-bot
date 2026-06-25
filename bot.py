import discord
from discord import app_commands
from discord.ext import commands
import os
import time
import database as db

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

YOUR_DISCORD_ID = 1201013390827597975  # ✅ Your ID is already set

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'✅ PARADOX Bot online as {bot.user}')

@bot.tree.command(name='redeem', description='Redeem a premium key')
@app_commands.describe(key='Your 32-character key')
async def redeem(interaction: discord.Interaction, key: str):
    user = db.get_user(str(interaction.user.id))
    if user:
        return await interaction.response.send_message('❌ You already have premium.', ephemeral=True)
    key_data = db.get_user_by_key(key)
    if key_data:
        return await interaction.response.send_message('❌ Key already used.', ephemeral=True)
    db.create_user(str(interaction.user.id), key, 30)
    await interaction.response.send_message('✅ Premium activated!', ephemeral=True)

@bot.tree.command(name='getstats', description='View your premium stats')
async def getstats(interaction: discord.Interaction):
    user = db.get_user(str(interaction.user.id))
    if not user:
        return await interaction.response.send_message('❌ No premium found.', ephemeral=True)
    discord_id, key, hwid, expires, execs, resets, banned, note = user
    days = (expires - int(time.time())) // 86400
    embed = discord.Embed(title='📊 Your Stats', color=0x00ff00)
    embed.add_field(name='Executions', value=execs, inline=True)
    embed.add_field(name='HWID', value=hwid or 'Not set', inline=True)
    embed.add_field(name='Key', value=key, inline=False)
    embed.add_field(name='Resets', value=resets, inline=True)
    embed.add_field(name='Expires', value=f'{days} days' if days > 0 else 'EXPIRED', inline=True)
    embed.add_field(name='Banned', value='Yes' if banned else 'No', inline=True)
    embed.add_field(name='Note', value=note or '-', inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='getscript', description='Get your PARADOX script')
async def getscript(interaction: discord.Interaction):
    user = db.get_user(str(interaction.user.id))
    if not user:
        return await interaction.response.send_message('❌ You don\'t have premium.', ephemeral=True)
    discord_id, key, hwid, expires, execs, resets, banned, note = user
    if banned:
        return await interaction.response.send_message('❌ You are banned.', ephemeral=True)
    if expires < int(time.time()):
        return await interaction.response.send_message('❌ Your key has expired.', ephemeral=True)
    script_url = "https://paradox-bot.onrender.com/paradox.lua"
    pc_copy = f'''script_key="{key}";
loadstring(game:HttpGet("{script_url}"))()'''
    mobile_copy = f'''script_key="{key}";
loadstring(game:HttpGet("{script_url}"))()'''
    embed = discord.Embed(title="🔥 Here is your PARADOX script:", description="Copy the script below and paste it into your executor.", color=0x00ff00)
    embed.add_field(name="🖥️ PC Copy", value=f"```lua\n{pc_copy}\n```", inline=False)
    embed.add_field(name="📱 Mobile Copy", value=f"```lua\n{mobile_copy}\n```", inline=False)
    embed.set_footer(text="Only you can see this • Dismiss message")
    await interaction.response.send_message(embed=embed, ephemeral=True)
    db.add_execution(str(interaction.user.id))

@bot.tree.command(name='resethwid', description='Reset your HWID')
async def resethwid(interaction: discord.Interaction):
    user = db.get_user(str(interaction.user.id))
    if not user:
        return await interaction.response.send_message('❌ No premium.', ephemeral=True)
    db.reset_hwid(str(interaction.user.id))
    await interaction.response.send_message('✅ HWID reset.', ephemeral=True)

@bot.tree.command(name='getrole', description='Get Premium role')
async def getrole(interaction: discord.Interaction):
    user = db.get_user(str(interaction.user.id))
    if not user:
        return await interaction.response.send_message('❌ No premium.', ephemeral=True)
    role = discord.utils.get(interaction.guild.roles, name='Premium')
    if not role:
        return await interaction.response.send_message('❌ Role not found.', ephemeral=True)
    await interaction.user.add_roles(role)
    await interaction.response.send_message('✅ Role added!', ephemeral=True)

@bot.tree.command(name='admin_genkey', description='Generate a key (Admin)')
@app_commands.describe(expiry_days='Days until expiry')
async def genkey(interaction: discord.Interaction, expiry_days: int = 30):
    if interaction.user.id != YOUR_DISCORD_ID:
        return await interaction.response.send_message('❌ Admin only.', ephemeral=True)
    key = db.generate_key()
    db.create_user(f'key_{key}', key, expiry_days)
    await interaction.response.send_message(f'✅ `{key}` (expires in {expiry_days} days)', ephemeral=True)

@bot.tree.command(name='admin_ban', description='Ban a user (Admin)')
@app_commands.describe(discord_id='User ID to ban')
async def ban(interaction: discord.Interaction, discord_id: str):
    if interaction.user.id != YOUR_DISCORD_ID:
        return await interaction.response.send_message('❌ Admin only.', ephemeral=True)
    db.ban_user(discord_id)
    await interaction.response.send_message(f'✅ {discord_id} banned.', ephemeral=True)

@bot.tree.command(name='admin_unban', description='Unban a user (Admin)')
@app_commands.describe(discord_id='User ID to unban')
async def unban(interaction: discord.Interaction, discord_id: str):
    if interaction.user.id != YOUR_DISCORD_ID:
        return await interaction.response.send_message('❌ Admin only.', ephemeral=True)
    db.unban_user(discord_id)
    await interaction.response.send_message(f'✅ {discord_id} unbanned.', ephemeral=True)

@bot.tree.command(name='admin_stats', description='View all users (Admin)')
async def admin_stats(interaction: discord.Interaction):
    if interaction.user.id != YOUR_DISCORD_ID:
        return await interaction.response.send_message('❌ Admin only.', ephemeral=True)
    users = db.get_all_users()
    msg = '📊 **All Users**\n'
    for u in users:
        msg += f'<@{u[0]}> | Key: {u[1]} | HWID: {u[2] or "None"} | Banned: {u[6]}\n'
    await interaction.response.send_message(msg[:2000], ephemeral=True)

bot.run(os.getenv('BOT_TOKEN'))
