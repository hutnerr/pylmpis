import asyncio
import os
import random

import discord
from discord import app_commands
from discord.ext import commands

import modules.files as f
import modules.jsondata as jd

filepath = jd.getFilepath()

############################################################################################################################## Cog Class

class misc(commands.Cog):
    """
    Contains all of the miscellaneous commands that don't fit into any other category.
    """
    
    ############################################################### Constructor
    
    def __init__(self, client: commands.Bot):
        """
        Constructor for the misc class.
        """
        self.client = client
    
    ############################################################### Goop Command
    
    @commands.command()
    async def goop(self, ctx):
        """
        Posts the goop face. Not a slash command. 
        """
        await ctx.send("⠀⠀⠀⢀⣠⣤⣶⣷⣿⣾⣦⣤⣤⣀⠀⠀⠀\n⠀⠀⢴⣾⣿⣿⠟⠛⠛⠻⠿⣿⣿⣿⣿⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣶⣶⣶⣶⣦⡤⠀\n⠀⣴⣿⣿⡟⣡⣴⣶⣶⣶⣤⣄⠉⢿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣷⡀\n⣼⣿⣿⡟⣰⣿⣿⣿⣿⣿⣿⣿⣷⡀⠙⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠈⠙⠻⣿⣿⣷⡄\n⣻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠸⣿⡇⠀⠀⠀⠀⣠⠀⠀⠀⣿⣿⣿⠃⠀⠀⣠⣾⣿⣿⣿⣶⣤⡀⣿⣿⣿⡄\n⠿⣿⣿⣿⣌⠻⣿⣿⣿⣿⣿⣿⣿⠟⠀⢠⣿⠇⠀⠀⠀⣤⣯⠀⠀⠀⣿⣿⡇⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⡇\n⠐⢿⣿⣿⣿⣷⣌⡙⠛⠻⠛⠋⢁⣠⣴⣿⠏⠀⢀⣴⣿⣿⣿⣷⡀⠀⢹⣿⣷⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⠀\n⠀⠝⢻⣿⣿⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿⠋⢀⣴⣿⣿⣿⣿⣿⣿⣷⠀⠙⣿⣿⣷⣄⡈⠛⠛⠛⠛⢛⣫⣵⣿⣿⣿⡇⠀\n⠀⠄⠀⠛⣿⢿⣿⣿⣿⣿⣿⠟⠉⠀⠁⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠐⠿⢿⣿⣿⣿⣷⣶⣶⣿⣿⣿⣿⣿⣿⣿⠃⠀\n⢠⣤⣄⣛⣹⣿⣇⣙⡏⠁⠀⠀⠀⠀⠀⠻⢿⠛⠻⢿⢿⣿⣿⣿⡇⠀⠀⠀⠙⠿⣿⡟⠭⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀\n⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣤⣀⣀⣀⡘⠀⠀⠀⠀⠐⢿⡿⠁⠀⠀⠀⠀⠀⣸⠃⠀⣨⣴⣿⣿⣿⣿⠇\n⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣧⡟⠹⣉⡿⠋⠻⡿⠻⢷⡶⠦⣾⣇⣀⣀⣀⣴⣶⣶⣿⣷⣾⣿⣿⡿⢿⣿⠏⠀⠀\n⠀⠀⠀⠀⠀⠸⣿⣿⣿⣾⣿⣩⣷⣤⣨⣧⡀⢀⠇⠀⠀⡇⠀⠀⢿⠀⢿⣭⣿⣿⣼⣿⣿⣿⡿⠋⠀⢸⡟⠀⠀\n⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⣶⣶⣧⣤⣼⣷⣿⣿⣿⣿⣿⠏⠀⠀⠀⠈⠇\n⠀⠀⠀⠀⠀⠀⠀⣿⡈⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀\n⠀⠀⠀⠀⠀⠀⠀⠈⠣⠀⠘⠻⣿⣿⣿⢿⣿⣿⣿⣿⡿⢿⣿⢿⣿⣿⣿⣿⣿⣿⠿⠃⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣷⣤⣧⣀⠀⡇⠀⠀⣧⠀⠸⠀⠘⢿⣿⠃⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣶⣶⣿⣦⣾⣷⣾⡿⠏⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⠟⠉⠁⠀⣸⡟⠑⠃⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⠃⠀⠀")
    
    ############################################################### on_message
    

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        This method is called whenever a message is received.
        Responds with "real" if the message contains "real".
        """
        if message.author == self.client.user: # Ignore bot messages
            return

        if 'real' in message.content.lower():
            await message.channel.send('real')


    ############################################################### Pick Slash Command
        
    # The classic /pick command. 
    @app_commands.command(name = "pick", description = "Picks a random choice from the list entered.")
    async def pick(self, interaction: discord.Interaction, args:str):
        """
        Picks a random choice from a list of choices, with optional weights.

        Parameters:
        - args (str): A string containing the choices and their optional weights, separated by spaces.
        
        If no weights are provided, the method picks a choice uniformly at random.
        If weights are provided, the method picks a choice based on the weights.

        Example usage:
        - pick("choice1 choice2 choice3") -> Picks a choice uniformly at random from "choice1", "choice2", and "choice3".
        - pick("choice1:2 choice2:3 choice3") -> Picks a choice based on the weights: "choice1" has weight 2, "choice2" has weight 3, and "choice3" has weight 1.
        """
        myDict = {} # Holds the choices and their weights
        arguments = args.split(" ")

        # If no weights at all, pick normally
        if ":" not in args:
            await interaction.response.send_message(random.choice(arguments))
            return

        # If there is at least one weight
        for choice in arguments: # Iterate over the choices and split them into the choice and the weight
            if ":" in choice:
                temp = choice.split(":")
                myDict[temp[0]] = float(temp[1]) # Use float instead of int to allow for decimal values
            else:
                myDict[choice] = 1 # If there is no weight, default to 1

        totalWeight = sum(myDict.values())                                      # Sum all of the weights to get the total weight
        weights = [weight / totalWeight for weight in myDict.values()]          # Calculate the weights. EX 1, 2, 3 -> 1/6, 2/6, 3/6 -> 1/6, 1/3, 1/2
        rchoice = random.choices(list(myDict.keys()), weights = weights)[0]     # Choose a random choice based on the weights. [0] is because it returns a list of one item

        await interaction.response.send_message(rchoice)

    ############################################################### Gamer Slash Command

    # Pings the server whenever the timer is set if set, otherwise just pings everyone
    @app_commands.command(name = "gamer", description = "Pings @everyone. Can be set for a time.")
    async def gamer(self, interaction: discord.Interaction, mins:int = 0):
        """
        Sends a gamer message after a specified amount of time.

        Parameters:
        - mins (int, optional): The number of minutes to wait before sending the gamer message. Defaults to 0.

        Raises:
        - Exception: If the specified number of minutes is greater than 720.
        """

        if mins > 720:
            raise Exception("12 Hour limit")
    
        gamerMessage = ("@everyone GAMER TIME GAMER TIME GAMER TIME GAMER TIME\n" +
                        "@everyone GAMER TIME GAMER TIME GAMER TIME GAMER TIME\n" + 
                        "@everyone GAMER TIME GAMER TIME GAMER TIME GAMER TIME\n")
        
        seconds = mins * 60
        
        # If a time was set, calculate the hours and the minutes
        # Use a response to send the message of when the time is set
        # Uses two different 
        # Sleep then send the gamer message after the set time. 
        if mins:
            hours, mins = divmod(mins, 60)
            await interaction.response.send_message(f"## Gamer time in {hours} hours, and {mins} mins" if hours else f"### Gamer time in {mins} mins")
            await asyncio.sleep(seconds)
            await interaction.channel.send(gamerMessage)
        
        # Need to have this in a separate statement so it can get a response and not time out due to the command being slept.
        # That is why this gamer is send through a response while the other is sent through the channel.
        else:
            await asyncio.sleep(seconds)
            await interaction.response.send_message(gamerMessage, allowed_mentions = discord.AllowedMentions(everyone = True))

    ############################################################### Bozo Slash Command
    
    @app_commands.command(name = "bozo", description = "Calls someone a bozo")
    async def bozo(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Increments the bozo count for a user in a CSV file or adds a new line for the user if not found.

        Parameters:
        - user (discord.Member, optional): The user for whom the bozo count should be incremented. If not provided, the interaction user is used.
        """
        path = os.path.join(filepath, "data", "csv", "bozo.csv")

        # If user is not provided, use the interaction user
        if user is None:
            user = interaction.user

        with open(path, "r+") as bozoFile:
            lines = bozoFile.readlines()
            found = False

            for i, bozo in enumerate(lines):
                bozoID, bozo_count = bozo.strip().split(",")

                if int(bozoID) == user.id:
                    bozo_count = str(int(bozo_count) + 1)
                    lines[i] = f"{bozoID},{bozo_count}\n"
                    found = True
                    break

            if not found:
                lines.append(f"{user.id},1\n")

            bozoFile.seek(0)
            bozoFile.truncate()

            bozoFile.writelines(lines)

            bozoFile.close()

        await interaction.response.send_message(f"{user.mention} is a bozo")

    ############################################################### Bozo Count Slash Command
    
    @app_commands.command(name = "bozocount", description = "Tells you how many times someone have been called a bozo")
    async def bozocount(self, interaction: discord.Interaction, user: discord.Member = None):
        """
        Retrieves the bozo count for a given user.

        Parameters:
        - user (discord.Member, optional): The user for whom to retrieve the bozo count. If not provided, the interaction user will be used.
        """
        path = os.path.join(filepath, "data", "csv", "bozo.csv")

        if user is None:
            user = interaction.user

        with open(path, "r") as bozoFile:
            for line in bozoFile:
                bozoID, bozo_count = line.strip().split(",")

                if int(bozoID) == user.id:
                    await interaction.response.send_message(f"{user.mention}: {bozo_count} times")
                    return
                
        await interaction.response.send_message(f"{user.mention} is not a bozo.")
        
    ############################################################### Bozo Board Slash Command
    
    # FIXME Might be an issue if there is too many bozos in the server and it becomes huge
    @app_commands.command(name = "bozoboard", description = "Lists the bozo ranking in the server.")
    async def bozoboard(self, interaction: discord.Interaction):
        """
        Displays the bozo leaderboard.
        """
        path = os.path.join(filepath, "data", "csv", "bozo.csv")

        membersAndId = {}
        bozosAndCount = {}

        for member in interaction.guild.members:
            membersAndId[member.id] = member.display_name
        
        with open(path, "r") as bozoFile:
            for line in bozoFile:
                bozoID, bozo_count = line.strip().split(",")

                if int(bozoID) in membersAndId:
                    bozosAndCount[int(bozoID)] = int(bozo_count)

        sorted_list = sorted(bozosAndCount.items(), key=lambda x: x[1])
        sorted_list.reverse()

        embed = discord.Embed(title = "Bozo Leaderboard", color = discord.Color.red())
        
        place = 1
        
        builtString = "```\n"
        for key, value in sorted_list:
            # builtString += f"{place}: " + str(membersAndId[key]) + "      " + str(value) + '\n'
            builtString += "{}. {:<20} {:>20}\n".format(place, str(membersAndId[key]), str(value))
            place += 1
            
        embed.add_field(name = "", value = builtString + "```")
        await interaction.response.send_message(embed = embed)
        
    ############################################################### Post Slash Command

    @app_commands.command(name = "post", description="Posts a message to a channel")
    @app_commands.choices(files = [
        app_commands.Choice(name = "(V) Jupiter", value = "jupiter.mp4"),
        app_commands.Choice(name = "(V) Market", value = "market.mp4"),
        app_commands.Choice(name = "(P) Alert", value = "alert.png"),
        app_commands.Choice(name = "(P) Apex", value = "apex.gif"),
        app_commands.Choice(name = "(P) Betrayal", value = "betrayal.jpg"),
        app_commands.Choice(name = "(P) Dog", value = "dog.jpg"),
        app_commands.Choice(name = "(P) Kaneki", value = "kaneki.jpg"),
        app_commands.Choice(name = "(M) CALLING", value= "apex.mp3")
    ])
    async def post(self, interaction: discord.Interaction, files:app_commands.Choice[str]):
        """
        Sends a message with a file based on the file type.

        Parameters:
        - files (app_commands.Choice[str]): The file to be sent.
        """

        pathDict = {
            "images": ["png", "jpg", "jpeg", "gif"],
            "videos": ["mp4", "mov"],
            "music": ["mp3"]
        }

        # Iterate over the dictionary and check if the file type is in the list of file types
        for key, value in pathDict.items():
            if files.value.split(".")[1] in value:
                path = os.path.join(filepath, "resources", key, files.value)
                break
        
        # Send the message with the file
        await interaction.response.send_message(file = discord.File(path))
    
    ############################################################### Clear Slash Command
    
    @app_commands.command(name = "clear", description = "Clears bot messages from the channel. Can be filtered by command name.")
    async def clear(self, interaction: discord.Interaction, command_names: str = None):
        """
        Clears messages output from specific commands from the channel.

        Parameters:
        - command_names (str, optional): A string containing the names of the commands whose messages should be cleared. 
          Multiple command names can be separated by spaces. If not provided, all bot messages will be cleared.
        """
        def msgCheck(m):
            if m.author != self.client.user:
                return False
            
            if command_names is None and m.interaction is not None: # If no commands set, clear interaction messages 
                return True
            
            if m.interaction is not None and m.interaction.name in command_names.split(): # If a command is set, clear only those commands
                return True
                
        if not interaction.guild.get_member(interaction.user.id).guild_permissions.administrator:
            await interaction.response.send_message("You are not allowed to run this command.", ephemeral = True)
            return
            
        await interaction.response.send_message("**Clearing messages...**")
        deleted = await interaction.channel.purge(check = msgCheck, bulk = True, limit = 100)
        await interaction.channel.send(f"Cleared `{len(deleted)}` messages")
    ############################################################### Error Handler
    
    @pick.error
    @gamer.error
    @bozo.error
    @bozocount.error
    @bozoboard.error
    @post.error
    @clear.error
    async def miscError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """
        Error handler.
        """
        await interaction.response.send_message(f"`{error}`", ephemeral = True)

############################################################################################################################## Setup for the cog command

async def setup(client: commands.Bot) -> None: 
    """
    Set up the cog.
    """
    await client.add_cog(misc(client))