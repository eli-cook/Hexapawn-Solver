# CS442P Assignment 2: Hexapawn Solver

Name: Eli Cook

Email: elcook@pdx.edu

> The purpose of this assignment was to develop a solver given an arbitrary board position of the game Hexapawn.
> This game uses a board with a set number of rows and columns and each side (black and white) have a set of pawns
> equal to the number of columns on the board. These pawns have the same basic moveset as they do in chess. You can
> win by one of the following methods: Get a pawn to the other edge of the board (win by promotion) or force the
> board into a situation where your opponent cannot move.

> This solver will determine who wins given perfect play. The pseudo code for the basic algorithm is shown below.

```
board_value(board)
  // takes in a board that contains information about the board's state and outputs a -1 or 1, where
  // a -1 represents a loss for the current player's turn, and a 1 for a win by the current player.
  
    moves <- legal moves in board
    if moves is empty
        return -1
    max_val = -1
    for m in moves
        result <- m(board)
        if result is win
            val <- 1
        else
            val <- - board_value(board)
        undo previous move
        max_val <- max of max_val, val
        
        if max_val == 1
          break out of for loop
        
    return max_val
```

> This algorithm is directly from the psuedo code discussed in class with a few optimizations. These optimizations
> are Win-Pruning, and Do-Undo. This program was implemented using Python mainly for my own benefit and for its
> simplicity in implementation. My implementation uses a board object to hold all the information necessary for
> a given state of the game. This includes, the board (a m x n grid of chars), whose turn, as well as some
> helper functions. The most important of these is the check_place function that is used to check legal moves for
> a given square by checking the legal moves for a piece and confirming they are valid moves. I wrote a
> legal_moves function that calls this helper function for each square on the board and gathers a list of valid
> "moves" to perform at each recursive step.

# Usage

>The tests are include in the test/positions/ directory.
> You must have Python3 or PyPy installed.
> The program can be run using the following commands

```sh
$ pypy hexapawn.py < tests/positions/3x3-1.in
```

> Thanks to Kevin Midkiff for contributing his ideas and brainstorming during the architecture and debugging of 
> this program.
