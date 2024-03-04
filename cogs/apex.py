import datetime
import os
import random

import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands

import modules.files as f
import modules.jsondata as jd

# path = jd.getFilepath()
path = jd.getFilepath("pi")
# path = jd.getFilepath("laptop")

mapURL = "https://apexlegendsstatus.com/current-map/battle_royale/pubs"

############################################################################################################################## Helper Functions

############################################################### scrapeMaps

def scrapeMaps():
    """
    Scrapes map and time data from a webpage and returns the scraped data.

    Returns:
    - maps (list): A list of map names.
    - times (list): A list of time ranges in EST and 12-hour format.
    - timesWhen (list): A list of time descriptions, such as "Starts in 1 hour" or "Ends in 5 minutes".
    """
    maps, times, timesWhen = [], [], []
  
    page = requests.get(mapURL)
    soup = BeautifulSoup(page.content, "html.parser")

    for i in soup.find_all("h3"): # Times are under h3 tags
        map_data = i.text
        maps.append(map_data)

    for i in soup.find_all("p"): # Maps are under p tags
        time_data = i.text
        times.append(time_data)

    # Clean up the lists and make them each have 10 items
    times = times[1:11]
    maps = maps[0:10]

    # Iterate through the times and correct the times be in EST and 12 hr 
    for index, time in enumerate(times):
        startTime = (adjustTime(time[5:10])) # 5:10 and 14:19 are the time portions of the string "time"
        endTime = (adjustTime(time[14:19])) 
        times[index] = startTime + " --- " + endTime # Update the list with the adjusted values
        timesWhen.append(time[21:].capitalize()) # This adds the "Starts in 1 hour" or "Ends in 5 minutes" etc

    # The maps are parallel indexed. map[0] is the map for times[0] etc
    return [maps, times, timesWhen]

############################################################### adJustTime

def adjustTime(time):
    """
    Adjusts the given time based on the current date and a timezone offset of 5 hours.

    Parameters:
    - time (str): The time to be adjusted in the format "HH:MM".

    Returns:
    - str: The adjusted time in the format "HH:MM".
    """
    currentTime = datetime.datetime.now() # Get the current date and time          EX: 2024-01-31 15:01:52.565209
    offset = datetime.timedelta(hours = 5)  # Adjust the timezone offset to 5 hours  EX: 5:00:00

    # Split the time and set the hour and minute
    time_parts = time.split(":")
    hour = int(time_parts[0])
    minute = int(time_parts[1])

    changedTime = currentTime.replace(hour = hour, minute = minute) - offset  # 12:00  EX: 2024-01-31 07:00:03.366483

    adjustedTime = changedTime.strftime("%I:%M") # Format time to 12hr not 24hr EX: 07:00 AM

    return adjustedTime

############################################################################################################################## Apex Cog

class apex(commands.Cog):
    """
    A Discord Cog for Apex Legends related commands.
    """
    
    ############################################################### Constructor

    def __init__(self, client: commands.Bot):
        """
        Initializes an instance of the Apex Cog class.

        Parameters:
        - client (commands.Bot): The Discord bot client.
        """
        self.client = client

    ############################################################### Squad Slash Command

    @app_commands.command(name = "squad", description = "Picks a random Apex Squad.")
    @app_commands.choices(players = [
        app_commands.Choice(name = "1", value = 1),
        app_commands.Choice(name = "2", value = 2),
        app_commands.Choice(name = "3", value = 3)])
    async def squad(self, interaction: discord.Interaction, players: app_commands.Choice[int] = None):
        """
        Picks a random Apex squad based on the number of players specified.

        Parameters:
        - players (app_commands.Choice[int], optional): The number of players in the squad. Defaults to None.
        """
        fpath = os.path.join(path, "data", "txt", "apex.txt")

        # If not set, use 3 players
        if players is None:
            playerNum = 3
        else:
            playerNum = players.value

        # Open the file of the list of legends and create a list of them
        with open(fpath, "r") as file:
            lines = file.readlines()
            
        legends = []
        
        # Choose a random legend (no duplicates) and add it to the list
        while len(legends) < playerNum:
            rchoice = random.choice(lines).strip()
            if rchoice not in legends:
                legends.append(rchoice)

        embed = discord.Embed(title = "APEX SQUAD", description = "")

        for num, legend in enumerate(legends):
            embed.add_field(name = f"Player {num + 1}", value = f"```{legend}```", inline = False)

        await interaction.response.send_message(embed = embed)
    
    ############################################################### Map Slash Command

    @app_commands.command(name = "map", description = "Tells you the Apex Legends map rotation")
    async def map(self, interaction: discord.Interaction):
        """
        Sends an embed message with the Apex Legends map rotation.
        """
        # scrapeMaps() returns the maps and times in a list so we split them apart here
        lists = scrapeMaps()
        maps = lists[0]         # EX [Kings Canyon, Olympus, World's Edge]
        times = lists[1]        # EX [12:00 --- 13:00, 13:00 --- 14:00, 14:00 --- 15:00]
        timesWhen = lists[2]    # EX [Ends in 5 minutes, Starts in 1 hour, 5 minutes]

        # Initialize and create the embed
        embed = discord.Embed(title = "APEX MAP ROTATION", description = "", color = discord.Color.teal())

        # Add the next 6 maps to the embed
        for i in range(6):
            embed.add_field(name = maps[i], value = f"```{times[i]}\n\n{timesWhen[i]}```", inline = False)
        
        await interaction.response.send_message(embed = embed)

    ############################################################### Olympus Slash Command
        
    @app_commands.command(name = "olympus", description = "Tells you the next times for Olympus")
    async def olympus(self, interaction: discord.Interaction):
        """
        Sends an embed message with the next times for Olympus.
        """
        # scrapeMaps() returns the maps and times in a list so we split them apart here
        lists = scrapeMaps()
        maps = lists[0]         # EX [Kings Canyon, Olympus, World's Edge]
        times = lists[1]        # EX [12:00 --- 13:00, 13:00 --- 14:00, 14:00 --- 15:00]
        timesWhen = lists[2]    # EX [Ends in 5 minutes, Starts in 1 hour, 5 minutes]
        olympusExists = False   # Boolean to check if Olympus is in the rotation

        embed = discord.Embed(title = "OLYMPUS ROTATION", description = "", color = discord.Color.teal())

        # Iterate over all maps and search for olympus, adding to embed when found
        for i in range(len(maps)):
            if maps[i] == "Olympus":
                embed.add_field(name = maps[i], value = f"```{times[i]}\n\n{timesWhen[i]}```", inline = False)
                olympusExists = True 
        
        if olympusExists:
            await interaction.response.send_message(embed = embed)
        else:
            await interaction.response.send_message("# Olympus not in rotation :(")

    ############################################################### Error Handling

    @squad.error
    @map.error
    @olympus.error
    async def apexError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """
        Error handler.
        """
        await interaction.response.send_message(f"`{error}`", ephemeral = True)

############################################################################################################################## Setup for the cog command

async def setup(client: commands.Bot) -> None: 
    """
    Set up the cog.
    """
    await client.add_cog(apex(client))