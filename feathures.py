from discord import FFmpegPCMAudio, utils, Embed, VoiceChannel
from asyncio import Future, sleep
from time import monotonic
from data import Data


class Audio:
    @staticmethod
    def play_async(voice_client, name, type):
        fut = Future()
        voice_client.play(FFmpegPCMAudio(f'./audio/{type}/{name}.mp3'),after=lambda e: fut.set_exception(e) if e else fut.set_result(None))
        return fut

    async def engine(self, interaction, client, channel, sound, type):
        if Data.Other.music_enabled == True:
            if type not in Data.Other.music_types_allowed and Data.Id.owner != interaction.user.id:
                await interaction.response.send_message(embed = Embed(title = "❌🔊 Not authorized!", description = "You are not the authorized to play this type of audio!", color = 0xff0000), ephemeral = True)
                return
            if Data.Id.owner == interaction.user.id or interaction.user.id in Data.Id.authorized: mode = 0
            elif interaction.user.id in Data.Id.uno_reversed_users:
                mode = 1
                channel = interaction.user.voice.channel
            else:
                await interaction.response.send_message(embed = Embed(title = "❌🔊 Not authorized!", description = "You are not in the authorized people list!", color = 0xff0000), ephemeral = True)
                return
            await interaction.response.send_message(embed = Embed(title = "🔊 Playing...", description = f"Starting to play `{sound}` in `{channel}`.", color = 0xeeff00), ephemeral = True)
            voice_client = utils.get(client.voice_clients, guild = interaction.guild)
            if voice_client is None: voice_client = await channel.connect(self_deaf = True)
            if voice_client.is_playing() == True:
                await interaction.edit_original_response(embed = Embed(title = "❌🔊 Already playing something!", description = "The bot is already playing something. Please try again later!", color = 0xff0000))
                return
            if mode == 0:
                await self.play_async(voice_client, sound.replace(' ', '_').lower(), type)
            elif mode == 1:
                for sound in ['i_will_send_you_to_jesus', 'failure', 'emotional_damage', 'stopid']:
                    await self.play_async(voice_client, sound, 'asian')
                await self.play_async(voice_client, 'skill_issue', 'other')
            await voice_client.disconnect()
            await interaction.edit_original_response(embed = Embed(title = "✅🔊 Successful!", description = f"Successfully played `{sound}` in `{channel}`.", color = 0x00ff2a))
        else: 
            await interaction.response.send_message(embed = Embed(title = "❌🔊 Disabled!", description = "This feature is currently disabled!", color = 0xff0000), ephemeral = True)

class Admin:
    @staticmethod
    async def clear(interaction, ammount: int):
        perms = interaction.permissions
        allowed = perms.manage_messages == True and perms.read_message_history == True
        if Data.Id.owner == interaction.user.id or perms.administrator == True or allowed == True:
            await interaction.response.send_message(embed = Embed(title = "🗑️ Deleting...", description = f"Deleting: `{ammount}` message(s).", color = 0xeeff00), ephemeral = True)
            await sleep(3)
            await interaction.channel.purge(limit = ammount + 1)
            await interaction.edit_original_response(embed = Embed(title = "✅🗑️ Successful!", description = f"Successfully deleted `{ammount}` message(s).", color = 0x00ff2a))
        else:
            await interaction.response.send_message(embed = Embed(title = "❌🗑️ Failed!", description = "You don't have: `manage_messages` and/or `read_message_history` permission(s)", color = 0xff0000), ephemeral = True)

    @staticmethod
    async def mass_move(interaction, channel: VoiceChannel):
        perms = interaction.permissions
        if Data.Id.owner == interaction.user.id or perms.administrator == True or perms.move_members == True:
            await interaction.response.send_message(embed = Embed(title = "⏬ Moving...", description = f"Moving all server's active members to `{channel.name}`", color = 0xeeff00), ephemeral = True)
            await sleep(3)
            for member in interaction.guild.members:
                if member.voice is not None:
                    await member.move_to(channel)
            await interaction.edit_original_response(embed = Embed(title = "✅⏬ Successful!", description = f"Successfully moved all active server's members to `{channel.name}`", color = 0x00ff2a))
        else:
            await interaction.response.send_message(embed = Embed(title = "❌⏬ Failed!", description = "You don't have: `move_members` permission", color = 0xff0000), ephemeral = True)

    @staticmethod
    async def setup(interaction):
        if Data.Id.owner == interaction.user.id or interaction.permissions.administrator == True:
            await interaction.response.send_message(embed = Embed(title="⚙️ Setting Up...", description="Starting to set up the server.", color = 0xeeff00), ephemeral = True)
            changes_made = False
            embed = Embed(title = "✅⚙️ Successful!", description = f"Setting up done! Changes made are:", color = 0x00ff2a)
            if utils.get(interaction.guild.channels, name = Data.Private_Channel.channel) is None:
                await interaction.guild.create_voice_channel(Data.Private_Channel.channel)
                changes_made = True
                embed.add_field(name = "Created voice channel:", value = Data.Private_Channel.channel)
            await sleep(3)
            if changes_made == False:
                await interaction.edit_original_response(embed = Embed(title = "✅⚙️ Successful!", description = f"No setting up was needed. Everything is already set up.", color = 0x00ff2a))
            else:
                await interaction.edit_original_response(embed = embed)
        else:
            await interaction.response.send_message(embed = Embed(title="❌⚙️ Failed!", description="You don't have: `administrator` permission!", color = 0xff0000), ephemeral = True)

class Info:
    @staticmethod
    async def ping(interaction):
        before = monotonic()
        await interaction.response.send_message(content = 'Pong!', ephemeral = True)
        ping = int((monotonic() - before) * 1000)
        embed = Embed(title = "Pong! 🏓", description = f"Bot's ping: `{ping}ms`", color = 0xff0000)
        await interaction.edit_original_response(content = None, embed = embed)

class Features:
    @staticmethod
    async def private_channel(member, before, after):
        if after.channel is not None and after.channel.name == Data.Private_Channel.channel:
            if member.id in Data.Id.uno_reversed_users:
                await member.voice_client.disconnect()
                return
            category = utils.get(member.guild.categories, name = Data.Private_Channel.category)
            if category is None: category = category = await member.guild.create_category(Data.Private_Channel.category)
            if member.nick is None: name = member.name
            else: name = member.nick
            channel = await category.create_voice_channel(f"{name}'s channel")
            await channel.set_permissions(member, manage_channels = True, manage_roles = True)
            Data.Private_Channel.channels.append(channel.name)
            await member.move_to(channel)
        if before.channel is not None and before.channel.name in Data.Private_Channel.channels and before.channel.members == []:
            await before.channel.delete()
            if before.channel.category.channels == []: await before.channel.category.delete()