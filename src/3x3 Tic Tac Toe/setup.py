import cx_Freeze

# name of the main game file
executables = [cx_Freeze.Executable("TicTacToe_AI.py")]

cx_Freeze.setup(
    # title of the application window
    name="Tic Tac Toe AI",
    options={"build_exe": {"packages": ["pygame"],
                           # other files that are part of the project
                           "include_files": ["O.png", "X.png", "AI_algo.py", "ZealotOutline-rnMy.ttf", "Gallant-2O1r3.ttf", "TicTacToe.ttf", "FrostbiteBossFight-dL0Z.ttf"]}},

    executables=executables

)
