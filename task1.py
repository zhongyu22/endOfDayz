import tkinter as tk
from tkinter import messagebox, simpledialog
from a2 import *
from constants import *


class AbstractGrid(tk.Canvas):
    """
    AbstractGrid is an abstract view class which inherits from tk.Canvas
    and provides base functionality for other view classes.
    """

    def __init__(self, master, rows, cols, width, height, **kwargs):
        """
        Parameters:
         master:
         rows: The number of rows in grid.
         cols: The number of columns in grid.
         width: The width of the grid(in pixels).
         height: The height of the grid(in pixels).
         kwargs: Any additional named  arguments supported by tk.Canvas
         should also be supported AbstractGrid.
        """
        super().__init__(master, **kwargs)

    def get_bbox(self, position):
        """
        Figure out bounding box for the (row, column) position

        Parameters:
            position:pixel positions of the edges of the shape,
                    in the form (x min, y min, x max, y max).
        """
        raise NotImplementedError

    def pixel_to_position(self, pixel):
        """
        Converts the (x, y) pixel position (in graphics units) to a (row,
        column) position.

        Parameters:
            pixel: (x, y) pixel position (in graphics units)
        """
        raise NotImplementedError

    def get_position_center(self, position):
        """
        Gets the graphics coordinates for the center of the cell at the
        given (row, column) position.

        Parameters:
            position:(row, column) position
        """
        bbox = self.get_bbox(position)
        return (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2

    def annotate_position(self, position, text):
        """
        Annotates the center of the cell at the given (row, column) position
        with the provided text.

        Parameters:
            position:  (row, column) position
            text: Content to be shown at the center of cell.
        """
        center = self.get_position_center(position)
        self.create_text(center[0], center[1], text=text)


class BasicMap(AbstractGrid):
    """
    BasicMap is a view class which inherits from AbstractGrid. Entities are
    drawn on the map using coloured rectangles at different (row, column)
    positions.
    """

    def __init__(self, master, size, **kwargs):
        """
        Parameters:
            master: window in in which the map to be drawn.
            size: The size of map.
        """
        super().__init__(master, size, size, width=size * CELL_SIZE,
                         height=size * CELL_SIZE, bg=MAP_BACKGROUND_COLOUR)

        self.config(width=size * CELL_SIZE, height=size * CELL_SIZE)

    def get_bbox(self, position):
        (x, y) = position
        return x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (
                y + 1) * CELL_SIZE

    def annotate_position(self, position, text):
        center = self.get_position_center(position)
        if text in [HOSPITAL, PLAYER]:
            self.create_text(center[0], center[1], text=text, fill='white')
        else:
            self.create_text(center[0], center[1], text=text)

    def draw_entity(self, position, tile_type):
        """
        Draws the entity with tile type at the given position using a
        coloured rectangle with superimposed text identifying the entity.
        Parameters:
            position: (row, column) position.
            tile_type: A string which represents an entity.

        """
        pixel = self.get_bbox(position)
        self.create_rectangle(pixel[0], pixel[1], pixel[2],
                              pixel[3], fill=ENTITY_COLOURS[tile_type])
        self.annotate_position(position, text=tile_type)


class InventoryView(AbstractGrid):
    """
    This class displays the items the player has in their inventory.This class
    also provides a mechanism through which the user can activate an item
    held in the player’s inventory.
    """

    def __init__(self, master, rows, **kwargs):
        """
        Paremeters:
             master:Window which to draw the inventory.
             rows:Rows should be set to the number of rows in the game map.
        """
        super().__init__(master, rows, 2, INVENTORY_WIDTH,
                         MAP_HEIGHT, bg=LIGHT_PURPLE)
        self.config(width=INVENTORY_WIDTH, height=rows * CELL_SIZE)

    def get_bbox(self, position):
        """
        Figure out bounding box for the (row, column) position

        Parameters:
            position:
        """
        (x, y) = position
        return x * INVENTORY_WIDTH / 2, y * CELL_SIZE, \
               (x + 1) * INVENTORY_WIDTH / 2, (y + 1) * CELL_SIZE

    def pixel_to_position(self, pixel):
        """
        Converts the (x, y) pixel position (in graphics units) to a (row,
        column) position.

        Parameters:
              pixel: (x, y) pixel position (in graphics units)
        """
        return pixel[0] // (INVENTORY_WIDTH / 2), pixel[1] // CELL_SIZE

    def annotate_position(self, position, text):
        center = self.get_position_center(position)
        self.create_text(center[0], center[1], text=text, font=('Times', '15'))

    def draw(self, inventory):
        """
        Draws the inventory label and current items with their
        remaining lifetimes.

        Parameters:
            inventory: Inventory instance which belongs to a player.
        """
        self.delete(tk.ALL)
        # draw label
        # draw label text
        self.annotate_position((0.5, 0), text='Inventory')
        # draw current items
        row = 1
        SPACE = "    "
        for item in inventory.get_items():
            if item.is_active():
                # draw item background
                self.create_rectangle((0, row * CELL_SIZE, INVENTORY_WIDTH,
                                       (row + 1) * CELL_SIZE),
                                      fill=DARKEST_PURPLE)

                # annotate item name and lifetime
                center_item = self.get_position_center((0, row))
                self.create_text(center_item[0], center_item[1],
                                 text=SPACE + item.__class__.__name__,
                                 fill='white', font=('Times', '15'))

                center_lifetime = self.get_position_center((1, row))
                self.create_text(center_lifetime[0], center_lifetime[1],
                                 text=item.get_lifetime(), fill='white',
                                 font=('Times', '15'))
                row += 1
            else:
                self.annotate_position((0, row),
                                       text=SPACE + item.__class__.__name__)

                self.annotate_position((1, row), text=item.get_lifetime())
                row += 1

    def toggle_item_activation(self, pixel, inventory):
        """
        Activates or deactivates the item (if one exists) in the row
        containing the pixel.

        Parameters:
              pixel: Position where mouse clicks.
              inventory: Inventory instance which belongs to a player.
        """
        # determine which row did the mouse click
        selected_item = self.get_clicked_item(pixel, inventory)
        if selected_item is None:
            return
        elif inventory.any_active():
            if selected_item.is_active():
                selected_item.toggle_active()
        else:
            selected_item.toggle_active()

    def get_clicked_item(self, pixel, inventory):
        """
        Determine whick item did the mouse click.

        Parameters:
           pixel: Position where mouse clicks.
           inventory: Inventory instance which belongs to a player.
        """
        position_y = self.pixel_to_position(pixel)[1]
        current_items = inventory.get_items()
        # row number equals position_y and nth row represents (n-1)th
        # item in the current_items list
        if position_y in range(1, len(current_items) + 1):
            return current_items[position_y - 1]


class BasicGraphicalInterface:
    """
     The BasicGraphicalInterface should manage the overall view
     (i.e. constructing the three "major widgets) and event handling.
     """

    def __init__(self, root, size):
        """
        This method should draw the title label, and instantiate and pack the
        BasicMap and InventoryView

        Parameters:
            root: root represents the root window.
            size: size represents the number of rows (= number of columns)
                  in the game map.
        """
        self._master = root
        self._size = size
        # Create a frame on the top, in order to put a banner in it.
        self._banner_frame = tk.Frame(self._master)
        self._banner_frame.config(width=size * CELL_SIZE + INVENTORY_WIDTH,
                                  height=BANNER_HEIGHT)
        self._banner_frame.pack_propagate(0)
        self._banner_frame.pack(side=tk.TOP)
        self._label = tk.Label(self._banner_frame, text=TITLE,
                               height=BANNER_HEIGHT, bg=DARKEST_PURPLE,
                               fg='white', font=('Times', '35'))

        self._label.pack(fill=tk.X)
        # Create a game frame to warp map and inventory view.
        self._game_frame = tk.Frame(self._master)
        self._game_frame.pack(side=tk.TOP)
        self._map = BasicMap(self._game_frame, self._size)
        self._map.pack(side=tk.LEFT)
        self._inventory = InventoryView(self._game_frame, self._size)
        self._inventory.pack(side=tk.RIGHT)

        self._game = None

    def _inventory_click(self, event, inventory):
        """
        This method should be called when the user left clicks on inventory
        view. It must handle activating or deactivating the clicked item (if
        one exists) and update both the model and the view accordingly.
        
        Parameters:
            event: Data about the event that has triggered this handler.
            inventory: An inventory holds a collection of entities which the
                        player can pickup.

        """
        pixel = (event.x, event.y)
        self._inventory.toggle_item_activation(pixel, inventory)
        self._inventory.draw(inventory)

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
        offset = game.direction_to_offset(direction)
        game.move_player(offset)
        self.draw(game)
        if game.has_won():
            self._master.after_cancel(self._after_identifier)
            ask = messagebox.askyesno(title=WIN_MESSAGE, message='Play '
                                                                 'again?')
            if ask:
                self.restart_game()
            else:
                return

    def _handle_keypress(self, event, game):
        """
        Convert keypress event to trigger player move.

        Parameters:
            event: Data about the event that has triggered this handler.
            game:The Game handles some of the logic for controlling the actions
                 of the player within the grid.
        """
        key = event.char.upper()
        inventory = game.get_player().get_inventory()
        if key in [UP, LEFT, RIGHT, DOWN]:
            self._move(game, key)

        if event.keysym in ['Down', 'Up', 'Left', 'Right']:
            arrow = ARROWS_TO_DIRECTIONS[event.keysym]
            # Logic to handle player shots zombies.
            if inventory.has_active(CROSSBOW):
                start = game.get_grid().find_player()
                offset = game.direction_to_offset(arrow)
                first = first_in_direction(game.get_grid(), start, offset)
                if first is not None and first[1].display() in ZOMBIES:
                    position, entity = first
                    game.get_grid().remove_entity(position)

    def _step(self, game):
        """
        The step method is called every second. This method triggers the
        step method for the game and updates the view accordingly.

        Parameters:
            game:The Game handles some of the logic for controlling the actions
                 of the player within the grid.
        """
        game.step()
        if game.has_lost():
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
        # Trigger zombies to move per second.
        self._after_identifier = self._master.after(1000,
                                                    lambda: self._step(game))

    def play(self, game):
        """
        Binds events and initialises gameplay. This method will need to be
        called on the instantiated BasicGraphicalInterface in main to commence
        gameplay

        Parameters:
            game:The Game handles some of the logic for controlling the actions
                 of the player within the grid.
        """
        self._master.bind("<Key>",
                          lambda event: self._handle_keypress(event, game))
        inventory = game.get_player().get_inventory()
        self._inventory.bind("<Button-1>", lambda event: self._inventory_click
                                                            (event, inventory))
        self._step(game)
        self.draw(game)

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
        game_serialize = game.get_grid().serialize()
        for position in game_serialize:
            self._map.draw_entity(position, game_serialize[position])

    def restart_game(self):
        """
        This method will cause game to its original state.
        """
        self._master.after_cancel(self._after_identifier)
        game = advanced_game(MAP_FILE)
        self._map.delete(tk.ALL)
        self._inventory.delete(tk.ALL)
        self.play(game)
