import time

"""
This file contains all functions for taking inputs and sanitisation
This file is used by both task1.py and task2.py
"""

"""
Function for checking if a given string can be cast as an integer
This function takes a string as a parameter and will return an integer
if the string can be cast as one. Else it will return "None"

Loosely imitates the function of string.isnumeric()
"""
def tryInt(string):
    # We use a try except statement to see if the string can be cast as an int
    try:
        # Tries to cast our string as an int, returns int if successful
        # An error is thrown if it can't be cast as an int, goes to except
        return int(string)
    # Except runs if our code above throws a runtime error. Returns None
    except:
        return None

"""
Function for inputting an integer
Will repeatedly ask the user for an input until a valid one is received
A valid input is one which does not break the following criteria:
- Only contains numeric characters (no strings)
- Does not contain a decimal value

Validation for these rules works on a "innocent until proven guilty" basis
We assume input is valid until it breaks one of the above criteria

We include options for a minimum value and maximum value
If the inputted integer is lower than the minumum or 
larger than the maximum then its is marked invalid

!!!IMPORTANT - MINIMUM AND MAXIMUM ARE INCLUSIVE

We include the option for a "stop code" which will cancel the input
If no stop code is included when the funciton is called then we do not allow cancel
If a stop code is provided we check if the input matches the stop code and return None

Stop code will mostly be used for inputting multiple integers (like in task 1)
But of course we still have the option of forcing an integer input
"""
def inputInteger(message, min=None, max=None, stopCode = None):
    # We create a boolean variable to store if input is valid or not
    validInput = False

    # This is our return variable, initialised with 0
    intInput = 0

    # Repeatedly ask the user for an input until a valid one is received
    while not validInput:
        # We treat all input as valid until until it breaks a criteria
        validInput = True

        # As user for input using message parameter
        userInput = input(message)

        # We check the input to see if it matches our stopcode
        # The escape character is used to stop inputting numbers
        # We use .lower() because this doesn't need to be case sensitive
        if stopCode and userInput.lower() == stopCode.lower():
            return None

        intInput = tryInt(userInput)

        # if our tryInt() function returns none, input is not an int
        if intInput == None:
            # input is not valid
            validInput = False

            # Give the user a nice message
            print("Input must be a valid integer, please try again")

            # Repeat the loop
            continue

        if min and intInput < min:
            validInput = False
            print(f"Input must be larger than or equal to {min}")

            # Repeat the loop
            continue

        if max and intInput > max:
            validInput = False
            print(f"Input must be no larger than {max}")
            
            # Repeat the loop
            continue

    # return our valid input
    return intInput

def inputYesNo(message):
    yesAnswers = ["yes", "y"]
    noAnswers = ["no", "n"]

    # We create a boolean variable to store if input is valid or not
    validInput = False

    # Repeatedly ask the user for an input until a valid one is received
    while not validInput:
        # We treat all input as valid until until it breaks a criteria
        validInput = True

        # As user for input using message parameter
        userInput = input(message)

        if userInput.lower() in yesAnswers:
            return True
        
        elif userInput.lower() in noAnswers:
            return False
        
        else:
            validInput = False
            print("Please Input yes or no")

"""
This function manages player inputs for our connect 4 game

Player inputs are made up of two parts

1. Action
    - Placing a disk (p)
    - Placing a special disk (s)
    - Removing a disc from a column (r)
2. The column to perform the action

so if a player wanted to place a disk in column 2, their input would be p2

Players have a 5 second time limit to make an action
It'd be near impossible to implement this limitation in real-time without the use of threading
The next best thing is to see how long it took the player to make their input
then just tell the player "you took to long tough shit" if they took longer than 5 seconds

The user only gets one attempt at input, if it is invalid it just skips their turn (skill issue)
"""
def inputAction(currentPlayer):
    # Make a record of  the current timestamp of when the player was asked for input
    startTime = time.time()

    # Ask the player for input
    playerInput = input(f"Please enter your action, Player {currentPlayer.getNum()}:").lower()

    # Initialise Return variables
    action = ""
    column = 0    

    # A valid input should be two in length
    if len(playerInput) != 2:
        print("Invalid input, skipping turn")
        # We return false if valid input is not received
        return False

    # We check to see if the first character of our input is a valid action
    if playerInput[0] in ["p", "s", "r"]:
        action = playerInput[0]
    else:
        print("Invalid Action (must be 'p', 's', or 'r'), skipping turn")
        return False
    
    # We check to see if the second character is an integer
    column = tryInt(playerInput[1])
    
    # If the input isn't an int, or it is an int but not a valid column
    if not column or not 1 <= column <= 7:
        print("Invalid Column Number, skipping turn")
        return False

    if time.time() - startTime > 5:
        print("Action must be inputted within five seconds, skipping turn")
        return False

    # Return both action and collumn
    return [action, column]