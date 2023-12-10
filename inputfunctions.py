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

We include the option for a "stop code" which will cancel the input
If no stop code is included when the funciton is called then we do not allow cancel
If a stop code is provided we check if the input matches the stop code and return None

Stop code will mostly be used for inputting multiple integers (like in task 1)
But of course we still have the option of forcing an integer input
"""
def inputInteger(message, stopCode = None):
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

        # We check the input for our escape phrase "stop"
        # The escape character is used to stop inputting numbers
        # We use .lower() because this doesn't need to be case sensitive
        if stopCode and userInput.lower() == stopCode:
            return None

        intInput = tryInt(userInput)

        # if our tryInt() function returns none, input is not an int
        if intInput == None:
            # input is not valid
            validInput = False

            # Give the user a nice message
            print("Input must be a valid integer, please try again")

    # return our valid input
    return intInput
