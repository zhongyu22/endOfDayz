"""
A GUI-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

# Replace these <strings> with your name, student number and email address.
__author__ = "Zhongyu Sun, 46634261"
__email__ = "zhongyu.sun@uqconnect.edu.au"


import tkinter as tk
from a2 import advanced_game
from constants import TASK, MAP_FILE

# Uncomment the following imports to import the view classes that represent
# the GUI for each of the tasks that you implement in the assignment.
from task1 import BasicGraphicalInterface
from task2 import ImageGraphicalInterface
from csse import MastersGraphicalInterface


def main() -> None:
	"""Entry point to gameplay."""
	game = advanced_game(MAP_FILE)

	root = tk.Tk()
	root.title('EndOfDayz')
	if TASK == 1:
		gui = BasicGraphicalInterface
	elif TASK == 2:
		gui = ImageGraphicalInterface
	else:
		gui = MastersGraphicalInterface
	app = gui(root, game.get_grid().get_size())
	app.play(game)
	root.mainloop()


if __name__ == '__main__':
	main()
