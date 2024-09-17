import inquirer
import pandas as pd
from tabulate import tabulate

watches = pd.read_csv("WatchDataset.csv")
yea
watches['Price (USD)'] = watches['Price (USD)'].replace({'\$': '', ',': ''}, regex=True)

watches['Price (USD)'] = watches['Price (USD)'].astype(float)

maxBudget = float(input("What is the maximum budget for the watch in dollars (USD): "))
watches = watches[watches["Price (USD)"] <= maxBudget]
print(watches)

movementTypes = watches["Movement Type"].unique()
movementTypes = list(movementTypes)
questions = [
    inquirer.List('Movement',
                  message="What Movement Type do you want?",
                  choices=movementTypes,
                  ),

]
answers = inquirer.prompt(questions)
print(answers["Movement"])

moveWatches = watches[watches["Movement Type"]==answers["Movement"]]

materialTypes = moveWatches["Strap Material"].unique()
MaterialTypes = list(materialTypes)

questions = [
    inquirer.List('Strap',
                  message="What Strap Material do you want?",
                  choices=MaterialTypes,
                  ),

]


answers = inquirer.prompt(questions)
print(answers["Strap"])

moveWatches = moveWatches[moveWatches["Strap Material"]==answers["Strap"]]

possibleOptions = len(moveWatches)

print("There is " + str(possibleOptions) + " possible choices, the top choices are: \n")

titles = moveWatches.apply(lambda row: f"{row['Brand']} {row['Model']}", axis=1).tolist()
questions = [
    inquirer.List('Learn',
                  message="Which one do you want to learn more about",
                  choices=titles,
                  ),

]
answers = inquirer.prompt(questions)
moveWatches['Brand_Model'] = moveWatches.apply(lambda row: f"{row['Brand']} {row['Model']}", axis=1)
selectedWatch = moveWatches[moveWatches['Brand_Model']==answers["Learn"]]

# print(tabulate(selectedWatch, headers="keys", tablefmt='simple'))

def cleanPrint(CurrentWatch):
    message = ""
    for col in CurrentWatch:
        if CurrentWatch[col].values[0] !="nan":
            print(col + ": ", CurrentWatch[col].values[0])


cleanPrint(selectedWatch.head(1))



