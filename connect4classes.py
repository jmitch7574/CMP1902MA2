"""
This file contains all of our classes for task2 connect 4 game
We have 4 classes, one for the game board, one for the cells of the board, and one for the players
"""

import random
from mathsfunctions import *

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
                newCell = Cell(isObstruction, self)
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
                
                # If the disk placed is our super special bye bye destructo disc 
                if isSpecialDisc:
                    # Iterate throgh a 3x3 area deleting all cells
                    for x in range(-1, 2):
                        # It is important we delete from top down using reverse
                        # Because as soon as we destroy a disc the ones above will fall down instantly
                        # Causing us to delete incorrect cells
                        for y in reversed(range(-1, 2)):
                            cellX = columnNo + x
                            cellY = r + y
                            # If the cell to delete isn't on the board, do nothing
                            if cellX < 0  or cellX > 6 or cellY < 0 or cellY > 5:
                                continue

                            
                            self.grid[columnNo + x][r + y].destroy()



                else:
                    # Set the first empty cell to the players disc
                    cell.changeType(player)

                    # Successfully placed disc, return true
                    return True
            
        # This line of code is only reached if we failed to place disc, return false
        return False


    """
    This function will run through each cell and check to see if it is part of a connect4
    We run through each cell, each cell will check if all possible connect4s that can be made which include it
    We tally up all the connect4s the cells come back with and divide it by 4 (or how many discs make up a connect4)
    """
    def checkScores(self):
        player1Score = 0
        player2Score = 0

        for x in range(7):
            for y in range(6):
                player1CellScore, player2CellScore = self.grid[x][y].checkConnectFours()
                player1Score += player1CellScore
                player2Score += player2CellScore
        
        return player1Score, player2Score


    """
    Override string cast function to make the board game look nice when printed out
    all about those ✨ asthetics ✨
    """

    def __str__(self):

        separator = "\n------------------------------------\n"

        # We initialise the string that we're going to return
        returnString = "\n"

        # Column Headings to our output
        returnString += "  1   2   3   4   5   6   7"

        # We use these giant lines to separate rows. and \n to put them on separate lines
        returnString += separator
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
            rowString += separator

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
    def __init__(self, isObstruct, gameBoard):
        if isObstruct:
            self.type = "o"
        else:
            self.type = "e"

        self.gameBoard = gameBoard

    def changeType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def isEmpty(self):
        return self.type == "e"

    def destroy(self):
        x, y = self.getPosition()


        # OBSTRUCTIONS ARE FUCKING INVINCIBLE!!!
        if self.type == "o":
            return
        
        self.gameBoard.grid[x].append(Cell(False, self.gameBoard))
        self.gameBoard.grid[x].remove(self)

    def __str__(self):
        return gameBoardIcons[self.type]
    
    def getPosition(self):
        
        # Iterate through every cell in the board until we find a match
        for x in range(7):
            for y in range(6):
                if self.gameBoard.grid[x][y] == self:
                    return x, y
        
        # Code should never reeach this point
        print("This error should not occur, if you are reading this message I'm impressed")

    """
    This function will take a given cell and check if it can make a connect4 in the following directions:
        - Up
        - Right
        - Diagonal Up and Right
        - Diagonal Down and Right

    First it checks if it has a disc in it, there's no point running the rest of the script if its never gonna come up with anyhting
    that's just wasing precious computing power which could be used for playing fortnite
    
    In each direction it will
    - Check if there are 4 cells in that direction to check (e.g a disc at the top of the board won't be able to make a connect4 upwards)
    - If there are 4 cells, then it will add up all these cells into a list 
    - This list is essentially a combination of all cells that make up a possible connect4
    - All of these combinations all get added into a second list
    - All combinations in this list will get iterated through and for each combinmation:
        - We check if all cells are the same type (e.g all red, all yellow)
        - If they are all red we incriment player1's score
        - If they are yellow we incriment player2's score

    We use min and max functions to ensure that the cell doesn't check for cells outside
    """
    def checkConnectFours(self):

        # Don't continue with the function if this cell doesn't have a disc
        if self.type not in ["r", "y"]: 
            return 0, 0

        x, y = self.getPosition()

        player1Total = 0
        player2Total = 0

        combinations = []

        ### We check what possible connect4s this cell can start with
        canConnectUp = y + 3 <= 5
        canConnectRight = x + 3 <= 6
        canConnectUpRight = canConnectUp and canConnectRight
        canConnectDownRight = y - 3 >= 0 and canConnectRight

        upCombination = []
        rightCombination = []
        upRightCombination = []
        downRightCombination = []

        ## Add all 4 cells that make up the different connections to their respective lists
        for i in range(4):
            if canConnectUp: upCombination.append(self.gameBoard.grid[x][y + i])
            if canConnectRight: rightCombination.append(self.gameBoard.grid[x + i][y])
            if canConnectUpRight: upRightCombination.append(self.gameBoard.grid[x + i][y + i])
            if canConnectDownRight: downRightCombination.append(self.gameBoard.grid[x + i][y - i])

        
        if canConnectUp: combinations.append(upCombination)
        if canConnectRight: combinations.append(rightCombination)
        if canConnectUpRight: combinations.append(upRightCombination)
        if canConnectDownRight: combinations.append(downRightCombination)

    
        for combination in combinations:
            # If the cells in the combination match
            if combination[0].getType() == combination[1].getType() == combination[2].getType() == combination[3].getType():
                if combination[0].getType() == "r":
                    player1Total += 1
                if combination[0].getType() == "y":
                    player2Total += 1

        return player1Total, player2Total