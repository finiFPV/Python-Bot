from discord import app_commands
from time import monotonic
from asyncio import sleep
import discord

botToken='***REMOVED***'
intents = discord.Intents.default()
obj = discord.Object(id = ***REMOVED***)
class MyClient(discord.Client):
    async def on_ready(self):
        await commands.sync(guild = obj)
        print(f'Logged on as {self.user}!')
client = MyClient(intents=intents)
commands = app_commands.CommandTree(client)


#Commands
@commands.command(name = "ping", description = "Replies with pong(bot's ping).", guild = obj)
async def ping(interaction):
    before = monotonic()
    await interaction.response.send_message(content = 'Pong!')
    ping = int((monotonic() - before) * 1000)
    embed = discord.Embed(title = "Pong!🏓", description = f"Bot's ping: `{ping}ms`", color = 0xff0000)
    await interaction.edit_original_response(content = None, embed = embed)

@commands.command(name = "clear", description = "Deletes set amount of messages from current channel.", guild = obj)
async def clear(interaction, ammount: int):
    perms = interaction.permissions
    allowed = perms.manage_messages == True and perms.read_message_history == True
    if perms.administrator == True or allowed == True:
        await interaction.response.send_message(embed = discord.Embed(title = "🗑️Deleting...", description = f"Deleting: `{ammount}` message(s).", color = 0xff0000))
        await sleep(3)
        await interaction.channel.purge(limit = ammount + 1)
        message = await interaction.followup.send(embed = discord.Embed(title = "✅🗑️Successful!", description = f"Successfully deleted `{ammount}` message(s).", color = 0x00ff2a))
        await sleep(7)
        await message.delete()
    else:
        await interaction.response.send_message(content = "You don't have `administrator` or `manage_messages` permission to use this command!")


client.run(botToken)