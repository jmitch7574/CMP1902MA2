"""
This file contains all of our classes for task2 connect 4 game
We have 4 classes, one for the game board, one for the cells of the board, and one for the players
"""

import random
from mathsfunctions import *

"""
The game stores all cells
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
        self.board = self.generateBoard(obstructionSizeX, obstructionSizeY)

    def getBoard(self):
        return self.board
    
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
    A function that checks if the game is full (our game end criteria)
    Iterates through every cell in the grid, returning false and breaking out
    as soon as an empty one is found (grid cannot be full)

    If the function finishes iterating, and can't find any empty cells
    then the board is full and returns True
    """
    def endGameCheck(self):
        # double for loop to iterate through 2D array
        for column in self.grid:
            for cell in column:
                # Is current cell empty?
                if cell.isEmpty():
                    # Return false and break out loop
                    return False

        # No empty cells found, grid is full, return true
        return True


    """
    Override string cast function to make the board game look nice when printed out
    all about those ✨ asthetics ✨
    """

    def __str__(self):

        separator = "\n-----------------------------\n"

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

"""
Dictionary that contians string representations of our 
different cell types
"""
gameIcons = {
    "e": " ",
    "r": "O",
    "y": "X",
    "o": "█"
}

"""
the individual cells have their own class to
just to contain some functions a cell can perform
is this at all memory efficient? no.
does it make things a tad easier to program? hell yeah
"""
class Cell:
    
    """
    Initialisation function
    if this cell is an obstruction, then change type accordingly
    store a reference to the game
    """
    def __init__(self, isObstruct, game):
        if isObstruct:
            self.type = "o"
        else:
            self.type = "e"

        self.game = game


    """
    get and set functions for the "type" attribute
    """

    def getType(self):
        return self.type

    def changeType(self, type):
        self.type = type

    """
    return true if the cell is empty
    returns false if the cell is an obstruction, or has a player disc
    """
    def isEmpty(self):
        return self.type == "e"

    """
    Deletes the cell from the column
    Due to how the grid is structured, once a cell at position x is removed
    from the column list, then the cell at position x + 1 will automatically
    now be at position x

    Columns need to maintain a specific length so once a cell is deleted
    then a new empty cell is appended (placed at the top)
    """
    def destroy(self):
        # Get cell's position
        x, y = self.getPosition()

        # OBSTRUCTIONS ARE FUCKING INVINCIBLE!!!
        if self.type == "o":
            return
        
        # remove cell and add empty cell at the top of the column
        self.game.getBoard()[x].append(Cell(False, self.game))
        self.game.getBoard()[x].remove(self)

    """
    use the gameIcons dictionary
    return string representation of cell's type
    """
    def __str__(self):
        return gameIcons[self.type]
    
    """
    get the x and y co-ordinates (as indexes) of the current cell's
    position on the game's board
    """
    def getPosition(self):
        
        # Iterate through every cell in the board until we find a match
        for x in range(7):
            for y in range(6):
                if self.game.getBoard()[x][y] == self:
                    return x, y
        
        # Code should never reeach this point
        print("This error should not occur, if you are reading this message I'm impressed")



    """
    okay this is like my third time writing this damn function


    this function runs from a given cell
    and will return 2 numbers, being the amount of points this cell
    contributes to both players scores

    (reading this now it'll only ever contribute to one players score
    so returning two numbers is kinda pointless but i can't be bothered
    rewriting this function again for a slight increase in efficiency)

    anyway back to how this function works
    it will generate 4 "combinations", stored in 4 lists
    each list will contain 4 cells which make up a "combination"
    e.g one list will contain 4 cells that are next to each other horizontally
    making up a horizontal "combination" that can award points if a player
    has a disc in all of them

    Each cell in the grid can act as the start of the following combinations:
        - horizontally (to 3 cells right)
        - vertically (to 3 cells above)
        - Diagonally (to 3 cells up and right)
        - Diagonally, again (to 3 cells down and right)

    Then we iterate through these combinations and for each combination
    we check if they all discs belonging to one player (e.g all Xs or all Os)
    and iterate a running tally for each

    once we have iterated through each combination, we return each player's
    points that this cell contributes to


    """
    def checkConnectFours(self):

        # Don't continue with the function if this cell doesn't have a disc
        # empty cells can't score ykyk
        if self.type not in ["r", "y"]: 
            return 0, 0

        # Get the cells co ordinates
        x, y = self.getPosition()

        # Initialise our running totals for each player
        player1Total = 0
        player2Total = 0

        # Initialise a list for our combinations
        combinations = []

        # We check what possible connect4s this cell can start with
        # e.g if it is impossible to make a combination 
        # (like if the 4th cell in a combination goes off the board)
        # then we don't include that combination to prevent an index out of range error
        canConnectUp = y + 3 <= 5
        canConnectRight = x + 3 <= 6
        canConnectUpRight = canConnectUp and canConnectRight
        canConnectDownRight = y - 3 >= 0 and canConnectRight

        # Initialise the lists for combinations
        upCombination = []
        rightCombination = []
        upRightCombination = []
        downRightCombination = []

        ## Add all 4 cells that make up the different connections to their respective lists
        for i in range(4):
            if canConnectUp: upCombination.append(self.game.getBoard()[x][y + i])
            if canConnectRight: rightCombination.append(self.game.getBoard()[x + i][y])
            if canConnectUpRight: upRightCombination.append(self.game.getBoard()[x + i][y + i])
            if canConnectDownRight: downRightCombination.append(self.game.getBoard()[x + i][y - i])

        # Add all our combinations to our combination array
        if canConnectUp: combinations.append(upCombination)
        if canConnectRight: combinations.append(rightCombination)
        if canConnectUpRight: combinations.append(upRightCombination)
        if canConnectDownRight: combinations.append(downRightCombination)

        # Iterate through our combination
        for combination in combinations:
            # If the cells in the combination match
            if combination[0].getType() == combination[1].getType() == combination[2].getType() == combination[3].getType():
                if combination[0].getType() == "r":
                    player1Total += 1
                if combination[0].getType() == "y":
                    player2Total += 1

        return player1Total, player2Total
    

class Player:
    def __init__(self, playerNum):
        self.playerNum = playerNum
        self.playerType = "r" if playerNum == 1 else "y"
        self.score = 0
        self.hasSpecialDisc = True

    def getScore(self):
        return self.score
    
    def setScore(self, score : int):
        self.score = score
    
    def getPlayerNum(self):
        return self.playerNum
    
    def getPlayerType(self):
        return self.playerType
    
    def hasSpecialDisc(self):
        return self.hasSpecialDisc
    
    def setSpecialDisk(self, value : bool):
        self.hasSpecialDisc = value
