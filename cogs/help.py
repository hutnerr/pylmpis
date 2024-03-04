import csv
import os

import discord
from discord import app_commands
from discord.ext import commands

import modules.files as f
import modules.jsondata as jd

# Makes the proper filepath requied. 
# fpath = os.path.join(jd.getFilepath(), "data", "help")
# fpath = os.path.join(jd.getFilepath("pi"), "data", "help")
fpath = os.path.join(jd.getFilepath("laptop"), "data", "help")


############################################################################################################################## Helper Functions
       
############################################################### setCommands

# Uses the csv files that hold the instructions to create an embed showing all of the commands
def setCommands():
    """
    Retrieves all the commands from the specified folders and creates an embed with the command information.

    Returns:
    - discord.Embed: An embed containing all the commands.
    """
    
    folders = f.getFolders(fpath)
    embed = discord.Embed(title = "All Commands")
    
    for cmdType in folders:
        field = setEmbedField(os.path.join(fpath, cmdType))
        embed.add_field(name = cmdType.capitalize(), value = field, inline = False)
    
    return embed

############################################################### setEmbedField

def setEmbedField(cmdpath):
    """
    Generates a formatted string containing the names of command files in a given folder.

    Args:
        cmdpath (str): The path to the folder containing the command files.

    Returns:
        str: A formatted string containing the names of the command files.
    """
    
    files = f.getFiles(cmdpath)
    field = "```"

    # For each command.csv file in the folder, split it to get rid of the .csv and add it to the field
    for cmd in files:
        command = cmd.split(".")
        field = f"{field} {command[0]}\n"
        
    # Return the field and finish the codeblock. 
    return field + "```"

############################################################### loadCSV

# Loads an embed based on the CSV file of the command
def loadCSV(command):
    """
    Loads a CSV file and creates an embed based on its contents.

    Args:
        command (str): The name of the command.

    Returns:
        discord.Embed: The embed containing the data from the CSV file.
    """

    file = os.path.join(fpath, command)
    
    # Opens the file and iterates through it
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file) # CSV FORMAT: Name,Value
        
        # SKIPS HEADER ROW
        next(csv_reader)
        
        # Initializes the embed based on the command asked about
        embed = discord.Embed(title = command.split("/")[1].split(".")[0].capitalize(), color = discord.Color.from_rgb(153, 242, 226))

        # Sets the fields of the embed based on the rows and fields located in the CSV file. 
        for row in csv_reader:
            embed.add_field(name = row[0], value = row[1], inline=False)

    # Returns the embed for use 
    return embed

############################################################################################################################## Help Cog

class help(commands.Cog):
    """
    Help Command Cog.
    Helps users find out about other commands. 
    """
    
    ############################################################### Constructor
    
    def __init__(self, client: commands.Bot):
        """
        Constructor for the help cog.
        """
        self.client = client
        
    ############################################################### Help Slash Command
    
    # TODO Make choices more dynamic
    @app_commands.command(name = "help", description = "Help function for more information on all commands.")
    @app_commands.choices(command = [
        app_commands.Choice(name = "Squad", value = "apex/squad.csv"),
        app_commands.Choice(name = "Map", value = "apex/map.csv"),
        app_commands.Choice(name = "Olympus", value = "apex/olympus.csv"),
        app_commands.Choice(name = "CS Nades", value = "csgo/cs.csv"),
        app_commands.Choice(name = "Abilities", value = "league/abilities.csv"),
        app_commands.Choice(name = "Counters", value = "league/counters.csv"),
        app_commands.Choice(name = "Runes", value = "league/runes.csv"),
        app_commands.Choice(name = "Stats", value = "league/stats.csv"),
        app_commands.Choice(name = "Calculator", value = "misc/calculator.csv"),
        app_commands.Choice(name = "Help", value = "misc/help.csv"),
        app_commands.Choice(name = "Leetcode", value = "misc/leetcode.csv"),
        app_commands.Choice(name = "Bozo", value = "misc/bozo.csv"),
        app_commands.Choice(name = "Bozo Count", value = "misc/bozocount.csv"),
        app_commands.Choice(name = "Gamer Time", value = "misc/gamer.csv"),
        app_commands.Choice(name = "Pick", value = "misc/pick.csv"),
        app_commands.Choice(name = "Post", value = "misc/post.csv"),
        app_commands.Choice(name = "Disconnect", value = "voice/dc.csv"),
        app_commands.Choice(name = "Outro", value = "voice/outro.csv"),
        app_commands.Choice(name = "Play", value = "voice/play.csv"),
        app_commands.Choice(name = "Skip", value = "voice/skip.csv"),
])
    async def help(self, interaction: discord.Interaction, command :app_commands.Choice[str] = None):
            """
            Displays help information for a specific command or all commands.

            Parameters:
            - command (app_commands.Choice[str], optional): The command for which help information is requested. If not provided, help information for all commands will be displayed.
            """
            if command is None:
                await interaction.response.send_message(embed = setCommands())
            else:
                await interaction.response.send_message(embed = loadCSV(command.value.lower().strip()))

    ############################################################### Error Handling

    # Error handling
    @help.error
    async def helpError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """
        Error handler.
        """
        await interaction.response.send_message(f"`{error}`", ephemeral=True)

############################################################################################################################## Setup for the cog command

async def setup(client: commands.Bot) -> None: 
    """
    Set up the cog.
    """
    await client.add_cog(help(client))