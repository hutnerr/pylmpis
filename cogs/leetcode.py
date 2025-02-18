import csv
import os
import random
from datetime import datetime, time
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands, tasks

import modules.files as f
import modules.jsondata as jd
from lcbothelpers import problem_distrubutor as pd 


fpath = jd.getFilepath()

target = time(7, 0)  # Daily Leetcode target time. 7:00 AM
url = "https://leetcode.com/problems/"

# Toggle for daily leetcodes
disabled = False

# Easy,Medium,Hard for all difs
# Easy,Medium for easy and med, etc...
DAILYDIF = "Easy"

############################################################################################################################## Helper Functions

############################################################### reader

def reader(dif = "all.csv") -> list[Any]:
    """
    Reads a CSV file and returns its contents as a list of lists.

    Parameters:
    - dif (str, optional): The name of the CSV file to read. Defaults to "all.csv".

    Returns:
    - list: A list of lists representing the contents of the CSV file.
    """

    dif = os.path.join(fpath, "data", "csv", dif)
    
    choices = []

    with open(dif, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            choices.append(row)

    return choices

############################################################### linkBuilder

# Builds the link to the problem
def linkBuilder(choice) -> str:
    """
    Builds a URL link based on the given choice.

    Parameters:
    - choice (list): A list containing the choice information.

    Returns:
    - str: The URL link generated based on the choice.
    """
    return url + choice[1]

############################################################################################################################## Leetcode Cog

class leetcode(commands.Cog):
    """
    Leetcode Cog class
    """
    
    ############################################################### Constructor
    
    def __init__(self, client: commands.Bot) -> None:
        """
        Constructor for the Leetcode Cog class.
        """
        self.client = client
        self.dailyLeetcode.start() # Start the repeated task.

    ############################################################### Leetcode Slash Command

    # Gets a random leetcode problem.
    @app_commands.command(name = "leetcode", description = "Gets a link to a random leetcode problem")
    @app_commands.choices(difs = [
        app_commands.Choice(name = "Easy", value = "easy.csv"),
        app_commands.Choice(name = "Medium", value = "medium.csv"),
        app_commands.Choice(name = "Hard", value = "hard.csv"),
        app_commands.Choice(name = "All", value = "all.csv")])
    async def leetcode(self, interaction: discord.Interaction, difs: app_commands.Choice[str]) -> None:
        """
        Gets a link to a random leetcode problem.

        Parameters:
        - difs: The difficulty level of the problem to retrieve.
        """
        pList = reader(difs.value)
        link = linkBuilder(random.choice(pList))
        await interaction.response.send_message(link)
    
    ############################################################### 


    # async def toggleleetcode(self, interaction:discord.Interaction) -> None:
        # disabled = !disabled
    
    @tasks.loop(minutes = 1) # Check every minute
    async def dailyLeetcode(self) -> None:
        """
        Sends a daily Leetcode problem to a specified channel at a specific time on weekdays.

        This method checks the current time and compares it with the target time. If the current time matches the target time
        and it is a weekday (Monday to Friday), it retrieves a random Leetcode problem from a CSV file and sends it to the specified channel.

        Parameters:
        - self: The instance of the class.
        """
        now = datetime.now()
        time = now.time()
        weekday = now.weekday()
        
        if not disabled and time.hour == target.hour and time.minute == target.minute and weekday < 5:
        # if not disabled:
            channel = self.client.get_channel(jd.getLeetcodeChannel()) 
            
            url = "https://leetcode.com/problems/"
            prob = pd.getProblem("free.csv", DAILYDIF)
            urlout = f"{url}{prob[0]}"
            
            probtitleneat = prob[0].replace("-", " ").title()
    
            em = discord.Embed(
                title = probtitleneat,
                color = discord.Color.green(), # hard coding since its hard coded as easy only rn
                url = urlout
            )
            
            em.add_field(name = "Daily Leetcode! :eyes:", value = "", inline = False)
            
            await channel.send(embed=em)                                                                                                                                                                  #type: ignore  
             # Change the csv file to change the difficulty easy.csv medium.csv hard.csv all.csv
            role = discord.utils.get(channel.guild.roles, name = "CODING RATS")                                                                                                                                                                  #type: ignore
            await channel.send(content = role.mention)                                                                                                                                                                    #type: ignore

    @dailyLeetcode.before_loop
    async def before_say_hello(self) -> None:
        """
        Sets up the task
        """
        await self.client.wait_until_ready()
          
############################################################################################################################## Setup

async def setup(client: commands.Bot) -> None: 
    """
    Set up the cog.
    """
    await client.add_cog(leetcode(client))
