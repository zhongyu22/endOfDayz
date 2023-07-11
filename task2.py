import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from a2 import *
from task1 import *
from constants import *
from PIL import Image, ImageTk


class StatusBar(tk.Frame):
    """
    A statusbar that includes :
        The chaser and chasee images.
        1.A game timer displaying the number of minutes and seconds the user
        has been playing the current game.
        2.A moves counter, displaying how many moves the player has made in the
        current game.
        3.A ‘Quit Game’ button, which ends the program.4
        4.A ‘Restart Game’ button, which allows the user to start the game again.
          This must reset the information on the status bar, as well as setting
          the map back to how it appeared at the start of the game. Clicking
          the ‘Restart Game’ button after game play is finishedshould start a new game.
    """

    def __init__(self, master, width):
        """
        Parameters:
            master:Main window of the drawing application.
            width: Map width.

        """

        super().__init__(master)
        self._master = master
        self._width = width
        self._chasee = ImageTk.PhotoImage(Image.open("images/chasee.png").
                                          resize((CELL_SIZE, CELL_SIZE)))
        self._chaser = ImageTk.PhotoImage(Image.open("images/chaser.png").
                                          resize((CELL_SIZE, CELL_SIZE)))

        # There are five frames in the bar, each frame occupies 1/5 bar width.
        FRAME_WIDTH = (INVENTORY_WIDTH + self._width) / 5

        # chaser frame
        self._chaser_frame = tk.Frame(self._master, width=FRAME_WIDTH,
                                      height=CELL_SIZE)
        self._chaser_frame.pack(side=tk.LEFT)
        self._chaser_frame.pack_propagate(0)
        self._chaser_logo = tk.Label(self._chaser_frame, image=self._chaser)
        self._chaser_logo.pack()

        # timer frame
        self._timer_frame = tk.Frame(self._master, width=FRAME_WIDTH,
                                     height=CELL_SIZE)
        self._timer_frame.pack(side=tk.LEFT)
        self._timer_frame.pack_propagate(0)
        tk.Label(self._timer_frame, text="Timer").pack()
        self._timer_text = tk.Label(self._timer_frame, text="0 mins 0 seconds")
        self._timer_text.pack()

        # move frame
        self._move_frame = tk.Frame(self._master, width=FRAME_WIDTH,
                                    height=CELL_SIZE)
        self._move_frame.pack(side=tk.LEFT)
        self._move_frame.pack_propagate(0)
        tk.Label(self._move_frame, text="Moves made").pack()
        self._move_text = tk.Label(self._move_frame,
                                   text="0 moves")
        self._move_text.pack()

        # Quit & restart frame
        self._setting_frame = tk.Frame(self._master, width=FRAME_WIDTH,
                                       height=CELL_SIZE)
        self._setting_frame.pack(side=tk.LEFT)
        self._setting_frame.pack_propagate(0)
        self._restart_button = tk.Button(self._setting_frame,
                                         text="Restart Game")
        self._restart_button.pack()
        self._quit_button = tk.Button(self._setting_frame, text="Quit Game",
                                      command=self.quit)
        self._quit_button.pack()

        # chase frame
        self._chasee_frame = tk.Frame(self._master, width=FRAME_WIDTH,
                                      height=CELL_SIZE)
        self._chasee_frame.pack(side=tk.LEFT)
        self._chasee_frame.pack_propagate(0)
        self._chasee_logo = tk.Label(self._chasee_frame, image=self._chasee)
        self._chasee_logo.pack()

        self._count = 0
        self._time = ""
        self._seconds = 0

    def set_command(self, callback1, callback2):
        """
        Bind buttons with method in Interface.
        """
        self._restart_button.config(command=callback1)
        self._quit_button.config(command=callback2)

    def count(self):
        """
        Count player's move steps.
        """
        self._count += 1
        self._move_text.config(text=f"{self._count} moves")

    def get_count(self):
        """
        Get player's move steps.
        """
        return self._count

    def change_count(self, count):
        """
        Change play's move steps. It could be useful when load a game.

        Parameters:
             count: move steps which you want to set.
        """
        self._count = count
        self._move_text.config(text=f"{self._count} moves")

    def timer(self, step: int):
        """
        A timer to record how long the game has been started.Since game step s
        is triggered per second, so game steps is always equal to game's
        duration time(seconds).

        Parameters:
            step: Game steps.
        """
        self._seconds = step
        min = step // 60
        second = step % 60
        self._timer_text.config(text=f"{min} mins {second} seconds")
        self._time = f"{min} mins {second} seconds"

    def get_timer(self):
        """
        Get the elapsed time of the game(min-second format)
        """
        return self._time

    def get_seconds(self):
        """
        Get the elapsed time of the game(second format)
        """
        return self._seconds

    def reset(self):
        """
        Clear steps and time
        """
        self._count = 0
        self._move_text.config(text="0 moves")


