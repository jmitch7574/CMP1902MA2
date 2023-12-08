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
These functions are all about finding any prime numbers in a given list of integers
One function finds all the factors of a number and returns them as a list
The other function will check if this list of factors only contains one and itself
The prime function will return True or False

You can write this as just one function that checks for factors and return false as soon
as you find a factor that isn't 1 or itself (would be slightly more efficient). But you 
never know when having a factors function might come in handy.
"""


"""
The factors function loops through all numbers between 1 and our given number
It uses the modal function to check if our iterated number is a factor of our given number
If the result of the modal operation is 0 we know it is a factor of our given number
We then add this number to a list of factors
"""

def getFactors(number):

    # Initialise factors list
    factors = []

    # loop through all numbers between 1 and our given number
    for i in range(1, number + 1):
        # Check if divisible
        if number % i == 0:
            # Add to the list of factors if divisible
            factors.append(i)
    
    # Return our list of factors
    return factors

"""
This function uses the getFactors function above and just checks if the only factors
are 1 and itself
"""
def isPrime(number):
    # We use a shorthand if statement to check if factors of a number are 1 and itself, return true or false
    return True if getFactors(number) == [1, number] else False


"""
This function takes a list of numbers
Iterates through the numbers
Adds any prime numbers it finds to a list
Returns the list
"""

def getPrimes(list):
    # Initialise list to hold prime numbers
    primes = []

    # Iterate through numbers in our list
    for i in list:
        # Use our isPrime function to check if number is prime
        if isPrime(i):
            # add number to list if prime
            primes.append(i)

    # return prime numbers
    return primes

