"""
This script:
- Prompts the user to enter multiple integers
- Saves these integers to a list
- Calculates the amount of integers, their sum, mean, minimum and maximum
- Finds if any numbers are prime numbers
- Outputs this information to the terminal
"""

# Import all our math and input functions
from mathsfunctions import *
from inputfunctions import *


inputtingNumbers = True
numbers = []

while inputtingNumbers:
    value = inputInteger("Please enter a valid integer number, or enter 'stop' to stop entering numbers: ")

    # If 'stop' is entered then inputInteger will return None
    if value == None:
        inputtingNumbers = False
    
    # A valid integer is inputted
    else:
        numbers.append(value)

print(f"These are the {count(numbers)} numbers you entered: ")
print(f"{number}, " for number in numbers)
print(f"Their sum is {sum(numbers)}")
print(f"Their mean is {mean(numbers)}")
print(f"The list had a minimum value of {minimum(numbers)} and a maximmum of {maximum(numbers)}")