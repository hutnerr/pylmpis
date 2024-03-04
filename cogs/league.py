import discord
import requests
from bs4 import BeautifulSoup
from discord import app_commands
from discord.ext import commands

headers = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

UGGURL = "https://u.gg/lol/champions/"

############################################################################################################################## Helper Functions

############################################################### makeURL

def makeURL(name, type):
    """
    Constructs a URL based on the given name and type.

    Parameters:
    - name (str): The name to be used in the URL.
    - type (str): The type of the URL.

    Returns:
    - str: The constructed URL.
    """
    name = "".join(char.lower() for char in name if char.isalpha())
    return UGGURL + name + type

############################################################### removeTag

# TODO Make this more dynamic
def removeTag(tag):
    """
    Removes specific prefixes from a given tag.

    Parameters:
    - tag (str): The tag to remove prefixes from.

    Returns:
    - str: The tag with prefixes removed.
    """
    return tag.replace("The Rune ", "").replace("The Keystone ", "")

############################################################### makeSoup

def makeSoup(name):
    """
    Creates a BeautifulSoup object by making a GET request to a URL.

    Parameters:
    - name (str): The name parameter used to construct the URL.

    Returns:
    - BeautifulSoup: The BeautifulSoup object representing the parsed HTML content.
    """
    cleaned = makeURL(name, "/build")
    page = requests.get(cleaned, headers = headers)
    return BeautifulSoup(page.content, "html.parser")

############################################################################################################################## BeautifulSoup Functions

############################################################### getStats

def getStats(soup):
        """
        Extracts League Champion statistics from the given BeautifulSoup object.

        Parameters:
        - soup: BeautifulSoup object representing the HTML page

        Returns:
        - A list of lists, where each inner list contains the name of a statistic and its corresponding value.
            The statistics include Winrate, Rank, Pick Rate, and Ban Rate.
        """
        champ = soup.find("div", class_ = "champion-profile-page")
        stats = champ.find("div", class_ = "champion-ranking-stats-normal")

        # FIXME So apparently there is a couple different types of win-rate div classes, there is good tier, okay tier, volxd-tier
        # FIXME shingo-tier, etc. can make a function to try them all out and see which one works?
        winrate = stats.find("div", class_ = "win-rate okay-tier").find("div", class_ = "value").text
        rank = stats.find("div", class_ = "overall-rank").find("div", class_ = "value").text
        pickrate = stats.find("div", class_ = "pick-rate").find("div", class_ = "value").text
        banrate = stats.find("div", class_ = "ban-rate").find("div", class_ = "value").text
        
        return [["Winrate", winrate], ["Rank", rank], ["Pick Rate", pickrate], ["Ban Rate", banrate]]
    
############################################################### getRunes

def getRunes(soup):
    """
    Extracts and returns League Champion runes from the given BeautifulSoup object.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object representing the HTML page.

    Returns:
    - list: A list of runes, including the keystone and minor runes.
    """
    keystone = soup.find("div", class_ = "perk keystone perk-active")
    keystone = [removeTag(img["alt"]) for img in keystone.find_all("img", alt = True)]

    minorRunes = [removeTag(img["alt"]) for div in soup.find_all("div", class_ = "perk perk-active") for img in div.find_all("img")]

    runes = [keystone[0]] + minorRunes[:5]
    return runes

############################################################### getCounters

def getCounters(soup):
    """
    Extracts League Champion counters from the given BeautifulSoup object.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

    Returns:
    - list: A list of lists containing the champion name and counter percentage.
    """
    counters = soup.find_all("div", class_="matchups")
    counters = [div.get_text() for div in counters]
    counters = counters[0].split(" Matches")

    finalList = []
    for counter in counters:
        tag = counter.split("%")
        champion = tag[0][:-4]
        percent = tag[0][-4:]
        
        # TODO This is really bad code. Fix later
        charstore = ""
        for char in percent:
            if char.isalpha():
                percent = percent.replace(char, "")
                charstore += char

        finalList.append([champion + charstore, percent])

    return finalList

############################################################### getAbilities

