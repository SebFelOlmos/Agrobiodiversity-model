def get_choice():
    while True:
        try:
            print('''
KIN model! :D 
What do you want to see? Write the number! 
1. First experiment: Role of kinship and inheritance on diversity at the community level.
2. Second experiment: Effect of different parameters on diversity at the community level.
3. Validation of the model: kinship dynamics and Behavior of the population. 

Remember, results are going to be in the Outputs folder
''')
            choice = input("Enter your choice (1, 2, or 3): ").strip()
            choice = int(choice)
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Invalid choice. Please select a number between 1 and 3.\n")
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).\n")

choice = get_choice()

if choice == 1:
    print("Lets go to the first experiment script...")
    # Path to the file to be executed
    script_path = "Experiment_1.py"
    with open(script_path, "r") as file:
        script_code = file.read()
    exec(script_code)
elif choice == 2:
    print("Lets go to the second experiment script...")
    # Path to the file to be executed
    script_path = "Experiment_2.py"
    with open(script_path, "r") as file:
        script_code = file.read()
    exec(script_code)
else:
    print("Lets go to the validation of the model script...")
    # Path to the file to be executed
    script_path = "Validation kinship systems.py"
    with open(script_path, "r") as file:
        script_code = file.read()
    exec(script_code)



