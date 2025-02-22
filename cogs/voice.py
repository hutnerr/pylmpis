import asyncio
import os

import discord
from discord import FFmpegPCMAudio, app_commands
from discord.ext import commands

import modules.files as f
import modules.jsondata as jd

filepath = os.path.join(jd.getFilepath(), "resources", "music")

############################################################################################################################## Helper Functions

############################################################### botJoin

# Helper function so I can have the bot join in other commands when they need it to for more functionality. 
async def botJoin(interaction: discord.Interaction, voice):
    """
    Connects the bot to the voice channel specified by the user.

    Parameters:
    - voice: The voice client object representing the bot's connection to a voice channel.

    Returns:
    - voice: The updated voice client object.

    Raises:
    - commands.CommandError: If the user is not in a voice channel.
    """
    try:
        channel = interaction.user.voice.channel
    except Exception:
        raise commands.CommandError("You are not in a voice channel.")

    if voice:
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    return voice

############################################################### leaveVC

async def leaveVC(interaction: discord.Interaction):
    """
    Disconnects the bot from the voice channel.
    
    Raises:
    - commands.CommandError: If the bot is not in a voice channel.
    """
    voice = interaction.user.guild.voice_client
    if voice:
        await voice.disconnect()
        await interaction.response.send_message("Disconnected from voice channel.")
    else:
        raise commands.CommandError("The bot is not in a voice channel")
    
############################################################### playSong
    
async def playSong(interaction: discord.Interaction, song: str):
    """
    Plays a song in the voice channel.

    Parameters:
    - song (str): The name of the song to be played.

    Returns:
    - voice (discord.VoiceClient): The voice client object representing the bot's connection to the voice channel.
    """

    voice = interaction.user.guild.voice_client # Bot's current VC

    # If the bot is not in a voice channel, or in a different one, join the user's channel
    if not voice or voice.channel != interaction.user.voice.channel:
        voice = await botJoin(interaction, voice)
        await asyncio.sleep(1) # Sleep for a second to make sure the bot is in the channel before playing the song

    songpath = os.path.join(filepath, song)

    # If a song is playing, stop it to play the new one
    if voice.is_playing():
        voice.stop()

    voice.play(discord.FFmpegPCMAudio(songpath))

    if song == "outro.mp3":
        await interaction.response.send_message("# Goodbye Gamers :saluting_face:")
    else:
        await interaction.response.send_message(f"Playing `{song.split('.')[0].capitalize()}`")

    return voice

############################################################################################################################## Voice Cog

# COG FOR THE VOICE COMMANDS
class voice(commands.Cog):
    """
    A class representing the voice cog.

    This cog handles voice-related commands for the Discord bot.
    """
    
    ############################################################### Constructor

    def __init__(self, client: commands.Bot):
        """
        Constructor for the voice cog.

        Parameters:
        - client (commands.Bot): The Discord bot client.
        """
        self.client = client
    
    ############################################################### Play Slash Command

    # TODO Make this dynamic so that the choices are populated based on what's in the folder
    @app_commands.command(name = "play", description = "Plays a song")
    @app_commands.choices(song = [
        # app_commands.Choice(name = "Apex", value = "apex.mp3"),
        app_commands.Choice(name = "American Wrapper", value = "aw.mp3"),
        app_commands.Choice(name = "Death Note", value = "deathnote.mp3"),
        app_commands.Choice(name = "Hunter x Hunter", value = "hxh.mp3"),
        app_commands.Choice(name = "Jupiter", value = "jupiter.mp3"),
        app_commands.Choice(name = "Naruto 1", value = "naruto1.mp3"),
        app_commands.Choice(name = "Naruto 2", value = "naruto2.mp3"),
        app_commands.Choice(name = "Outro", value = "outro.mp3"),
        # app_commands.Choice(name = "Tense Long", value = "tenseL.mp3"),
        app_commands.Choice(name = "Tense Short", value = "tenseS.mp3"),
        app_commands.Choice(name = "Train 1", value = "train1.mp3"),
        app_commands.Choice(name = "Train 2", value = "train2.mp3"),
        app_commands.Choice(name = "Viking", value = "viking.mp3"),
        app_commands.Choice(name = "Wakeup", value = "wakeup.mp3"),
        app_commands.Choice(name = "You Say Run", value = "yousayrun.mp3"),
        app_commands.Choice(name = "Zen", value = "zen.mp3"),
        app_commands.Choice(name = "Mongolian Throat Singing", value = "mongolian.mp3"),
        app_commands.Choice(name = "Big Bad Wolf", value = "bigbadwolf.webm"),
        app_commands.Choice(name = "Bleach Spirital Pressure", value = "bleach.webm"),
        app_commands.Choice(name = "Cowboy Intro", value = "cowboyintro.webm"),
        app_commands.Choice(name = "Erwin Speech", value = "erwinspeech.webm"),
        # app_commands.Choice(name = "Everything Black", value = "everythingblack.webm"),
        app_commands.Choice(name = "Fairy Tail", value = "fairytail.webm"),
        app_commands.Choice(name = "That Boys a Glider", value = "glider.webm"),
        # app_commands.Choice(name = "Moog City", value = "moogcity.webm"),
        app_commands.Choice(name = "Sadness & Sorrow", value = "sadnesssorrow.webm"),
        app_commands.Choice(name = "Severance", value = "severance.webm"),
        app_commands.Choice(name = "Sneaky Snitch", value = "sneaky-snitch.webm"),
        app_commands.Choice(name = "Terraria Overworld", value = "terraria-overworld.webm"),
        # app_commands.Choice(name = "Terraria Underworld", value = "terraria-underworld.webm"),
    ])
    async def play(self, interaction: discord.Interaction, song: app_commands.Choice[str]):
        """
        Plays a song in the voice channel.

        Parameters:
        - song (str): The name or URL of the song to be played.
        """
        await playSong(interaction, song.value)
        
    ############################################################### Outro Slash Command

    # outro
    @app_commands.command(name = "outro", description = "Plays the outro song")
    async def outro(self, interaction: discord.Interaction):
            """
            Plays the outro song, waits for the drop, and then disconnects all from the VC.
            """
            voice = await playSong(interaction, "outro.mp3")
        
            await asyncio.sleep(58)
            
            for user in voice.channel.members:
                await user.move_to(None)
            
    ############################################################### Skip and DC Slash Commands

    # aliased commands
    
    # Disconnects the bot from VC
    @app_commands.command(name = "skip", description = "Skips the current song playing.")
    async def skip(self, interaction: discord.Interaction):
        """
        Disconnects the bot from the voice channel.
        """
        await leaveVC(interaction)

    # Disconnects the bot from VC
    @app_commands.command(name = "dc", description = "Disconnects the bot from it's current VC")
    async def dc(self, interaction: discord.Interaction):
        """
        Disconnects the bot from the voice channel.
        """
        await leaveVC(interaction)
    
    ############################################################### Error Handling

    @skip.error
    @dc.error
    @play.error
    @outro.error
    async def error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """
        Error handler.
        """
        await interaction.response.send_message(f"`{error}`", ephemeral=True)
        
############################################################################################################################## Setup for the cog command

async def setup(client: commands.Bot) -> None: 
    """
    Set up the cog.
    """
    await client.add_cog(voice(client))