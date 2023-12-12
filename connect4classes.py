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
        
        return player1Score / 4, player2Score / 4


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
    This function will check for all possible connect4s this cell can make
    We check verticals, horizontals and diagonals separately

    For each direction this cell will:
        - The cell will generate 4 sets of 4 cells
        - These are all possible combinations of a connect4 in the given direction
        - We go through each set of cells and check if they all match a players color


    We use min and max functions to ensure that the cell doesn't check for cells outside
    """
    def checkConnectFours(self):
        x, y = self.getPosition()

        player1Total = 0
        player2Total = 0

        combinations = []

        ## Horizontal Checks
        for i in range(4):
            if x - i >= 0 and x - i + 3 <= 6:
                combinationCells = []
                for j in range(4):
                    combinationCells.append(self.gameBoard.grid[x - i + j][ y])
                combinations.append(combinationCells)

        ## Vertical Checks
        for i in range(4):
            if y - i >= 0 and y - i + 3 <= 5:
                combinationCells = []
                for j in range(4):
                    combinationCells.append(self.gameBoard.grid[x][ y - i + j])
                combinations.append(combinationCells)

        # Diagonal Checks - 1
        for i in range(4):
            if (x - i >= 0 and x - i + 3 <= 6) and (y - i >= 0 and y - i + 3 <= 5):
                combinationCells = []
                for j in range(4):
                    combinationCells.append(self.gameBoard.grid[x - i + j][y - i + j])
                combinations.append(combinationCells)
        
        
        # Diagonal Checks - 2
        for i in range(4):
            if (x - i >= 0 and x - i + 3 <= 6) and (y - i >= 0 and y - i + 3 <= 5):
                combinationCells = []
                for j in range(4):
                    k = 3 - j
                    print(str(x-i+j) + " " + str(y-i+k))
                    combinationCells.append(self.gameBoard.grid[x - i + j][y - i + k])

                combinations.append(combinationCells)
    
        for combination in combinations:
            # If the cells in the combination match
            if combination[0].getType() == combination[1].getType() == combination[2].getType() == combination[3].getType():
                if combination[0].getType() == "r":
                    player1Total += 1
                if combination[0].getType() == "y":
                    player2Total += 1

        return player1Total, player2Total