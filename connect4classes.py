"""
This file contains all of our classes for task2 connect 4 game
We have 4 classes, one for the game board, one for the cells of the board, and one for the players
"""

import random
from mathsfunctions import *
from inputfunctions import *
import time

"""
The game class stores the game board and all functions to do with modifying the game board
The cells are stored in a 2D array that goes column by column

Game is stored as column by column, makes it easier to manage columns 
only downside is voodoo magic is required to print board
"""

class Game:

    """
    Initialise function
    Creates a blank game board with obstruction cells
    """
    def __init__(self):
        
        # Get our game settings
        obstructionSizeX, obstructionSizeY, discsForConnection = self.GameSettings()

        # Initialise our 2D grid array
        self.board = self.generateBoard(obstructionSizeX, obstructionSizeY)
        self.discsForConnection = discsForConnection
        
        
        print("========================================")

        # Initialise turn count
        self.turns = 0

        # Initialise Player Variables
        self.playerOne = Player(1)
        self.playerTwo = Player(2)

        # Boolean variable, Game continues while true, game ends when false
        self.playing = True

        # a loop to keep asking players for turns until the game ends
        while self.playing:
            self.turn()

        self.gameOver()
    
    
    """
    Input all the game settings
    """
    def GameSettings(self):
        obstructionSizeX = inputInteger("Please enter the width of the obstruction: ", min=0, max=7)
        obstructionSizeY = inputInteger("Please enter the height of the obstruction: ", min=0, max=6)
        discsForConnection = inputInteger("Please enter how many discs in a row form a connection (minimum 2): ", min=2, max=7)

        return obstructionSizeX, obstructionSizeY, discsForConnection

    """
    Function for a given turn
    Plays the current players action and updates scores
    """
    def turn(self):
        # End the game if the board is full
        if self.endGameCheck():
            self.playing = False
            return

        # reference to the current player's variable
        # Player one goes on even turns
        currentPlayer = self.playerOne if self.turns % 2 == 0 else self.playerTwo

        # Output board and score
        print(self)
        print(f"\n Player 1 Score: {self.playerOne.score}\n Player 2 Score: {self.playerTwo.score}")

        currentPlayer.playTurn(self)

        # incriment turns
        self.turns += 1

        # Update player scores
        self.playerOne.score, self.playerTwo.score = self.checkScores()

    """
    Game over function
    Output player scores and who won
    """
    def gameOver(self):
        # Final outputs, board, scores and who wins
        print(self)
        print("{:=^30}".format("GAME OVER"))
        print("{: ^30}".format("Player 1 Score: " + str(self.playerOne.score)))
        print("{: ^30}".format("Player 2 Score: " + str(self.playerTwo.score)))

        if self.playerOne.score == self.playerTwo.score:
            print("{:=^30}".format("Tie"))
        elif self.playerOne.score > self.playerTwo.score:
            print("{:=^30}".format("Player One Wins"))
        else:
            print("{:=^30}".format("Player Two Wins"))

    
    def generateBoard(self, obstructionSizeX, obstructionSizeY):
        
        # Generate the starting x co-ordinate (bottom left) of our obstruction block
        obstructionX = random.randint(0, 7 - obstructionSizeX)

        # Initialise 2d array
        grid = []

        # 7 Columns
        for x in range(7):

            # Initialise Empty column
            column = []

            # 6 Cells per column (rows)
            for y in range(6):
                # Check if this cell should be an obstruction
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
        # Iterate through all cells in our column
        for r in range(6):
            # Assign current cell to variable
            cell = self.board[columnNo][r]

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

                            
                            self.board[columnNo + x][r + y].destroy()
                else:
                    # Set the first empty cell to the players disc
                    cell.type = player

                    # Successfully placed disc, return true
                    return True
            
        # This line of code is only reached if we failed to place disc, return false
        # time.sleep so the player has time to understand the consequences of their actions
        print("Column is full, skipping turn")
        time.sleep(3)
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
                player1CellScore, player2CellScore = self.board[x][y].checkConnections()
                player1Score += player1CellScore
                player2Score += player2CellScore
        
        return player1Score, player2Score


    """
    A function that checks if the game is full (our game end criteria)
    Iterates through every cell in the grid, if cell is empty then we return false and stop
    Return true if we finish iterating without finding empty cell
    """
    def endGameCheck(self):
        # double for loop to iterate through 2D array
        for column in self.board:
            for cell in column:
                # Is current cell empty?
                if cell.isEmpty():
                    # Return false and break out loop
                    return False

        # No empty cells found, grid is full, return true
        return True

    """
    Function that allows a player to remove the bottom disc from a column 
    only if said disc belongs to them
    returns True if successful, false if failure
    """
    def tryRemoveDisc(self, playerType, columnNo):
        # Get selected cell
        cell = self.board[columnNo][0]

        # Is it one of the players discs
        if cell.type == playerType:
            # remmove cell and return true (success)
            cell.destroy()
            return True
        # Cell isn't one of the players discs, return False (failure)
        else:
            return False

    """
    Function for getting a cell
    take a tuple argument including x and y
    """
    def getCell(self, coord):
        return self.board[coord[0]][coord[1]]

    """
    Override string cast function to make the board game look nice when printed out
    all about those ✨ asthetics ✨
    """

    def __str__(self):

        separator = "\n+---+---+---+---+---+---+---+\n"

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
                rowString += f" {self.board[c][r]} |"

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
the individual cells have their own class too
just to contain some functions a cell can perform
is this at all memory efficient? no.
does it make things a tad easier to program? hell yeah
"""
class Cell:
    
    """
    Initialisation function
    """
    def __init__(self, isObstruct, game):
        if isObstruct:
            self.type = "o"
        else:
            self.type = "e"

        self.game = game

    """
    return true if the cell is empty, else false
    """
    def isEmpty(self):
        return self.type == "e"

    """
    Deletes the cell from the column
    All cells above fall down one index
    Adds empty cell to top of column
    """
    def destroy(self):
        # Get cell's position
        x, y = self.getPosition()

        # Obstructions can't be destroyed
        if self.type == "o":
            return
        
        # remove cell and add empty cell at the top of the column
        self.game.board[x].append(Cell(False, self.game))
        self.game.board[x].remove(self)

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
                if self.game.board[x][y] == self:
                    return x, y
        
        # Code should never reeach this point
        print("This error should not occur, if you are reading this message I'm impressed")



    """
    This function runs from a cell and checks all possible combinations that can be made with this cell as the first one
    Each disc can be the start of 4 possible combinations, up, right, up right and down right
    (down and left aren't needed because tokens down to the left will be checking right and up as well)
    iterate through these combinations and see if any of them all belong to the same player, iterate players score
    """
    def checkConnections(self):

        # Don't continue with the function if this cell doesn't have a disc
        # empty cells can't score ykyk
        if self.type not in ["r", "y"]: 
            return 0, 0
        
        discsForConnection = self.game.discsForConnection

        # Get the cells co ordinates
        x, y = self.getPosition()

        # Initialise our running totals for each player
        player1Total = 0
        player2Total = 0

        # Initialise a list for our combinations
        combinations = [[], [], [], []]

        ## Add all 4 cells that make up the different connections to their respective lists
        for i in range(discsForConnection):
            combinations[0].append([x, y + i])      # Up (incriment y)
            combinations[1].append([x + i, y])      # Right (incriment x)
            combinations[2].append([x + i, y + i])  # Up Right (incriment x and y)
            combinations[3].append([x + i, y - i])  # Down Right (incriment x and decrement y)

        # Iterate through our combination
        for combination in combinations:
            # If the cells in the combination match
            if self.doCellsMatch(combination):
                if self.game.getCell(combination[0]).type == "r":
                    player1Total += 1
                if self.game.getCell(combination[0]).type == "y":
                    player2Total += 1

        return player1Total, player2Total
    
    def doCellsMatch(self, combination):
        typeMatch = self.game.getCell(combination[0]).type

        for cell in combination:
            if not(0 <= cell[0] < 7 and 0 <= cell[1] < 6):
                return False

            if self.game.getCell(cell).type != typeMatch:
                return False
        return True


"""
Class to hold all player attributes
"""
class Player:
    def __init__(self, playerNum):
        self.num = playerNum
        self.type = "r" if playerNum == 1 else "y"
        self.score = 0
        self.hasSpecialDisc = True

    def playTurn(self, board):

        # Special function in inputfunctons.py for inputting player actions
        # Returns false if invalid input
        # Returns a tuple containing action type and column number if valid
        playerAction = self.playerAction()

        # Did we get a valid input
        if playerAction:
            
            # Split our returned value into the action type and the column number
            actionType, columnNo = playerAction

            # Placing a disc
            if actionType == "p":
                board.placeDisc(self.type, columnNo-1, False)
            
            # Placing a special disc
            if actionType == "s":
                if self.hasSpecialDisc:
                    board.placeDisc(self.type, columnNo-1, True)
                    self.hasSpecialDisc = False
                else:
                    print("You have already used your special disk, skipping turn")
                    # 3 second break between turns to player can read outputs
                    time.sleep(3)
                    return

            if actionType == "r":
                success = board.tryRemoveDisc(self.type, columnNo)

                if not success:
                    print("Failed to remove disc (either no disc is present or is opponents disc)")
                    print("Skipping turn...")
                    time.sleep(3)
                    return

                
        else:
            # 3 second break between turns to player can read outputs
            time.sleep(3)   
            return
    
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
    def playerAction(self):
        
        # Make a record of  the current timestamp of when the player was asked for input
        startTime = time.time() 

        # Ask the player for input
        playerInput = input(f"Please enter your action, Player {self.num}:").lower()

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

        # Subtract start time from current time to find time taken
        # Skip turn if player took more than 5 seconds
        if time.time() - startTime > 5:
            print("Action must be inputted within five seconds, skipping turn")
            return False

        # Return both action and collumn
        return (action, column)