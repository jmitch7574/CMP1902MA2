"""
Ok game plan for how this is gonna work
This program is for a ⭐ special variant ⭐ of connect 4

It includes the basic rules for a connect 4 game
- 6 rows, 7 columns
- two players, red and yellow
- Players place a token down in a column and it drops to the lowest empty space
- the objective is to connect four tokens of your colour horizontally, vertically or diagonally

With a few added special rules:
- The game does not end when a connect 4 is made, instead the player is awarded a point
- The amount of points will change dynamically with the board (elaborated in later points)
- The game instead terminates when the board is completely filled
- At the start of the game, randomly generate a 2 row, 3 column block of cells, which obstruct tokens
- Each player has 5 seconds to make a move. If a move is not performed, the turn is lost
    - this will be difficult to accomplish in real time without threading
    - Could wait until the user has inputted something, and if its been over 5 seconds we can ignore their input
- Each player has a special disc that can be played once per game, when played, will remove all adjacent tokens (apart from obstruction cells)

Advanced functionality:
- During each turn, a player can also remove one of their own discs from the bottom row 
    - idk how this can be implemented in a fair way at this point, as players could theoretically stall a game forever
    - An idea might be to require a player to decide between adding a token or removing one, but that can still be abused
    - Maybe a defecit can be added, i.e each time you remove a token will subtract from your final score
    - Hell you could keep this defecit hidden until the end of the game to add an extra layer of strategy
    - A game of sacrifice, spend one point to make your opponents lose multiple points
    - That or just put a limit on it, easier to implement but also boring
    - TODO decide on this please
- Before the game starts the player should be able to decide on 2 settings
    - How many discs forms a "connection"
    - How large the obstruction block will be


As for how this should be done?
- A class for the actual game board
    - will have functions for generating the obstruction cells, placing a token etc.
    - will perform checks for connections (god knows how im gonna do that)
    - Cells will be stored in a 2D array that stores row values in columns
- Cells will be their own class 
    - With 4 different states, Blank, Red, Yellow, Obstruction
    - Functions for changing states
    - aaand maybe functions for checking connect-4s (depends on which class it goes better in, who knows maybe both)
- Most likely a class for a player as well
    - Contains the players score, whether or not they have their special disc
    
Both functions will have special __str__ functions for outputting to the terminal
This is what an example board will look like (shrunk because space)

------------
| 🟥 | 🟨 |
------------
| ⬛ | 🟨 |
-----------

UPDATE 19/12/23
ok so like i've got most of this done (bar removing discs and the game actually finishing lol)
anyway so the game isn't gonna use emojis for the icons anymore because cmd doesn't like it
anyway so now obstructions are █, player 1 is now O, and player 2 is now X

"""

# Import our classes for our game and other wacky libraries
from connect4classes import *
from inputfunctions import *

def PlayGame():

    # Boolean variable, Player 1's turn when True, Player 2's turn when False
    playerOneTurn = True

    # Initialise Player Variables
    playerOne = Player(1)
    playerTwo = Player(2)

    # Boolean variable, Game continues while true, game ends when false
    playing = True

    obstructionSizeX, obstructionSizeY, discsForConnection = GameSettings()

    board = Game(obstructionSizeX, obstructionSizeY, discsForConnection)

    while playing:

        currentPlayer = playerOne if playerOneTurn else playerTwo

        print(board)
        print(f"\n Player 1 Score: {playerOne.getScore()}\n Player 2 Score: {playerTwo.getScore()}")
        playerAction = inputAction(currentPlayer)

        if playerAction:

            if playerAction[0] == "p":
                board.placeDisc(currentPlayer.getType(), playerAction[1]-1, False)
            
            if playerAction[0] == "s":
                if currentPlayer.hasSpecialDisc():
                    board.placeDisc(currentPlayer.getType(), playerAction[1]-1, True)
                    currentPlayer.setSpecialDisk(False)
                else:
                    print("You have already used your special disk, skipping turn")
                    # 3 second break between turns to player can read outputs
                    time.sleep(3) 
                    
            
            if playerAction[0] == "r":
                success = board.tryRemoveDisc(currentPlayer.getType(), playerAction[1]-1)

                if not success:
                    print("Failed to remove disc (either no disc is present or is opponents disc)")
                    print("Skipping turn...")
                    time.sleep(3)

                
        else:
            # 3 second break between turns to player can read outputs
            time.sleep(3)   

        # Invert our player boolean, switching which player turn it is
        playerOneTurn = not playerOneTurn

        player1Score, player2Score = board.checkScores()
        playerOne.setScore(player1Score)
        playerTwo.setScore(player2Score)

        if board.endGameCheck():
            playing = False

    print(board)
    print("{:=^30}".format("GAME OVER"))
    print("{: ^30}".format("Player 1 Score: " + str(playerOne.getScore())))
    print("{: ^30}".format("Player 2 Score: " + str(playerTwo.getScore())))

    if playerOne.getScore() == playerTwo.getScore():
        print("Tie")
    elif playerOne.getScore() > playerTwo.getScore():
        print("Player One Wins")
    else:
        print("Player Two Wins")

def GameSettings():
    obstructionSizeX = inputInteger("Please enter the width of the obstruction: ", min=0, max=7)
    obstructionSizeY = inputInteger("Please enter the height of the obstruction: ", min=0, max=6)
    discsForConnection = inputInteger("Please enter how many discs in a row form a connection (minimum 2): ", min=2, max=7)

    return obstructionSizeX, obstructionSizeY, discsForConnection


if __name__== "__main__":
    Playing = True

    while Playing:
        PlayGame()

        Playing = inputYesNo("Would you like to play again?")

