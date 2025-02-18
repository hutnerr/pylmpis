""" 
Related to distributing problems to users

Functions: 
    - getProblem(file:str, dif:str) -> list
    - getProblemFromSettings(serverID: int, problemID: int) -> list
"""
import os

from lcbothelpers import file_helper as fh
from lcbothelpers import random_helper as rh
from lcbothelpers.consts import Difficulty as difs

def getProblem(file:str, dif:str) -> list:
    """
    Get a problem from a problem set file based on the difficulty
    Args:
        file (str): The file name of the problem set. e.g "free.csv" or "paid.csv"
        dif (str): The csv difficulty string. e.g "Easy,Medium"
    Returns:
        list: The problem as a list of strings. e.g ["two-sum", "Easy", "false"]
    """
    problemsetFilepath = os.path.join("data", "problem_sets", file)
    problems = fh.fileToList(problemsetFilepath)
    difficulties = dif.split(",") 
    
    if len(difficulties) > 3 or len(difficulties) < 1:
        print("invalid difficulty string") 
        return None
    
    # we know we want a random problem if it was explicitly asked for or if all difficulties are allowed
    if dif == difs.RANDOM.value or len(difficulties) == 3:
        return rh.getRandom(problems).split(",")
    
    filtered = []
    
    # if there is only or two difficulties, we need to filter the problems to only those difficulties
    for problem in problems:
        if problem.split(",")[1] in difficulties:
            filtered.append(problem.split(","))

    return rh.getRandom(filtered)
