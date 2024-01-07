
# Import our classes for our game and other wacky libraries
from connect4classes import *
from inputfunctions import *

"""
This function contains all process that create an entire game of connect 4
everything from asking the user for game settings to outputting the winner when the games over
"""
def PlayGame():
    print("========================================")

    # Initialise turn count
    turns = 0

    # Initialise Player Variables
    playerOne = Player(1)
    playerTwo = Player(2)

    # Boolean variable, Game continues while true, game ends when false
    playing = True

    # Get our game settings
    obstructionSizeX, obstructionSizeY, discsForConnection = GameSettings()

    # Generate our game board
    board = Game(obstructionSizeX, obstructionSizeY, discsForConnection)

    # a loop to keep asking players for turns until the game ends
    while playing:

        # End the game if the board is full
        if board.endGameCheck():
            playing = False
            continue

        # reference to the current player's variable
        # Player one goes on even turns
        currentPlayer = playerOne if turns % 2 == 0 else playerTwo

        # Output board and score
        print(board)
        print(f"\n Player 1 Score: {playerOne.score}\n Player 2 Score: {playerTwo.score}")

        # Special function in inputfunctons.py for inputting player actions
        # Returns false if invalid input
        # Returns a tuple containing action type and column number if valid
        playerAction = inputAction(currentPlayer)

        # Did we get a valid input
        if playerAction:
            
            # Split our returned value into the action type and the column number
            actionType, columnNo = playerAction

            # Placing a disc
            if actionType == "p":
                board.placeDisc(currentPlayer.type, columnNo-1, False)
            
            # Placing a special disc
            if actionType == "s":
                if currentPlayer.hasSpecialDisc:
                    board.placeDisc(currentPlayer.type, columnNo-1, True)
                    currentPlayer.hasSpecialDisc = False
                else:
                    print("You have already used your special disk, skipping turn")
                    # 3 second break between turns to player can read outputs
                    time.sleep(3) 

            if actionType == "r":
                success = board.tryRemoveDisc(currentPlayer.type, columnNo)

                if not success:
                    print("Failed to remove disc (either no disc is present or is opponents disc)")
                    print("Skipping turn...")
                    time.sleep(3)

                
        else:
            # 3 second break between turns to player can read outputs
            time.sleep(3)   

        # incriment turns
        turns += 1

        # Update player scores
        playerOne.score, playerTwo.score = board.checkScores()

    # Final outputs, board, scores and who wins
    print(board)
    print("{:=^30}".format("GAME OVER"))
    print("{: ^30}".format("Player 1 Score: " + str(playerOne.score)))
    print("{: ^30}".format("Player 2 Score: " + str(playerTwo.score)))

    if playerOne.score == playerTwo.score:
        print("{:=^30}".format("Tie"))
    elif playerOne.score > playerTwo.score:
        print("{:=^30}".format("Player One Wins"))
    else:
        print("{:=^30}".format("Player Two Wins"))

"""
Input all the game settings
"""
def GameSettings():
    obstructionSizeX = inputInteger("Please enter the width of the obstruction: ", min=0, max=7)
    obstructionSizeY = inputInteger("Please enter the height of the obstruction: ", min=0, max=6)
    discsForConnection = inputInteger("Please enter how many discs in a row form a connection (minimum 2): ", min=2, max=7)

    return obstructionSizeX, obstructionSizeY, discsForConnection

"""
Main function
"""
if __name__== "__main__":
    Playing = True

    
    ## Tutorial for the game because i realised the rules aren't explained anywhere but in my comments lol
    ## Tutorials here because it only needs seeing once
    print("=======Tutorial========")
    print("Each turn the player must make action")
    print("An action consists of a type, and a column number")
    print("The types are:")
    print("- p to place a disc")
    print("- s to place a special disc that destroys all nearby tiles (except obstructions)")
    print("- r to remove the bottom disc from a column (if it is yours)")
    print("e.g to place a disc in the 3rd column would be p3")
    print("failure to make a valid input within 5 seconds will result in your turn being skipped")
    print(f"Points are scored by connecting discs together in a straight line")
    print("The game ends when the board if full, whoever has the most points wins")
    print("Press enter to begin...")
    input()

    # Gameloop
    while Playing:
        PlayGame()

        Playing = inputYesNo("Would you like to play again? ")