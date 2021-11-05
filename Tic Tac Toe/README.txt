DESCRIPTION:

My program implements a generalized version of Tic-Tac-Toe, using
four algorithms each with minor modification(improvement) than the previous.
Algorithms: -
1. Basic Minimax Algorithm
2. Depth Limited Algorihm
3. Alpha Beta Pruning
4. Alpha Beta with depth Limited Algorithm


INSTALLATION:

This code is built with a python GUI, PyGame. 
So to run this, first you need to install Pygame in your systems.

Run the following command in your terminal - 
$ pip install pygame
To check whether you have correctly installed pygame run this - 
$ pip show pygame

HOW TO RUN:

$ cd S20180010170
To run the basic tictactoe -
$ python tictactoe.py

To run open field tictactoe -
For this make a minor modification in the code, i.e, 
change self.gridsize=3 to self.gridsize=n

$ python extendedtictactoe.py 

The program first asks you to chose the game. After you choose the game 
you are supposed to choose whether you play first or the opponent(computer).
Then you need to select any one of the algorithm which is used by the game playing agent.
Symbols -
Player: X
Computer: O

There are two videos attached in this folder.
One playing basic tictactoe and the other open filed tictactoe.

Open field tic tac toe takes a lot of computation time in algorithms 1,2 and 3.
Only alpha beta with depth limited is giving the output.



