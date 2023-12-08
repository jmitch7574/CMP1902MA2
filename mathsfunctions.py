"""
This file contains our maths functions, separated for cleanliness of code
and so that the main function of task1.py isn't bloated with math functions

This file will be imported in our task1.py file
"""


"""
Custom function for finding the length of a list
Iterates through the list incrim
"""
def count(list):
    # Initialise count at 0
    count = 0

    # Iterate through items in the list
    for i in list:
        # Incriment our total for each item in list
        count+=1

    # return our count
    return count

"""
Custom function for finding the sum of numbers in a list
Iterates through the list and adds values to a running total
"""
def sum(list):
    # initialise sum at 0
    sum = 0

    # iterate through our list
    for i in list:
        # add the value of i to our running sum
        sum += i

    # return sum
    return sum


"""
Custom function for finding the mean of integers in a list
Easily accomplished using our super cool sum() and count() functions from above
"""
def mean(list):
    # return the total(sum) of our list divided by amount of numbers in the list
    return sum(list) / count(list)


"""
Custom function for finding the minumum value in a list of ints
We start by storing the first number in a variable
Then iterating through the remaining numbers and checking if one is lower
"""
def minimum(list):
    # Check if list has at least 1 value, else return None
    if count(list) == []:
        return None
    
    # Continue with function if there is at least one item

    # Initialise our minimum with the first value in the list
    minimum = list[0]

    # iterate through the list
    for i in list:
        # if current item is lower than our current minimum
        if i < minimum:
            # item becomes our new minimum
            minimum = i

    # return our minimum
    return minimum



"""
Custom function for finding the maximum value in a list of ints
We start by storing the first number in a variable
Then iterating through the remaining numbers and checking if one is larger
"""
def maximum(list):
    # Check if list has at least 1 value, else return None
    if count(list) == []:
        return None
    
    # Continue with function if there is at least one item

    # Initialise our minimum with the first value in the list
    maximum = list[0]

    # iterate through the list
    for i in list:
        # if current item is larger than our
        #  current minimum
        if i > maximum:
            # item becomes our new minimum
            maximum = i

    # return our minimum
    return maximum



"""
These Functions  are a
"""