class ImageMap(BasicMap):
    """
    ImageMap extends existing BasicMap class. This class should behave
    similarly to BasicMap, except that images should be used to display
     each square rather than rectangles .
    """
    def __init__(self, master, size, **kwargs):
        super().__init__(master, size)
        self._size = size * CELL_SIZE

        self._arrow = ImageTk.PhotoImage(Image.open(IMAGES[ARROW]).
                                         resize((CELL_SIZE, CELL_SIZE)))
        self._crossbow = ImageTk.PhotoImage(Image.open(IMAGES[CROSSBOW]).
                                            resize((CELL_SIZE, CELL_SIZE)))
        self._garlic = ImageTk.PhotoImage(Image.open(IMAGES[GARLIC]).
                                          resize((CELL_SIZE, CELL_SIZE)))
        self._hero = ImageTk.PhotoImage(Image.open(IMAGES[PLAYER]).
                                        resize((CELL_SIZE, CELL_SIZE)))
        self._hospital = ImageTk.PhotoImage(Image.open(IMAGES[HOSPITAL]).
                                            resize((CELL_SIZE, CELL_SIZE)))
        self._zombie = ImageTk.PhotoImage(Image.open(IMAGES[ZOMBIE]).
                                          resize((CELL_SIZE, CELL_SIZE)))
        self._background = ImageTk.PhotoImage(Image.open(IMAGES[BACK_GROUND]).
                                          resize((CELL_SIZE, CELL_SIZE)))

        self._image = {
            PLAYER: self._hero,
            HOSPITAL: self._hospital,
            ZOMBIE: self._zombie,
            GARLIC: self._garlic,
            TRACKING_ZOMBIE: self._zombie,
            CROSSBOW: self._crossbow,
            ARROW: self._arrow,
            BACK_GROUND: self._background
        }

    def draw_entity(self, position, tile_type):
        center = self.get_position_center(position)
        self.create_image(center[0], center[1], image=self._image[tile_type])


class FileMenu(tk.Menu):
    """
    A file menu will appear at the top of the game window.
    """
    def __init__(self, master, menus):
        """
        master: Main window of the drawing application.
        menus: Details of all the menus for this window.
        """
        super().__init__(master)
        master.config(menu=self)
        MENU_NAME = 0
        MENU_ITEMS = 1

        # Extract all menus from the list and add them to the menubar.
        for menu_details in menus:
            menu_to_add = tk.Menu(self)
            self.add_cascade(label=menu_details[MENU_NAME], menu=menu_to_add)
            # Extract all items for each menu and add them to the menu.
            for menu_item, event_handler in menu_details[MENU_ITEMS].items():
                menu_to_add.add_command(label=menu_item, command=event_handler)


