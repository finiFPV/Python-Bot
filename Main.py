from discord import app_commands
from time import monotonic
import asyncio
import discord

botToken='MTA0NjE3ODQ5MzAzNTE4NDIzMQ.Gc2Me2.I43BKpOGqk5T7GWd0wanNDp_iBaxrO6m230eb4'
obj = None #discord.Object(id = 1011395727546662962)
rep_channel = '➕ Create private channel'
rep_category = 'Private Channels'
def owner(interaction): return interaction.user.id == 973604858764591145

intents = discord.Intents.default()
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await commands.sync(guild = obj)
        print(f'Commands synced!')
client = MyClient(intents=intents)
commands = app_commands.CommandTree(client)
channels = []


#Events
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and after.channel.name == rep_channel:
        category = discord.utils.get(member.guild.categories, name = rep_category)
        if category is None: category = await member.guild.create_category(rep_category)
        if member.nick is None: name = member.name
        else: name = member.nick
        channel = await after.channel.clone(name = f"{name}'s channel")
        await channel.move(beginning = True, category = category)
        await channel.set_permissions(member, manage_channels = True, manage_roles = True)
        channels.append(channel.name)
        await member.move_to(channel)
    if before.channel is not None and before.channel.name in channels and before.channel.members == []:
        await before.channel.delete()
        if before.channel.category.channels == []: await before.channel.category.delete()


#Commands
@commands.command(name = "ping", description = "Replies with pong(bot's ping).", guild = obj)
async def ping(interaction):
    before = monotonic()
    await interaction.response.send_message(content = 'Pong!', ephemeral = True)
    ping = int((monotonic() - before) * 1000)
    embed = discord.Embed(title = "Pong! 🏓", description = f"Bot's ping: `{ping}ms`", color = 0xff0000)
    await interaction.edit_original_response(content = None, embed = embed)

@commands.command(name = "clear", description = "Deletes set amount of messages from current channel.", guild = obj)
async def clear(interaction, ammount: int):
    perms = interaction.permissions
    allowed = perms.manage_messages == True and perms.read_message_history == True
    if perms.administrator == True or allowed == True or owner(interaction) == True:
        await interaction.response.send_message(embed = discord.Embed(title = "🗑️ Deleting...", description = f"Deleting: `{ammount}` message(s).", color = 0xff0000), ephemeral = True)
        await asyncio.sleep(3)
        await interaction.channel.purge(limit = ammount + 1)
        await interaction.edit_original_response(embed = discord.Embed(title = "✅🗑️ Successful!", description = f"Successfully deleted `{ammount}` message(s).", color = 0x00ff2a))
    else:
        await interaction.response.send_message(embed = discord.Embed(title = "❌🗑️ Failed!", description = "You don't have: `manage_messages` and/or `read_message_history` permissions", color = 0xff0000))


client.run(botToken)