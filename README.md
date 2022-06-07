# Game-AI
developing an AI game player for a modified version of the game called Teeko. We call this modified version Teeko2.


## How to play Teeko
![image](https://user-images.githubusercontent.com/54726422/172276153-190ea11c-21a9-4ae4-811e-c348e9455bef.png)

It is a game between two players on a 5x5 board. Each player has four markers of either red or black. Beginning with black, they take turns placing markers (the "drop phase") until all markers are on the board, with the goal of getting four in a row horizontally, vertically, or diagonally, or in a 2x2 box as shown above. If after the drop phase neither player has won, they continue taking turns moving one marker at a time -- to an adjacent space only! (Note this includes diagonals, not just left, right, up, and down one space.) -- until one player wins.

## How to play Teeko2
The Teeko2 rules are almost identical to those of Teeko but we will exchange a rule. Specifically, we remove the 2x2 box winning condition and replace it with a 3x3 box winning condition -- same colored markers at the four corners of a 3x3 square. Mathematically, if (i,j) is the center of a 3x3 board, then it must be that (i,j) is empty and that there is a marker of the appropriate color on each of (i-1,j-1), (i-1,j+1), (i+1,j-1), and (i+1,j+1). 

## Win conditions summarized for Teeko2:
Four same colored markers in a row horizontally, vertically, or diagonally.
Four same colored markers at the corners of a 3x3 square.

## Program Specification
1. The make_move(self, state) method begins with the current state of the board. It is up to you to generate the subtree of depth d under this state, create a heuristic scoring function to evaluate the "leaves" at depth d (as you may not make it all the way to a terminal state by depth d so these may still be internal nodes) and propagate those scores back up to the current state, and select and return the best possible next move using the minimax algorithm.
2. Define a successor function (e.g. succ(self, state) ) that takes in a board state and returns a list of the legal successors. During the drop phase, this simply means adding a new piece of the current player's type to the board; during continued gameplay, this means moving any one of the current player's pieces to an unoccupied location on the board, adjacent to that piece. Note: wrapping around the edge is NOT allowed when determining "adjacent" positions.
3. Using game_value(self, state) as a starting point, create a function to score each of the successor states. A terminal state where your AI player wins should have the maximal positive score (1), and a terminal state where the opponent wins should have the minimal negative score (-1).
4. Define a max_value(self, state, depth) function where your first call will be  max_value(self, curr_state, 0) and every subsequent recursive call will increase the value of depth.
