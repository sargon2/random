When a board game is filled with go pieces, a winner is determined.

Start with a small board size, such as 2x2.

oo
oo o wins

ox
oo x is taken -- game not over

xx
oo - whoever moved last moved illegally -- game not over

xx
xx x wins

xo
ox - whoever moved last moved illegally

For board size 2x2, there are only 2 end positions.

There is only one first move.

o.
..

The second move is either next to or across.

ox  o.
..  .x

ox  oo
.o  .x

Across is better.

--

There are board states.  There are moves.  A board state plus a move is another board state.
A move can be illegal.  A move is just a color of stone plus a board position.

Each position on the board can be black, white, or empty.

A board position has a "predicted winner"?

When deciding on a move, some of your available moves will predict you winning, and some will predict the enemy winning.  How do we decide which of the winning positions to play?

Strategy: If the computer is choosing based on which move has the highest percentage chance of winning, play the moves that point it towards a loss.

3x3 is too many positions to list out here, I think.

Apparently go is only solved up to 5x6.  Wow.

Is it actually the case that there is more than one winning move to make?
