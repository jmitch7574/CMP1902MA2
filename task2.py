
# Import our classes for our game and other wacky libraries
from connect4classes import *
from inputfunctions import *


"""
Main function
"""
if __name__== "__main__":
    playingGames = True

    
    ## Tutorial for the game because i realised the rules aren't explained anywhere but in my comments lol
    ## Tutorials here because it only needs seeing once
    print("=======Tutorial========")
    print("Each turn the player must make action")
    print("An action consists of a type, and a column number")
    print("The types are:")
    print("    - p to place a disc")
    print("    - s to place a special disc that destroys all nearby tiles (except obstructions)")
    print("    - r to remove the bottom disc from a column (if it is yours)")
    print("e.g to place a disc in the 3rd column would be p3")
    print("failure to make a valid input within 5 seconds will result in your turn being skipped")
    print(f"Points are scored by connecting discs together in a straight line")
    print("The game ends when the board if full, whoever has the most points wins")
    print("Press enter to begin...")
    input()

    # Gameloop
    while playingGames:
        Game()

        playingGames = inputYesNo("Would you like to play again? ")

    print("Thank you for playing!")