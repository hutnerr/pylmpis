import os

##############################################################################################################################

def getFolders(directory):
    """
    Gets a list of the folders in a directory.

    Parameters:
    - directory (str): The directory to search in
    
    Returns:
    - folders (list): A list of the folders in the directory
    """
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    return folders

##############################################################################################################################

def getFiles(directory):
    """
    Gets a list of the files in a directory.

    Parameters:
    - directory (str): The directory to search in
    
    Returns:
    - folders (list): A list of the folders in the directory
    """
    files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    return files
