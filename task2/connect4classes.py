"""
This file contains all of our classes for task2 connect 4 game
We have 4 classes, one for the game board, one for the cells of the board, and one for the players
"""

import random


"""
The Gameboard stores all cells
The cells are stored in a 2D array that goes column by column

Row by row is generally better for board games as it makes more visual sense
you start at [0, 0] in the top right, go to the end of the row and start on the next one
until you get to the bottom right corner [height, width]

Due to the nature of connect4 having a large reliance on columns
it'll make it easier to write certain functions (such as discs falling)
especially with removing discs, if the bottom of the column (index 0) is removed
then every disc above it moves down one, e.g index 1 will now be at index 0

The only downside to this is that printing out the board becomes a bit trickier
and the board in general becomes slightly harder to visualise
(worth it in my opinion to avoid spaghetti code everywhere else)

"""
class Game:

    """
    Initialise function
    Creates a blank game board with obstruction cells
    """
    def __init__(self, obstructionSizeX, obstructionSizeY):

        # Initialise our 2D grid array
        self.grid = self.generateBoard(obstructionSizeX, obstructionSizeY)

    
    def generateBoard(self, obstructionSizeX, obstructionSizeY):
        
        # Generate the starting x co-ordinate (bottom left) of our obstruction block
        obstructionX = random.randint(0, 7 - obstructionSizeX)

        # Initialise 2d array
        grid = []

        for x in range(7):
            column = []
            for y in range(6):

                # Boolean checks to see if current cell is an obstruction
                # Checks x co-ordinate is between the x co-ordinate of our obstruction + the obstructions width
                # Obstruction always starts at bottom row so we check if y co-ordinate is below the obstructions height
                obstructionXCheck = obstructionX <= x < obstructionX + obstructionSizeX
                obstructionYCheck = y < obstructionSizeY

                # If both checks pass then we know cell is an obstruction
                isObstruction = obstructionXCheck and obstructionYCheck

                # Generate cell and add it to the current column
                newCell = Cell(isObstruction)
                column.append(newCell)


            # Add generated column to our griddy
            grid.append(column)

        # return generated grid
        return grid

    """
    This function will try to place a player's disc in a given column
    We iterate through all the spaces in the column (starting at 0, the bottom of the board)
    We keep iterating until we find an empty space, at which point we change the cell to a players disc and return true
    This function will return false if it can't place a disc
    """
    def placeDisc(self, player, columnNo, isSpecialDisc):

        # Columns are labelled ingame as 1-6
        columnNo -= 1

        # Iterate through all cells in our column
        for r in range(6):
            # Assign current cell to variable
            cell = self.grid[columnNo][r]

            # Use cell function to see if it is empty
            if cell.isEmpty():

                # Set the first empty cell to the players disc
                cell.changeType(player)

                # Successfully placed disc, return true
                return True
            
        # This line of code is only reached if we failed to place disc, return false
        return False





    """
    Override string cast function to make the board game look nice when printed out
    all about those ✨ asthetics ✨
    """

    def __str__(self):
        # We initialise the string that we're going to return
        returnString = ""

        # We use these giant lines to separate rows. and \n to put them on separate lines
        returnString += "------------------------------------\n"

        #iterate through rows
        # we use reversed function because otherwise the bottom of the board (index 0) would be printed first (top)
        # while we wanted it printed last (bottom)
        for r in reversed(range(6)):
            # Inisialise a string for our row
            rowString = "|"

            #iterate through columns
            for c in range(7):
                # Add cell to row
                rowString += f" {self.grid[c][r]} |"

            # Add another row separator and a new line
            rowString += "\n------------------------------------\n"

            # Add the row to our return string
            returnString += rowString

        # return our board as a string
        return returnString

            
gameBoardIcons = {
    "e": "  ",
    "r": "🔴",
    "y": "🟡",
    "o": "⬛"
}

class Cell:
    def __init__(self, isObstruct):
        if isObstruct:
            self.type = "o"
        else:
            self.type = "e"

    def changeType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def isEmpty(self):
        return self.type == "e"

    def __str__(self):
        return gameBoardIcons[self.type]