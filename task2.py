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

Both functions will have special __str__ functions for outputting to the terminal
This is what an example board will look like (shrunk because space)

------------
| 🟥 | 🟨 |
------------
| ⬛ | 🟨 |
-----------

That's the game plan
TODO work on it tomorrow, im eepy
"""