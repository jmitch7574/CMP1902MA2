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


# Boolean value, program will continue asking for input while true
inputtingNumbers = True

# Create an empty list to contain inputted numbers
numbers = []

# keep asking the user for input while true
while inputtingNumbers:
    # get user input using inputInteger function in inputfunctions.py
    value = inputInteger("Please enter a valid integer number, or enter 'stop' to stop entering numbers: ")

    # If 'stop' is entered then inputInteger will return None
    if value == None:
        # False value stops loop
        inputtingNumbers = False
    
    # A valid integer is inputted
    else:
        # Add number to our list
        numbers.append(value)
        # Confirm addition to user
        print(f"Added {value}")

"""
Output the count, sum, mean, min, max and primes of our numbers
We use .join to output our numbers with comma separation
We use map to ensure that numbers are cast as strings(.join throws an error when given integers)
Also print some massive lines out for ⭐ asthetics ⭐
"""

print("----------------------------------------------------------------------------------")
print(f"These are the {count(numbers)} numbers you entered: " + ", ".join(map(str, numbers)))
print(f"Their sum is {sum(numbers)}")
print(f"Their mean is {mean(numbers)}")
print(f"The list had a minimum value of {minimum(numbers)} and a maximmum of {maximum(numbers)}")
print(f"This list contained the following prime numbers: "  + ", ".join(map(str, getPrimes(numbers))))
print("----------------------------------------------------------------------------------")