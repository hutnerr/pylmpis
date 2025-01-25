############################################################################################################################## IMPORTS 
import platform
import time
from typing import Literal

import discord
from colorama import Back, Fore, Style
from discord import app_commands
from discord.ext import commands

import modules.jsondata as jd

############################################################################################################################## CLIENT SETUP

# Custom client setup
class Client(commands.Bot):
    
    # Constructor that sets up the base client. 
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix = commands.when_mentioned_or("/"), intents = intents)
        
        self.cogslist = [
            "cogs.help",
            
            "cogs.csgo",
            "cogs.apex",
            "cogs.league",
            "cogs.calculator",
            
            "cogs.misc",
            "cogs.voice",
            "cogs.leetcode",
        ]


    # Allows for persistent views and loads cogs
    # self.add_view() for persistent views here. 
    async def setup_hook(self) -> None:
        for ext in self.cogslist:
            await self.load_extension(ext)


    # Prints out system info, syncs slash commands to the tree, and changes the bots status
    async def on_ready(self):
        prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S EST", time.localtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
        print(prfx + " Logged in as " + Fore.YELLOW + client.user.name)
        print(prfx + " Bot ID " + Fore.YELLOW + str(client.user.id))
        print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__) 
        print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
        synced = await client.tree.sync()
        print(prfx + " Slash CMDs Sycned " + Fore.YELLOW + str(len(synced)))
        await client.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = "/help for commands"))


# Create our main client ( Bot ) object   
client = Client()
client.remove_command("help") # remove default help so I can add custom one. 


############################################################################################################################## RELOAD COMMAND

# Custom check to make sure only owner can run the reload command.
def meCheck(interaction: discord.Interaction) -> bool:
    return interaction.user.id == jd.getDiscordID()

# Allows you to reload a cog from within discord so you don't have to re-run the bot every time. 
@client.tree.command(name = "reload", description = "Relods a Cog Class")
@app_commands.check(meCheck)
async def reload(interaction: discord.Interaction, cog:Literal["csgo", "calculator", "help", "misc", "voice", "apex", "leetcode", "league"]): # You can use a literal to set specific options
    await client.reload_extension(name = "cogs."+ cog.lower()) 
    await interaction.response.send_message(f"Succesfully reloaded **{cog}.py**")
   
# Error handling for the reload command.  
@reload.error
async def reloadError(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.CheckFailure): # Handle for my custom check
        await interaction.response.send_message("You are not a user allowed to run this command.", ephemeral=True)
    else: # Handles everything else 
        await interaction.response.send_message(f"Failed to reload cog\n`{error}`", ephemeral=True)

############################################################################################################################## Run the Bot

# client.run(jd.getKey("test"))
client.run(jd.getKey())
