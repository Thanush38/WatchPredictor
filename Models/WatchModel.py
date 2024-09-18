import inquirer
import pandas as pd

def cleanPrint(CurrentWatch):
    for col in CurrentWatch:
        if CurrentWatch[col].values[0] != "nan":
            print(col + ": ", CurrentWatch[col].values[0])


def PredictWatch():
    # Load watch dataset from a CSV file into a pandas DataFrame
    watches = pd.read_csv("Data/WatchDataset.csv")

    # Clean the 'Price (USD)' column by removing '$' and ',' and converting it to a float
    watches['Price (USD)'] = watches['Price (USD)'].replace({'\$': '', ',': ''}, regex=True)
    watches['Price (USD)'] = watches['Price (USD)'].astype(float)

    # Get the maximum budget from the user and filter watches within the budget
    maxBudget = float(input("What is the maximum budget for the watch in dollars (USD): "))
    watches = watches[watches["Price (USD)"] <= maxBudget]

    # If no watches match the budget, inform the user
    if len(watches) == 0:
        print("No Watches match this budget")
        return

    # Get unique movement types from the filtered watches
    movementTypes = watches["Movement Type"].unique()
    movementTypes = list(movementTypes)

    # Ask the user to select a movement type using inquirer
    questions = [
        inquirer.List('Movement',
                      message="What Movement Type do you want?",
                      choices=movementTypes,
                      ),
    ]
    answers = inquirer.prompt(questions)
    print(answers["Movement"])

    # Filter watches based on the selected movement type
    moveWatches = watches[watches["Movement Type"] == answers["Movement"]]

    # Get unique strap materials from the filtered watches
    materialTypes = moveWatches["Strap Material"].unique()
    MaterialTypes = list(materialTypes)

    # Ask the user to select a strap material
    questions = [
        inquirer.List('Strap',
                      message="What Strap Material do you want?",
                      choices=MaterialTypes,
                      ),
    ]
    answers = inquirer.prompt(questions)
    print(answers["Strap"])

    # Filter watches based on the selected strap material
    moveWatches = moveWatches[moveWatches["Strap Material"] == answers["Strap"]]

    # Check how many watches match the criteria and print top choices
    possibleOptions = len(moveWatches)
    print("There is " + str(possibleOptions) + " possible choices, the top choices are: \n")

    # Create a list of watch brand and model titles for the user to choose from
    titles = moveWatches.apply(lambda row: f"{row['Brand']} {row['Model']}", axis=1).tolist()

    # Ask the user which specific watch they want to learn more about
    questions = [
        inquirer.List('Learn',
                      message="Which one do you want to learn more about",
                      choices=titles,
                      ),
    ]
    answers = inquirer.prompt(questions)

    # Create a new column for the brand and model combination and select the chosen watch
    moveWatches['Full Name'] = moveWatches.apply(lambda row: f"{row['Brand']} {row['Model']}", axis=1)
    selectedWatch = moveWatches[moveWatches['Full Name'] == answers["Learn"]]

    # Print the details of the selected watch (first row)
    cleanPrint(selectedWatch.head(1))

