from lcbothelpers import problem_distrubutor as pd 

url = "https://leetcode.com/problems/"

prob = pd.getProblem("free.csv", "Easy")
print(f"{url}{prob[0]}")
probtitleneat = prob[0].replace("-", " ").title()
print(probtitleneat.title())