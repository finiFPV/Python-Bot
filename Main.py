from discord import app_commands, Intents, Client, utils, Embed
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
    if perms.administrator == True or allowed == True or Data().owner(interaction) == True:
        await interaction.response.send_message(embed = Embed(title = "🗑️ Deleting...", description = f"Deleting: `{ammount}` message(s).", color = 0xff0000), ephemeral = True)
        await sleep(3)
        await interaction.channel.purge(limit = ammount + 1)
        await interaction.edit_original_response(embed = Embed(title = "✅🗑️ Successful!", description = f"Successfully deleted `{ammount}` message(s).", color = 0x00ff2a))
    else:
        await interaction.response.send_message(embed = Embed(title = "❌🗑️ Failed!", description = "You don't have: `manage_messages` and/or `read_message_history` permissions", color = 0xff0000))


client.run(Data().botToken)