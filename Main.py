from discord import app_commands, Intents, Client, utils, Embed, VoiceChannel
from time import monotonic
from asyncio import sleep
from data import Data

intents = Intents.default()
class MyClient(Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await commands.sync()
        print(f'Commands synced!')
client = MyClient(intents=intents)
commands = app_commands.CommandTree(client)
channels = []


#Events
@client.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and after.channel.name == Data().rep_channel:
        category = utils.get(member.guild.categories, name = Data().rep_category)
        if category is None: category = await member.guild.create_category(Data().rep_category)
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
@commands.command(name = "ping", description = "Replies with pong(bot's ping).")
async def ping(interaction):
    before = monotonic()
    await interaction.response.send_message(content = 'Pong!', ephemeral = True)
    ping = int((monotonic() - before) * 1000)
    embed = Embed(title = "Pong! 🏓", description = f"Bot's ping: `{ping}ms`", color = 0xff0000)
    await interaction.edit_original_response(content = None, embed = embed)

@commands.command(name = "clear", description = "Deletes set amount of messages from current channel.")
async def clear(interaction, ammount: int):
    perms = interaction.permissions
    allowed = perms.manage_messages == True and perms.read_message_history == True
    if Data().owner == interaction.user.id or perms.administrator == True or allowed == True:
        await interaction.response.send_message(embed = Embed(title = "🗑️ Deleting...", description = f"Deleting: `{ammount}` message(s).", color = 0xeeff00), ephemeral = True)
        await sleep(3)
        await interaction.channel.purge(limit = ammount + 1)
        await interaction.edit_original_response(embed = Embed(title = "✅🗑️ Successful!", description = f"Successfully deleted `{ammount}` message(s).", color = 0x00ff2a))
    else:
        await interaction.response.send_message(embed = Embed(title = "❌🗑️ Failed!", description = "You don't have: `manage_messages` and/or `read_message_history` permission(s)", color = 0xff0000), ephemeral = True)

@commands.command(name = "mass_move", description = "Moves everyone from all channels to current channel or specified channel")
async def mass_move(interaction, channel: VoiceChannel = None):
    perms = interaction.permissions
    if Data().owner == interaction.user.id or perms.administrator == True or perms.move_members == True:
        if channel is None: channel = interaction.user.voice.channel
        await interaction.response.send_message(embed = Embed(title = "⏬ Moving...", description = f"Moving all server's active members to `{channel.name}`", color = 0xeeff00), ephemeral = True)
        await sleep(3)
        for member in interaction.guild.members:
            if member.voice is not None:
                await member.move_to(channel)
        await interaction.edit_original_response(embed = Embed(title = "✅⏬ Successful!", description = f"Successfully moved all active server's members to `{channel.name}`", color = 0x00ff2a))
    else:
        await interaction.response.send_message(embed = Embed(title = "❌⏬ Failed!", description = "You don't have: `move_members` permission", color = 0xff0000), ephemeral = True)


client.run(Data().botToken)