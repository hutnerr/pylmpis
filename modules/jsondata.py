import json

##############################################################################################################################

def openFile():
    """
    Opens the data.json file and returns the data in it.
    """
    with open("data.json", "r") as file:
        return json.load(file)

##############################################################################################################################

def getKey(bot: str = None):
    """
    Gets a discord bot key.

    Parameters:
    - bot (str, optional): The bot to get the key for. Defaults to the main key
    """
    if bot == "test":
        return openFile()["testkey"]
    else:
        return openFile()["key"]

##############################################################################################################################

def getDiscordID():
    """
    Gets the host's discord ID.
    """
    return openFile()["discordID"]

##############################################################################################################################

def getLeetcodeChannel():
    """
    Gets the discord channel to send Daily Leetcode problems to.
    """
    return openFile()["leetcodeChannel"]


##############################################################################################################################

def getFilepath(loc:str = None):
    """
    Gets the filepath of the bot.
    """
    if loc == "pi":
        return openFile()["pifilepath"]
    elif loc == "laptop":
        return openFile()["laptopfilepath"]
    else:
        return openFile()["filepath"]