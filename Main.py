from discord import app_commands, Intents, Client, VoiceChannel
from feathures import Audio, Admin, Info, Features
from typing import Literal
from data import Data


class MyClient(Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await commands.sync()
        print(f'Commands synced!')
client = MyClient(intents = Intents.default())
commands = app_commands.CommandTree(client)


#Events
@client.event
async def on_voice_state_update(member, before, after):
    await Features.private_channel(member, before, after)


#Commands
@commands.command(name = "ping", description = "Replies with pong(bot's ping).")
async def ping(interaction):
    await Info.ping(interaction)

@commands.command(name = "clear", description = "Deletes set amount of messages from current channel.")
async def clear(interaction, ammount: int):
    await Admin.clear(interaction, ammount)

@commands.command(name = "mass_move", description = "Moves everyone from all channels to current channel or specified channel")
async def mass_move(interaction, channel: VoiceChannel):
    await Admin.mass_move(interaction, channel)

@commands.command(name = "asian", description = "Plays the selected Asian sound effect in the selected voice channel.")
async def sound(interaction, channel: VoiceChannel, sound: Literal['Stopid', 'Emotional Damage', 'Failure', 'I Will Send You To Jesus']):
    await Audio.engine(interaction, client, channel, sound, 'asian')

@commands.command(name = "indian", description = "Plays the selected Indian sound effect in the selected voice channel.")
async def sound(interaction, channel: VoiceChannel, sound: Literal['Hello Your Computer Has Virus', 'Indian Song']):
    await Audio.engine(interaction, client, channel, sound, 'indian')

@commands.command(name = "sound_effect", description = "Plays the selected sound effect in the selected voice channel.")
async def sound(interaction, channel: VoiceChannel, sound: Literal['Skill Issue']):
    await Audio.engine(interaction, client, channel, sound, 'other')

@commands.command(name = "setup", description = "Sets up everything for the server for the bot to work properly.")
async def setup(interaction):
    await Admin.setup(interaction)

client.run(Data.Other.bot_token, log_level = 0)