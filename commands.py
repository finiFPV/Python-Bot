from asyncio import Future
from discord import FFmpegPCMAudio, utils, Embed
from data import Data


class Audio:
    def play_async(self, voice_client, name, type):
        fut = Future()
        voice_client.play(FFmpegPCMAudio(f'./audio/{type}/{name}.mp3'),after=lambda e: fut.set_exception(e) if e else fut.set_result(None))
        return fut

    async def engine(self, interaction, client, channel, sound, type):
        if Data().owner == interaction.user.id or interaction.user.id in Data().authorized: mode = 0
        elif interaction.user.id in Data().uno_reversed_users:
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
        await voice_client.disconnect()
        await interaction.edit_original_response(embed = Embed(title = "✅🔊 Successful!", description = f"Successfully played `{sound}` in `{channel}`.", color = 0x00ff2a))