def getAbilities(soup):
    """
    Retrieves a League Champion's order of maxing from the given BeautifulSoup object.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object containing the HTML data.

    Returns:
    - list: The order of abilities as a list of strings.
    """
    abilities = soup.find("div", class_ = "skill-priority-path")
    abilityOrder = [ability.text for ability in abilities.find_all("div", class_ = "champion-skill-with-label")]
    return abilityOrder

############################################################################################################################## League Cog Class

class league(commands.Cog):
    """
    League cog class

    This cog provides commands related to League of Legends, such as getting stats, runes, counters, and abilities for a champion.
    """
    
    ############################################################### Constructor

    def __init__(self, client: commands.Bot):
        """
        Constructor for the League cog.
        """
        self.client = client
        
    ############################################################### Stats Slash Command

    @app_commands.command(name = "stats", description = "Gets stats for a league champion")
    async def stats(self, interaction: discord.Interaction, champion: str):
        """
        Retrieves the stats for a League champion.

        Parameters:
        - champion (str): The name of the League champion.
        """
        soup = makeSoup(champion)
        stats = getStats(soup)
        embed = discord.Embed(title = f"{champion.capitalize()}", color=discord.Color.blue())
        builtFromList = ""
        for stat in stats:
            builtFromList += "{:<10} {:>10}\n".format(stat[0], stat[1])
        embed.add_field(name = "Stats", value = f"```{builtFromList}```", inline = False)
        await interaction.response.send_message(embed=embed)
    
    ############################################################### Runes Slash Command
    
    @app_commands.command(name = "runes", description = "Gets runes for a league champion")
    async def runes(self, interaction: discord.Interaction, champion: str):
        """
        Retrieves the runes for a League champion.

        Parameters:
        - champion (str): The name of the League champion.
        """
        soup = makeSoup(champion)
        runes = getRunes(soup)
        embed = discord.Embed(title = f"{champion.capitalize()}", color = discord.Color.blue())
        embed.add_field(name = "Keystone", value = f"```{runes[0]}```", inline = False)
        keystoneRunes = "\n".join(runes[1:4])
        secondaryRunes = "\n".join(runes[4:])
        embed.add_field(name = "Runes", value = f"```{keystoneRunes}\n\n{secondaryRunes}```", inline = False)
        await interaction.response.send_message(embed = embed)
        
    ############################################################### Counters Slash Command
    
    @app_commands.command(name = "counters", description = "Gets counters for a league champion")
    async def counters(self, interaction: discord.Interaction, champion: str):
        """
        Retrieves the counters for a League champion.

        Parameters:
        - champion (str): The name of the League champion.
        """
        soup = makeSoup(champion)
        counters = getCounters(soup)
        counters.pop(-1)
        embed = discord.Embed(title = f"{champion.capitalize()}", color = discord.Color.blue())
        builtFromList = ""
        for counter in counters:
            builtFromList += "{:<10} {:>10}%\n".format(counter[0], counter[1])
        embed.add_field(name = "Counters", value = f"```{builtFromList}```", inline = False)
        await interaction.response.send_message(embed = embed)
    
    ############################################################### Abilities Slash Command
    
    @app_commands.command(name = "abilities", description = "Gets abilities for a league champion")
    async def abilities(self, interaction: discord.Interaction, champion: str):
        """
        Retrieves the abilities for a League champion.

        Parameters:
        - champion (str): The name of the League champion.
        """
        soup = makeSoup(champion)
        abilities = getAbilities(soup)
        embed = discord.Embed(title = f"{champion.capitalize()}", color = discord.Color.blue())
        embed.add_field(name = "Abilities", value = f"```{abilities[0]} --> {abilities[1]} --> {abilities[2]}```", inline=False)
        await interaction.response.send_message(embed = embed)
    
    ############################################################### Error Handling
    
    @stats.error
    @runes.error
    @counters.error
    @abilities.error
    async def leagueErrors(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """
        Handles errors that occur in the League commands.

        Parameters:
        - error (app_commands.AppCommandError): The error that occurred.
        """
        await interaction.response.send_message("`Please type a correct champion. Don't type 'mundo', do 'drmundo' or 'dr mundo'.`", ephemeral = True)
        
############################################################################################### Setup for the cog command

async def setup(client: commands.Bot) -> None: 
    """
    Set up the cog.
    """
    await client.add_cog(league(client))