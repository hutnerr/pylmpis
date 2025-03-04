from lcbothelpers import problem_distrubutor as pd 
import random 

url = "https://leetcode.com/problems/"

mydifs = ["Easy", "Medium"]

# prob = pd.getProblem("free.csv", DAILYDIF)
prob = pd.getProblem("free.csv", random.choice(mydifs))

# prob = pd.getProblem("free.csv", "Easy")
print(f"{url}{prob[0]}")
probtitleneat = prob[0].replace("-", " ").title()
print(probtitleneat.title())