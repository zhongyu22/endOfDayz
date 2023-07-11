import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from a2 import *
from task2 import *
from constants import *
from PIL import Image, ImageTk

class MastersMap(ImageMap):
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
        self._time_machine = ImageTk.PhotoImage(Image.open(
            'time_machine.png').resize((CELL_SIZE, CELL_SIZE)))

        self._image = {
            PLAYER: self._hero,
            HOSPITAL: self._hospital,
            ZOMBIE: self._zombie,
            GARLIC: self._garlic,
            TRACKING_ZOMBIE: self._zombie,
            CROSSBOW: self._crossbow,
            ARROW: self._arrow,
            BACK_GROUND: self._background,
            TIME_MACHINE: self._time_machine
        }

    def draw_entity(self, position, tile_type):
        center = self.get_position_center(position)
        self.create_image(center[0], center[1], image=self._image[tile_type])

class MastersGraphicalInterface(ImageGraphicalInterface):
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
        self._map = MastersMap(self._game_frame, self._size)
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
        # Restore map data after time machine being activated
        self._serial = []
        # Restore inventory data after time machine being activated
        self._inventory_serial = []
        self._steps = []



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


    def _move(self, game, direction):
        self._statusbar.count()
        offset = game.direction_to_offset(direction)
        game.move_player(offset)
        self.draw(game)
        if game.get_player().get_inventory().has_active(TIME_MACHINE):
            serial = game.get_grid().serialize()
            if len(self._serial) < 5:
                self._serial.append(serial)
            else:
                for i in range(4):
                    self._serial[i] = self._serial[i + 1]
                self._serial[4] = serial

            inventory = game.get_player().get_inventory()
            inventory_serial = inventory.serialize()
            if len(self._inventory_serial) < 5:
                self._inventory_serial.append(inventory_serial)
            else:
                for i in range(4):
                    self._inventory_serial[i] = self._inventory_serial[i + 1]
                self._inventory_serial[4] = inventory_serial

            if len(self._steps) < 5:
                self._steps.append(game.get_steps())
            else:
                for i in range(4):
                    self._steps[i] = self._steps[i + 1]
                self._steps[4] = game.get_steps()

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
        self._statusbar.timer(game.get_steps())
        game.step()
        if game.has_lost():
            if game.get_player().get_inventory().has_active(TIME_MACHINE):
                game.get_player().get_inventory().remove_time_machine()
                if len(self._serial) < 5:
                    self.restart_game()
                else:
                    grid_size = game.get_grid().get_size()
                    new_grid = AdvancedMapLoader().load_game(Grid(grid_size),
                                                             self._serial[0])
                    new_game = load_new_game(new_grid)
                    for item in self._inventory_serial[0]:
                        if item == TIME_MACHINE:
                            pass
                        pickup = str_to_item(item)
                        new_game.get_player().get_inventory().add_item(pickup)
                        pickup.set_lifetime(self._inventory_serial[0][item])

                    new_game.change_steps(self._steps[0])
                    self._statusbar.change_count(self._statusbar.get_count() - 5)
                    self._map.delete(tk.ALL)
                    self._inventory.delete(tk.ALL)
                    self._steps.clear()
                    self._serial.clear()
                    self._inventory_serial.clear()
                    self.play(new_game)
                    return

            else:
                self._master.after_cancel(self._after_identifier)
                ask = messagebox.askyesno(title=LOSE_MESSAGE, message='Play '
                                                                      'again?')
                if ask:
                    self.restart_game()
                    return
                else:
                    return

        self.draw(game)
        self._inventory.draw(game.get_player().get_inventory())
        self._after_identifier = self._master.after(1000,
                                                    lambda: self._step(game))

