# **Tic Tac Toe using AI**

This is the simple game of 'Tic Tac Toe' also known as 'Noughts & Crosses'.

 GitHub Repo Link [ketan-lambat/AI_Games](https://github.com/ketan-lambat/AI_Games "ketan-lambat/AI_Games")
>  This might return a 404 as the Repo is private

Gameplay Video URL [TicTacToe with AI](http://youtube.com "TicTacToe with AI")

------------


First to setup the game dependencies, you need to install [pygame](https://www.pygame.org/docs/ "pygame").

`
pip install pygame
`

------------



## To run the 3x3 varient
1.  Navigate to *src/3x3 Tic Tac Toe/*  directory in the terminal or command prompt.
2.  Enter the command 
`
 python TicTacToe_AI.py
` to run the script.
3. You should get the Hello message from the pygame community in the terminal and the game application window shall now open.
4. Select the AI algorithm to use by clicking on the appropriate button and watch the terminal too for the output messages.
5. The Tic Tac Toe game shall now start, and you can play by clicking on the box you want to make the next move on.
6. Ensure you watch the terminal to get the **time taken** by the AI algo to decide the next move.
7. If either of the player wins, you can see that with the strike through line across the winning cells, or a Game Draw message if all the cells are filled (simple Tic Tac Toe rule).
8. The average time taken by the AI algo is printed in the console window after the game ends and the game application window closes.


## To run the Open Field Varient
1.  Navigate to *src/Open Field Tic Tac Toe/*  directory in the terminal or command prompt.
2.  Enter the command 
`
 python TicTacToe_AI.py
` to run the script.
3. You should get the Hello message from the pygame community in the terminal and the game application window shall now open.


-----

> (Optional) To build an executable file, you will need [cx_Freeze](https://anthony-tuininga.github.io/cx_Freeze/ "cx_Freeze")

`
python -m pip install cx_Freeze
`