class ImageGraphicalInterface(BasicGraphicalInterface):
    """
    The BasicGraphicalInterface should manage the overall view
     (i.e. constructing the three "major widgets) and event handling."""

    def __init__(self, root, size):
        self._master = root
        self._size = size
        self._width = self._height = CELL_SIZE * self._size
        self._banner_frame = tk.Frame(self._master)
        self._banner_frame.pack(side=tk.TOP)
        self._banner_logo = self._banner = ImageTk.PhotoImage \
            (Image.open("images/banner.png").resize
             ((self._width + INVENTORY_WIDTH,
               BANNER_HEIGHT)))

        self._label = tk.Label(self._banner_frame, image=self._banner_logo)
        self._label.pack()

        self._game_frame = tk.Frame(self._master)
        self._game_frame.pack()
        self._map = ImageMap(self._game_frame, self._size)
        self._map.pack(side=tk.LEFT, anchor=tk.W)
        self._inventory = InventoryView(self._game_frame, self._size)
        self._inventory.pack(side=tk.RIGHT, anchor=tk.E)

        self._statusbar_frame = tk.Frame(self._master)
        self._statusbar_frame.config(width=INVENTORY_WIDTH + self._size *
                                           CELL_SIZE, height=80)
        self._statusbar_frame.pack_propagate(0)
        self._statusbar_frame.pack()
        self._statusbar = StatusBar(self._statusbar_frame,
                                    self._size * CELL_SIZE)
        self._statusbar.pack()
        self._statusbar.set_command(self.restart_game, self.quit)

        FileMenu(self._master, [("File", {"Restart game":
                                              self.restart_game,
                                          "Save game": self.save_game,
                                          "Load game": self.load_game,
                                          "High score": self.show_high_scores,
                                          "Quit": self.quit})
                                ])

    def _move(self, game, direction):
        """
        Handles moving the player and redrawing the game. It may be easiest
        to create a new method to handle the ‘<KeyPress>’ event, which calls
        move with the relevant arguments.

        Parameters:
            game:The Game handles some of the logic for controlling the actions
                 of the player within the grid.
            direction: A direction which player prompts.
                """
        self._statusbar.count()
        offset = game.direction_to_offset(direction)
        game.move_player(offset)
        # Restore game state after move, in order to save game later.
        self._game = game
        self.draw(game)
        if game.has_won():
            self._master.after_cancel(self._after_identifier)
            try:
                self._third_score = self.get_high_scores()[2][0]
            except IndexError:
                self._third_score = float("inf")

            if self._statusbar.get_seconds() < self._third_score:
                self.prompt_name()
            else:
                ask = messagebox.askyesno(title=WIN_MESSAGE, message='Play '
                                                                      'again?')
                if ask:
                    self.restart_game()
                else:
                    return

    def _step(self, game):
        """
        The step method is called every second. This method triggers the
        step method for the game and updates the view accordingly.

        Parameters:
            game:The Game handles some of the logic for controlling the actions
                 of the player within the grid.
        """
        # After each step, game time plus one.
        self._statusbar.timer(game.get_steps())
        super()._step(game)

    def get_game(self):
        """
        Get game data to save game.
        """
        return self._game

    def draw(self, game):
        """
        Clears and redraws the view based on the current game state

        Parameter:
            game:The Game handles some of the logic for controlling the actions
                 of the player within the grid.
        """
        self._map.delete(tk.ALL)
        self._inventory.delete(tk.ALL)
        # draw inventory
        inventory = game.get_player().get_inventory()
        self._inventory.draw(inventory)
        # draw map
        for i in range(game.get_grid().get_size()):
            for j in range(game.get_grid().get_size()):
                self._map.draw_entity((i, j), BACK_GROUND)
        game_serial = game.get_grid().serialize()
        for position in game_serial:
            self._map.draw_entity(position, game_serial[position])

    def restart_game(self):
        """
        This method will cause game and status bar to its original state.
        """
        self._master.after_cancel(self._after_identifier)
        game = advanced_game(MAP_FILE)
        self._map.delete(tk.ALL)
        self._inventory.delete(tk.ALL)
        self._statusbar.reset()
        self.play(game)

    def save_game(self):
        """
        Create a txt file to restore all information need to preserved.
        """
        self._master.after_cancel(self._after_identifier)
        file_name = filedialog.asksaveasfilename()
        if file_name:
            with open(file_name, 'w') as file:
                serial = self.get_game().get_grid().serialize()
                for key in serial:
                    file.write(f"{key}:{serial[key]}\n")

                inventory = self.get_game().get_player().get_inventory().get_items()
                for item in inventory:
                    file.write(f"{item.display()}={item.get_lifetime()}\n")

                file.write(f"{self.get_game().get_grid().get_size()}\n")
                file.write(f"{self.get_game().get_steps()}\n")
                file.write(f"{self._statusbar.get_count()}\n")

    def load_game(self):
        """
        Load game from a txt file.
        """
        self._master.after_cancel(self._after_identifier)
        file_name = filedialog.askopenfilename()
        try:
            if file_name:
                with open(file_name, 'r') as file:
                    mapping = {}
                    inventory = {}
                    other_info = []
                    # Get mapping data.
                    for line in file:
                        line = line.strip()
                        if line.count(':') == 1:
                            name, value = line.split(':')
                            mapping[str_tuple(name.strip())] = value.strip()
                        # Get inventory data.
                        elif line.count('=') == 1:
                            item, lifetime = line.split('=')
                            inventory[item.strip()] = int(lifetime.strip())
                        # Get moves and steps data.
                        else:
                            other_info.append(int(line))

                grid_size = other_info[0]
                game_steps = other_info[1]
                moves = other_info[2]

                # Initialise new game using data got above.
                new_grid = AdvancedMapLoader().load_game(Grid(grid_size),
                                                         mapping)
                new_game = load_new_game(new_grid)
                for item in inventory:
                    pickup = str_to_item(item)
                    new_game.get_player().get_inventory().add_item(pickup)
                    pickup.set_lifetime(inventory[item])

                new_game.change_steps(game_steps - 1)
                self._statusbar.change_count(moves)
                self._map.delete(tk.ALL)
                self._inventory.delete(tk.ALL)
                self.play(new_game)

        except ValueError:
            toplevel = tk.Toplevel(self._master)
            toplevel.title('Error')
            toplevel.geometry("300x100")
            tk.Label(toplevel, text="Please choose a correct \nfile to be "
                                    "loaded!", font=20).pack()

    def prompt_name(self):
        """
        Request users to enter names if they achieve top 3 scores.
        """
        toplevel = tk.Toplevel(self._master)
        toplevel.title(WIN_MESSAGE)
        tk.Label(toplevel, text=f"You won in {self._statusbar.get_timer()}! "
                                f"Enter your name:", pady=5).pack()

        string_var = tk.StringVar(toplevel)
        entry = tk.Entry(toplevel, textvariable=string_var)
        entry.pack(side=tk.TOP, pady=5)
        # Stop game after entering name.
        button_stop = tk.Button(toplevel, text="Enter", command=lambda: [
            toplevel.destroy(), self.write_name_to_file(string_var.get())])
        button_stop.pack(side=tk.LEFT, padx=20, pady=10)
        # Restart game after entering name.
        button_again = tk.Button(toplevel, text="Enter and play again",
                                 command=lambda: [
                                     self.write_name_to_file(string_var.get()),
                                     toplevel.destroy(),
                                     self.restart_game()])
        button_again.pack(side=tk.RIGHT, padx=20, pady=10)

    def write_name_to_file(self, name):
        """
        Put name entered by user in high_scores file.

        Parameters:
            name: Name that user enters.
        """
        file = open(HIGH_SCORES_FILE, 'a')
        file.write(f"{self._statusbar.get_seconds()}:{name}\n")
        file.close()

    def get_high_scores(self):
        """
        SGet top 3 scores in the high_scores file.
        """
        try:
            open(HIGH_SCORES_FILE, 'r')
        except IOError:
            open(HIGH_SCORES_FILE, 'w')

        with open(HIGH_SCORES_FILE, 'r') as file:
            rank = {}
            count = 0
            for line in file:
                line = line.strip()
                count += 1
                if line.count(':') == 1:
                    name, value = line.split(':')
                    rank[int(name.strip())] = value.strip()
            top_3 = sorted(rank.items(), key=lambda x: x[0])[
                    :MAX_ALLOWED_HIGH_SCORES]
            return top_3

    def show_high_scores(self):
        """
        Show top 3 scores in the pop-up window.
        """
        toplevel = tk.Toplevel(self._master)
        toplevel.title('Top 3')
        tk.Label(toplevel, text="High scores", fg="white",
                 bg=DARKEST_PURPLE, font=('Calibri', 40)).pack(fill=tk.X)

        top_3 = self.get_high_scores()
        for score in top_3:
            time, player = score
            if time >= 60:
                text = f"{player}: {time // 60}m {time % 60}s"
            else:
                text = f"{player}: {time}s"
            tk.Label(toplevel, text=text).pack()
        tk.Button(toplevel, text="Done", command=toplevel.destroy).pack()

    def quit(self):
        """
        Pop up a window to ask user if they want to quit game.
        """
        if messagebox.askyesno(title='Quit', message="Are you sure to quit "
                                                     "the game?"):
            exit()


def str_tuple(x: str):
    """
    Convert a tuple of string format to a real tuple.
    Example: "(1, 2)" -> (1, 2)
    """
    temp = x.replace('(', '').replace(')', '')
    return tuple([int(i) for i in temp.split(',')])
