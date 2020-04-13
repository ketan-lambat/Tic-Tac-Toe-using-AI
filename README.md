# **Tic Tac Toe using AI**

This is the simple game of 'Tic Tac Toe' also known as 'Noughts & Crosses'.

 GitHub Repo Link [ketan-lambat/AI_Games](https://github.com/ketan-lambat/AI_Games "ketan-lambat/AI_Games")
>  This might return a 404 if the Repo is still private

Gameplay Video URL [TicTacToe with AI](https://youtu.be/Q0U6IyicW9E "TicTacToe with AI")

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
![3x3Home](/img/1.3x3Home.jpg)
4. Select the AI algorithm to use by clicking on the appropriate button and watch the terminal too for the output messages.
![Algo Selected](/img/2.AlgoSelected.jpg)
5. The Tic Tac Toe game shall now start, and you can play by clicking on the box you want to make the next move on.
6. Ensure you watch the terminal to get the **time taken** by the AI algo to decide the next move.
![AI Time Taken](/img/3.AI_TimeTaken.jpg)
7. If either of the player wins, you can see that with the strike through line across the winning cells, or a Game Draw message if all the cells are filled (simple Tic Tac Toe rule).
![AI Wins](/img/4.AI_wins.jpg)

8. The **average time taken by the AI algo is printed in the console window** after the game ends and the game application window closes.
![Game Draw](/img/5.Draw.jpg)


## To run the Open Field Varient
1.  Navigate to *src/Open Field Tic Tac Toe/*  directory in the terminal or command prompt.
2.  Enter the command 
`
 python TicTacToe_AI.py
` to run the script.
3. You should get the Hello message from the pygame community in the terminal and the game application window shall now open.
4. Select the size of the board you wish to play on.
![Open Field Home](/img/6.OpenFieldHome.jpg)
5. Select the AI_algo to use. Due to **computational constraints**, these algo might take longer to generate an output (or might not generate at all). So kindly use the ones mentioned.
![Grid Selected](/img/7.GridSelected.jpg)
6. Next steps are same as the above game.

![Algo Selected](/img/8.AlgoSelected.jpg)

![User Wins](/img/9.UserWin.jpg)

### Notice the High Computation time required for Alpha-Beta Pruning algo for 4x4 grid

![High Computational Time](/img/10.ComputTime.jpg)

-----

> (Optional) To build an executable file (if not already present), you will need [cx_Freeze](https://anthony-tuininga.github.io/cx_Freeze/ "cx_Freeze")

`
python -m pip install cx_Freeze
`
- Navigate to the project folder *src/Open Field Tic Tac Toe/* or *src/3x3 Tic Tac Toe/* 
- The setup.py file contains the configuration for the build command
- Run the command
`
python setup.py build
`
- This will create a build folder in the directory which should have a folder named *ext.____* 
- Within this folder will be an executable file eg. *TicTacToe_AI.exe*
- Double-click on this and the console output window and the game application window will open and you can play the game as mentioned above.

------
### Points to Note
- Here we are sourcing the static files(images and fonts) from the same folder as the source code. We can also put them in a static folder and and access them using relative paths. But, this creates issues when building the executable file. So, to avoid that, the static folder method has not been used.
- Each project has 3 python (.py) files, 2 are the source code and the setup.py file contains the instructions for building the executable.
