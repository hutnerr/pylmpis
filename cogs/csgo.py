import csv
import os

import discord
from discord import app_commands
from discord.ext import commands

import modules.files as f
import modules.jsondata as jd

############################################################################################################################## Helper Functions

############################################################### setInstructions

def setInstructions(embed: discord.Embed, instructionsCSV):
    """
    Dynamically sets instructions for the choice based on the rows of a CSV file. 
    Allows for there to be differences in instructions since not all are the same. 
    
    Parameters:
    - embed (discord.Embed): The emebed we're setting the instructions to
    - instructionsCSV (string): The name of the CSV file to read from
    """
    with open(instructionsCSV, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        
        next(csv_reader)
        
        for row in csv_reader: # CSV Format: Title,Description
            embed.add_field(name = row[0], value = row[1], inline = False)

############################################################### setEmoji

def setEmoji(type):
    """
    Sets the emoji for the option based on who the nade is for. 
    
    Parameters:
    - type (string): The location of the nade being thrown
    
    Returns:
    - var (type): text
    """
    if type == "a":
        return "🅰️"
    elif type == "b":
        return "🅱️"
    elif type == "mid":
        return "Ⓜ️"
    else:
        return "⚪"

############################################################### loadCSV

def loadCSV(options:list, mapName, nadeType):
    """
    Uses a CSV file to load the options allowed per each map.
    Uses the map you set to find the directory
    
    Parameters:
    - options (list): A list to store the populated options.
    - mapName (str): The name of the map.
    - nadeType (str): The type of grenade.
    
    Returns:
    - options (list): The list of populated options.
    """
    directory = os.path.join(jd.getFilepath(), "resources", "counterstrike", mapName, nadeType)
    mapfileCSV = os.path.join(directory, f"{nadeType}.csv")
    
    with open(mapfileCSV, "r") as csv_file: # CSV Format: Label,Description,Side,Folder
        csv_reader = csv.reader(csv_file)
        
        next(csv_reader) # Skips the header row

        for row in csv_reader:
            
            # Set the variables 
            label = row[0]
            description = row[1]
            emoji = setEmoji(row[2]) # sets the emoji based on the type 
            filep = os.path.join(directory, row[3]) # Sets the filepath of what was chosen 
            
            # Add all of the variables to an option and append it to a list
            option = discord.SelectOption(label = label, description = description, emoji = emoji, value = filep)
            options.append(option)

    return options

############################################################### setFileInfo

async def setFileInfo(filepath):
    """
    Retrieves file information from the specified filepath and returns them as a list of discord.File objects.

    Parameters:
    - filepath (str): The path to the directory containing the files.

    Returns:
    - list: A list containing the discord.File objects representing the files. The list has the following structure:
        - [instructions, position, lineup, video]
        - If the instructions file is missing, it will be represented by an empty string.
    """
    files = f.getFiles(filepath)
    
    # TODO Make this more dynamic. 
    # Returns if there are instructions
    if len(files) == 4:
        # Sets the files from the filepath
        instructions = os.path.join(filepath, files[0])
        position = discord.File(os.path.join(filepath, files[1]))
        lineup = discord.File(os.path.join(filepath, files[2]))
        video = discord.File(os.path.join(filepath, files[3]))
        
        # Return the files to be used
        return [instructions, position, lineup, video]
    
    # This branch is used when there is no instructions.csv file
    # Different index values due to what getFiles returns
    else:
        position = discord.File(os.path.join(filepath, files[0]))
        lineup = discord.File(os.path.join(filepath, files[1]))
        video = discord.File(os.path.join(filepath, files[2]))

        # Empty string in place of instructions as a placeholder so same index values can be used
        return ["", position, lineup, video]

############################################################################################################################## MapSelect Class

class MapSelect(discord.ui.View):
    """
    A class representing a map selection view. This class is used to display a dropdown menu for selecting a map.
    Gets filled from the initial button, that is where mapName and nadeType come from.
    Hold the Map() select menu class since you must display it as a discord.ui.view but Map() must inheirt discord.ui.Select

    Parameters:
    - mapName (str): The name of the map.
    - nadeType (str): The type of grenade.
    """
    
    ############################################################### Constructor 

    def __init__(self, mapName, nadeType):
        """
        Constructor for the MapSelect class.

        Parameters:
        - mapName (str): The name of the map.
        - nadeType (str): The type of grenade.
        """
        super().__init__()
        self.add_item(Map(mapName, nadeType))
        

############################################################################################################################### Map Class

class Map(discord.ui.Select):
    """
    Represents a map selection dropdown.
    """
    
    ############################################################### Constructor
    
    def __init__(self, mapName, nadeType):
        """
        Constructs a Map object.
        This method initializes the object by creating options based on reading from a CSV file.
        
        Parameters:
        - mapName (str): The name of the map.
        - nadeType (str): The type of grenade.
        """
        options = loadCSV([],  mapName, nadeType)
        super().__init__(placeholder = "What would you like?", options = options)

    ############################################################### callback

    async def callback(self, interaction: discord.Interaction):
        """
        Callback function for when a value is received.
        
        This method performs several actions when a value is received:
        1. Runs setFileInfo to get the requested information (pictures, video, and instructions).
        2. Deletes the original interaction message and sends the position and lineup pictures.
        3. Creates an embed and populates it based on the content located in the CSV file of the specific choice.
        4. Sends the embed along with a button that allows you to click it to provide the associated video.
        """
        files = await setFileInfo(self.values[0])
        
        await interaction.message.delete()
        await interaction.channel.send(file = files[2])  # position pic
        await interaction.channel.send(file = files[1])  # lineup pic

        # TODO Make this more dynamic as well.
        if len(files) == 4: # If there are instructions
            embed = discord.Embed(title = "Instructions", color = discord.Color.from_rgb(153, 242, 226))
            setInstructions(embed, files[0])
            await interaction.channel.send(embed = embed, view=VideoButton(vid = files[3]))
        else:
            await interaction.channel.send(view = VideoButton(vid = files[3]))

############################################################################################################################## Button Class

# Button class, takes in the filepath of the video as a parameter
class VideoButton(discord.ui.View):
    """
    Button class for displaying a video tutorial.

    Attributes:
        video (str): The filepath of the video.
    """
    
    ############################################################### Constructor
    
    def __init__(self, vid:str):
        """
        Constructs a VideoButton object.

        Parameters:
            vid (str): The filepath of the video
        """
        super().__init__()
        self.video = vid  # the video filepath
    
    ############################################################### Button to send the video
    
    @discord.ui.button(label = "SEE FULL TUTORIAL", style = discord.ButtonStyle.green)
    async def vidButton(self, interaction: discord.Interaction, Button: discord.ui.Button):
        """
        Sends the video if the button is pressed.
        """
        await interaction.channel.send(file = self.video)
        await interaction.response.defer()
        
############################################################################################################################## OptionButtons Class

class OptionButtons(discord.ui.View):
    """
    A class representing a set of option buttons for a specific map.
    
    Attributes:
    - mapName (str): The name of the map associated with the option buttons.
    """
    
    ############################################################### Constructor

    def __init__(self, mapName):
        """Constructs an OptionButtons object.

        Parameters:
        - mapName (str): The name of the map associated with the option buttons.
        """
        self.mapName = mapName
        super().__init__()

    ############################################################### Buttons

    @discord.ui.button(label = "Smokes", emoji = "💨", style = discord.ButtonStyle.green)
    async def smokes(self, interaction: discord.Interaction, Button: discord.ui.Button):
        """
        Sends a message with the selected map and option type as "smokes".
        """
        await interaction.channel.send(view=MapSelect(self.mapName, "smokes"))
        await interaction.message.delete()

    @discord.ui.button(label = "Flashes", emoji = "💡", style = discord.ButtonStyle.green)
    async def flashes(self, interaction: discord.Interaction, Button: discord.ui.Button):
        """
        Sends a message with the selected map and option type as "flashes".
        """
        await interaction.channel.send(view=MapSelect(self.mapName, "flashes"))
        await interaction.message.delete()

    @discord.ui.button(label = "Molotovs", emoji = "🔥", style = discord.ButtonStyle.green)
    async def mollys(self, interaction: discord.Interaction, Button: discord.ui.Button):
        """
        Sends a message with the selected map and option type as "mollys".
        """
        await interaction.channel.send(view=MapSelect(self.mapName, "mollys"))
        await interaction.message.delete()

    @discord.ui.button(label = "Random", style = discord.ButtonStyle.blurple)
    async def random(self, interaction: discord.Interaction, Button: discord.ui.Button):
        """
        Sends a message with the selected map and option type as "random".
        """
        await interaction.channel.send(view = MapSelect(self.mapName, "random"))
        await interaction.message.delete()

############################################################################################################################## CSGO Cog Class

# Cog class to hold the slash commands
class csgo(commands.Cog):
    """
    A class representing the CSGO cog.
    """
    ############################################################### Constructor

    def __init__(self, client: commands.Bot):
        """
        Constructor for the CSGO Cog class.
        """
        self.client = client

    ############################################################### cs

    @app_commands.command(name = "cs", description = "Select a map and get tutorials")
    @app_commands.choices(maps = [
        app_commands.Choice(name = "Ancient", value = "ancient"),
        app_commands.Choice(name = "Anubis", value = "anubis"),
        app_commands.Choice(name = "Inferno", value = "inferno"),
        app_commands.Choice(name = "Mirage", value = "mirage"),
        app_commands.Choice(name = "Nuke", value = "nuke"),
        app_commands.Choice(name = "Overpass", value = "overpass"),
        app_commands.Choice(name = "Vertigo", value = "vertigo")
    ])
    async def cs(self, interaction: discord.Interaction, maps: app_commands.Choice[str]):
        """
        Select a map and get tutorials.

        Parameters:
        - maps (app_commands.Choice[str]): The chosen map.
        """
        await interaction.response.send_message(view = OptionButtons(maps.value))

    ############################################################### csError

    @cs.error
    async def csError(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """
        Error handler.
        """
        await interaction.response.send_message(f"`{error}`", ephemeral = True)

############################################################################################################################## Setup for the cog command

async def setup(client: commands.Bot) -> None: 
    """
    Set up the cog.
    """
    await client.add_cog(csgo(client))