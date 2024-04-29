import tkinter as tk
import tkinter.ttk as ttk
import math
import json
import random

better_pokemon_data_keys_dict = {
    "type_main": {"key": "Type I", "data_type": "boolean"},
    "type_secondary": {"key": "Type II", "data_type": "boolean"},
    "ability_one": {"key": "Ability I", "data_type": "boolean"},
    "ability_two": {"key": "Ability II", "data_type": "boolean"},
    "hidden_ability": {"key": "Hidden Ability", "data_type": "boolean"},
    "evolution_stage": {"key": "Evolution Stage", "data_type": "boolean"},
    "classification": {"key": "Classification", "data_type": "boolean"},
    "number": {"key": "#", "data_type": "range"},
    "health": {"key": "HP", "data_type": "range"},
    "attack": {"key": "Atk", "data_type": "range"},
    "defense": {"key": "Def", "data_type": "range"},
    "special_attack": {"key": "SpA", "data_type": "range"},
    "special_defense": {"key": "SpD", "data_type": "range"},
    "speed": {"key": "Spe", "data_type": "range"},
    "total_stats": {"key": "Tot", "data_type": "range"},
    "height": {"key": "Height (m)", "data_type": "range"},
    "weight": {"key": "Weight (kg)", "data_type": "range"},
    "catch_rate": {"key": "Catch Rate", "data_type": "range"},
    "evolution_method": {"key": "Evolution", "data_type": "None"},
}

guess_display_order = [
    "type_main",
    "type_secondary",
    "evolution_stage",
    "height",
    "weight",
]


def resize_image(image, width=False, height=False, resize_resolution=10):
    """
    Resize the given image based on the specified width, height, and resize resolution.

    Args:
        image: The image to be resized.
        width (optional): The desired width of the image. If not provided, the width will not be changed.
        height (optional): The desired height of the image. If not provided, the height will not be changed.
        resize_resolution (optional): The resolution used for resizing the image. Default is 10.

    Returns:
        The resized image.

    """
    original_width = image.width()
    original_height = image.height()
    print(f"Original Size: {original_width, original_height}")
    if width:
        width_fraction = math.ceil((width / original_width) / (resize_resolution / 100))
        print(f"Width Fraction : {width_fraction}")
    if height:
        height_fraction = math.ceil(
            (height / original_height) / (resize_resolution / 100)
        )
        print(f"Height Fraction Numerator : {height_fraction}")

    print(f"Shrinking Denominator : {resize_resolution}")
    return image.zoom(
        width_fraction if width else 1, height_fraction if height else 1
    ).subsample(resize_resolution if width else 1, resize_resolution if height else 1)


class Guess:
    """
    Represents a game guess.

    Attributes:
    - correct_pokemon: The correct Pokemon object for the guess.
    - guessed_pokemon_list: A list of guessed Pokemon objects.

    Methods:
    - compare_range: Compares a guessed value with the correct value for a given key.
    - compare_boolean: Compares a guessed value with the correct value for a given key (boolean type).
    - guess_display: Displays the guessed Pokemon and their results.
    - guess: Performs a guess and updates the guessed Pokemon list.
    """

    def __init__(self, correct_pokemon):
        self.correct_pokemon = correct_pokemon
        self.guessed_pokemon_list = []

    def compare_range(self, guessed_value, key):
        """
        Compare the guessed value with the correct value for a given key.

        Parameters:
        - guessed_value (int): The value guessed by the player.
        - key (str): The key representing the attribute of the correct value.

        Returns:
        - str: The result of the comparison. Possible values are "Equal", "Greater", "Less", or "Error".
        """
        correct_value = self.correct_pokemon.key(key)
        if correct_value == guessed_value:
            return "True"
        if correct_value > guessed_value:
            return "Greater"
        if correct_value < guessed_value:
            return "Less"
        return "Error"

    def compare_boolean(self, guessed_value, key):
        """
        Compare the guessed value with the correct value for the given key.

        Parameters:
        - guessed_value (bool): The value guessed by the player.
        - key (str): The key representing the attribute of the Pokemon.

        Returns:
        - bool: True if the guessed value matches the correct value, False otherwise.
        """
        if self.correct_pokemon.key(key) == guessed_value:
            return "True"
        else:
            return "False"

    def guess(self, guessed_pokemon_name):
        """
        Performs a guess and updates the guessed Pokemon list.

        Args:
        - guessed_pokemon_name: The name of the guessed Pokemon.

        Returns:
        - The updated guessed_pokemon_list.
        """
        result = {}
        guessed_pokemon = Pokemon(
            (guessed_pokemon_name, pokemon_data[guessed_pokemon_name])
        )
        if self.correct_pokemon.number == guessed_pokemon.number:
            result = {"Correct": True}
        else:
            result = {"Correct": False}
        for key, value in better_pokemon_data_keys_dict.items():
            guessed_value = guessed_pokemon.key(key)
            if value["data_type"] == "range":
                result[key] = {
                    "data_type": value["data_type"],
                    "guessed_value": guessed_value,
                    "result": self.compare_range(guessed_value, key),
                }
            elif value["data_type"] == "boolean":
                result[key] = {
                    "data_type": value["data_type"],
                    "guessed_value": guessed_value,
                    "result": self.compare_boolean(guessed_value, key),
                }

        self.guessed_pokemon_list.append(
            {
                "guess_number": len(self.guessed_pokemon_list),
                "guess_pokemon": guessed_pokemon.name,
                "results": result,
            }
        )
        # return self.guessed_pokemon_list


class Pokemon:
    """
    Represents a Pokemon object.

    Attributes:
        name (str): The name of the Pokemon.
        data (dict): The data associated with the Pokemon.
    """

    def __init__(self, pokemon_tuple):
        self.name = pokemon_tuple[0]
        self.data = pokemon_tuple[1]

    def __getattr__(self, attr_name):
        return self.data[better_pokemon_data_keys_dict[attr_name]["key"]]

    def key(self, key):
        """
        Retrieves the value from the `data` dictionary based on the given `key`.

        Parameters:
        key (str): The key to retrieve the value for.

        Returns:
        The value associated with the given key in the `data` dictionary.
        """
        return self.data[better_pokemon_data_keys_dict[key]["key"]]


# Load Pokemon data
with open("Pokemon.json", encoding="utf-8") as file:
    pokemon_data = json.load(file)

# Select a random Pokemon
pokemon_data = pokemon_data[0]
target_pokemon = random.choice(list(pokemon_data.items()))

# print(target_pokemon)
correctPokemon = Pokemon(target_pokemon)
# print(f"Correct Pokemon: {correctPokemon.name}")

# Create a Guess object
guess_attempt = Guess(correctPokemon)

# guess_attempt.guess("Ivysaur")
# print(f"LIST: {guess.guessed_pokemon_list}")


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return "#%02x%02x%02x" % (red, green, blue)


def test():
    print("Hello")


class RabRectangle:
    """
    A class representing a custom rectangle shape.

    Args:
        parent: The parent canvas object.
        x: The x-coordinate of the top-left corner of the rectangle.
        y: The y-coordinate of the top-left corner of the rectangle.
        width: The width of the rectangle.
        height: The height of the rectangle.
        corner_radius: The radius of the rounded corners of the rectangle.
        fill: The fill color of the rectangle.
        text_data: Optional text data for displaying text within the rectangle.
        button: A boolean indicating whether the rectangle is a button.
        input: A boolean indicating whether the rectangle is an input field.
        command: The command to be executed when the button is clicked.
        top_left_arc: A boolean indicating whether the top-left corner has an arc.
        top_right_arc: A boolean indicating whether the top-right corner has an arc.
        bottom_left_arc: A boolean indicating whether the bottom-left corner has an arc.
        bottom_right_arc: A boolean indicating whether the bottom-right corner has an arc.
        rect_outline: A boolean indicating whether the rectangle has an outline.

    Attributes:
        canvas: The parent canvas object.
        x: The x-coordinate of the top-left corner of the rectangle.
        y: The y-coordinate of the top-left corner of the rectangle.
        width: The width of the rectangle.
        height: The height of the rectangle.
        corner_radius: The radius of the rounded corners of the rectangle.
        fill: The fill color of the rectangle.
        top_left_arc: A boolean indicating whether the top-left corner has an arc.
        top_right_arc: A boolean indicating whether the top-right corner has an arc.
        bottom_left_arc: A boolean indicating whether the bottom-left corner has an arc.
        bottom_right_arc: A boolean indicating whether the bottom-right corner has an arc.
        text_data: Optional text data for displaying text within the rectangle.
        rect_outline: A boolean indicating whether the rectangle has an outline.
        input: A boolean indicating whether the rectangle is an input field.
        button: A boolean indicating whether the rectangle is a button.
        command: The command to be executed when the button is clicked.
        rectangle: The rectangle shape created on the canvas.
        text_id: The ID of the text object created on the canvas (if text_data is provided).

    Methods:
        make_rectangle: Creates the polygon shape of the rectangle.
        _on_press: Event handler for the button press event.
        _on_release: Event handler for the button release event.
    """

    def __init__(
        self,
        parent,
        x,
        y,
        width,
        height,
        corner_radius,
        fill,
        text_data=None,
        button=False,
        input=False,
        command=None,
        top_left_arc=True,
        top_right_arc=True,
        bottom_left_arc=True,
        bottom_right_arc=True,
        rect_outline=False,
    ):
        self.canvas = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.fill = fill
        self.top_left_arc = top_left_arc
        self.top_right_arc = top_right_arc
        self.bottom_left_arc = bottom_left_arc
        self.bottom_right_arc = bottom_right_arc
        self.text_data = text_data
        self.rect_outline = rect_outline
        self.input = input

        self.rectangle = self.make_rectangle()

        if self.text_data:
            # print(f'Creating Text: {self.text_data["string"]}')
            self.text_id = self.canvas.create_text(
                self.x + self.width / 2,
                self.y + self.height / 2,
                text=self.text_data["string"],
                fill=self.text_data["color"],
                font=(self.text_data["font"], self.text_data["size"]),
            )
        self.button = button
        if self.button:
            self.command = command
            self.canvas.tag_bind(self.rectangle, "<ButtonPress-1>", self._on_press)
            self.canvas.tag_bind(self.rectangle, "<ButtonRelease-1>", self._on_release)
            if hasattr(self, "text_id"):
                self.canvas.tag_bind(self.text_id, "<ButtonPress-1>", self._on_press)
                self.canvas.tag_bind(
                    self.text_id, "<ButtonRelease-1>", self._on_release
                )

    def __setattr__(self, name, value):
        if hasattr(self, "canvas") and hasattr(self, "rectangle"):
            # self.canvas.moveto(self.text.id, self.x, self.y)
            if name == "x" or name == "y":
                self.canvas.moveto(
                    self.rectangle,
                    value if name == "x" else self.x,
                    value if name == "y" else self.y,
                )

                if name == "x":
                    delta_x = value - self.x
                else:
                    delta_x = 0
                if name == "y":
                    delta_y = value - self.y
                else:
                    delta_y = 0

                self.canvas.move(self.text_id, delta_x, delta_y)

                object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def make_rectangle(self):
        """
        Creates the polygon shape of the rectangle.

        Returns:
            The ID of the rectangle shape created on the canvas.
        """
        points = []
        if self.top_left_arc:
            # Top left arc
            for i in range(180, 271):
                a = math.radians(i)
                points.extend(
                    [
                        self.x + self.corner_radius + self.corner_radius * math.cos(a),
                        self.y + self.corner_radius + self.corner_radius * math.sin(a),
                    ]
                )
        else:
            points.extend([self.x, self.y, self.x, self.y])

        if self.top_right_arc:
            # Top right arc
            for i in range(270, 361):
                a = math.radians(i)
                points.extend(
                    [
                        self.x
                        + self.width
                        - self.corner_radius
                        + self.corner_radius * math.cos(a),
                        self.y + self.corner_radius + self.corner_radius * math.sin(a),
                    ]
                )
        else:
            points.extend([self.x + self.width, self.y])

        if self.bottom_right_arc:
            # Bottom right arc
            for i in range(0, 91):
                a = math.radians(i)
                points.extend(
                    [
                        self.x
                        + self.width
                        - self.corner_radius
                        + self.corner_radius * math.cos(a),
                        self.y
                        + self.height
                        - self.corner_radius
                        + self.corner_radius * math.sin(a),
                    ]
                )
        else:
            points.extend([self.x + self.width, self.y + self.height])

        if self.bottom_left_arc:
            # Bottom left arc
            for i in range(90, 181):
                a = math.radians(i)
                points.extend(
                    [
                        self.x + self.corner_radius + self.corner_radius * math.cos(a),
                        self.y
                        + self.height
                        - self.corner_radius
                        + self.corner_radius * math.sin(a),
                    ]
                )

        else:
            points.extend([self.x, self.y + self.height])

        if self.rect_outline:
            return self.canvas.create_polygon(
                points,
                fill=self.fill,
                width=1,
                outline=self.rect_outline,
            )
        else:
            return self.canvas.create_polygon(
                points,
                fill=self.fill,
                width=1,
            )

    def _on_press(self, event):
        """
        Event handler for the button press event.
        """
        self.canvas.configure(relief="sunken")

    def _on_release(self, event):
        """
        Event handler for the button release event.
        """
        self.canvas.configure(relief="raised")
        if self.command is not None:
            self.command()

    def move_rect(self, delta_x, delta_y):
        self.x = int(self.x + delta_x)
        self.y = int(self.y + delta_y)


class GridMaker:
    """
    A class that represents a grid maker.

    Attributes:
        parent (object): The parent object.
        canvas (object): The canvas object.
        grid_width (int): The width of the grid.
        amount_of_rectangles (int): The number of rectangles in the grid.
        rect_gap (int): The gap between rectangles.
        arcs (list): The arcs for the corners of the rectangles.
        text_data (dict): The data for the text in the rectangles.
        combined (bool): Whether the rectangles are combined.
        arcs (list): The arcs for the corners of the rectangles.
        grid_height (int): The height of the grid.
        grid_y (int): The y-coordinate of the grid.
        fill (str): The fill color of the rectangles.
    """

    def __init__(
        self,
        parent,
        canvas,
        grid_width,
        amount_of_rectangles,
        rect_gap,
        text_data,
        combined=False,
        arcs=[True, True, True, True],
        grid_height=50,
        grid_y=0,
        fill="black",
        fill_list=[],
    ):
        self.parent = parent
        self.canvas = canvas
        self.grid_width = grid_width
        self.grid_starting_x = int((self.parent.window_width - self.grid_width) / 2)
        self.grid_y = grid_y
        self.amount_of_rectangles = amount_of_rectangles
        self.rect_gap = rect_gap
        self.list_of_rectangles = []
        self.test_data = text_data
        self.combined = combined
        self.arcs = arcs
        self.grid_height = grid_height
        self.fill_list = fill_list

        self.fill = fill

        self.rect_width = (
            int(self.grid_width - (self.amount_of_rectangles - 1) * self.rect_gap)
            / self.amount_of_rectangles
        )

        self.rect_height = 50

        for i in range(self.amount_of_rectangles):
            if self.fill_list:
                rect_fill = self.fill_list[i]
            else:
                rect_fill = self.fill
            rect = RabRectangle(
                self.canvas,
                self.grid_starting_x + (i * rect_gap) + (i * self.rect_width),
                self.grid_y,
                self.rect_width,
                self.grid_height,
                10,
                rect_fill,
                text_data={
                    "string": self.test_data["string_list"][i],
                    "color": self.test_data["color"],
                    "font": self.test_data["font"],
                    "size": self.test_data["size"],
                },
                button=True,
                command=test,
                top_left_arc=self.arcs[0] if i == 0 else False,
                top_right_arc=(
                    self.arcs[1] if i == self.amount_of_rectangles - 1 else False
                ),
                bottom_left_arc=self.arcs[2] if i == 0 else False,
                bottom_right_arc=(
                    self.arcs[3] if i == self.amount_of_rectangles - 1 else False
                ),
            )
            self.list_of_rectangles.append(rect)

    def __setattr__(self, name, value):
        if hasattr(self, "canvas") and hasattr(self, "list_of_rectangles"):
            if len(self.list_of_rectangles) > 0:
                if hasattr(self, "grid_starting_x") and name == "grid_starting_x":
                    delta_x = value - self.grid_starting_x
                    object.__setattr__(self, name, value)
                    for rectangle in self.list_of_rectangles:
                        rectangle.move_rect(int(delta_x), 0)
                elif hasattr(self, "grid_y") and name == "grid_y":
                    delta_y = value - self.grid_y
                    object.__setattr__(self, name, value)
                    for rectangle in self.list_of_rectangles:
                        rectangle.move_rect(0, int(delta_y))
                else:
                    object.__setattr__(self, name, value)
            else:
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)


class Window(tk.Canvas):
    """
    Represents a custom window for the game.

    Args:
        parent (object): The parent widget.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Attributes:
        parent: The parent widget.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        rect_x = 50
        rect_y = 50
        rect_width = self.parent.window_width - 200
        rect_height = 200
        rect_radius = 40
        rect_color = "#0000FF"
        background_color = "#333333"
        cw = 2
        rect_color_rgb = hex_to_rgb(rect_color)
        background_color_rgb = hex_to_rgb(background_color)
        antialias_r = int((rect_color_rgb[0] + background_color_rgb[0] * cw) / (cw + 1))
        antialias_g = int((rect_color_rgb[1] + background_color_rgb[1] * cw) / (cw + 1))
        antialias_b = int((rect_color_rgb[2] + background_color_rgb[2] * cw) / (cw + 1))
        antialias_color_hex = rgb_to_hex(antialias_r, antialias_g, antialias_b)

        # print(f"Title-Bar is : {self.parent.title_bar_y}")
        background = RabRectangle(
            self,
            0,
            0,
            self.parent.window_width,
            self.parent.window_height - self.parent.title_bar_y,
            20,
            fill=background_color,
            top_left_arc=False,
            top_right_arc=False,
            bottom_left_arc=True,
            bottom_right_arc=True,
        )

        header_grid = GridMaker(
            self.parent,
            self,
            grid_y=50,
            grid_width=rect_width,
            amount_of_rectangles=7,
            rect_gap=2,
            fill="#CCCCCC",
            text_data={
                "string_list": [
                    "Picture",
                    "Pokèmon",
                    "Main Type",
                    "Secondary Type",
                    "Evo Stage",
                    "Height",
                    "Weight",
                ],  # TODO: Make this dynamic
                "color": "black",
                "font": "Arial",
                "size": 14,
            },
            combined=True,
            arcs=[True, True, True, True],
        )
        header_grid.grid_y = 49

        def display_guess():
            list = guess_attempt.guessed_pokemon_list
            all_results = []
            for attempt in list:
                attempt_names = [" ", attempt["guess_pokemon"]]
                attempt_results = ["gray"]
                if attempt["results"]["Correct"]:
                    attempt_results.append("green")
                else:
                    attempt_results.append("red")
                for header in guess_display_order:
                    attempt_names.append(attempt["results"][header]["guessed_value"])
                    attemp_result_value = attempt["results"][header]["result"]
                    if attemp_result_value == "True":
                        attempt_results.append("green")
                    elif attemp_result_value == "False":
                        attempt_results.append("red")
                    elif (
                        attemp_result_value == "Greater"
                        or attemp_result_value == "Less"
                    ):
                        attempt_results.append("orange")

                all_results.append([attempt_names, attempt_results])

            return all_results

        def make_grid_maker():
            list_of_guess_results = display_guess()
            for i, guess_results in enumerate(list_of_guess_results):
                grid = GridMaker(
                    self.parent,
                    self,
                    grid_y=(self.parent.window_height - 200) - (i * 51),
                    grid_width=rect_width,
                    amount_of_rectangles=len(guess_results[0]),
                    rect_gap=2,
                    fill="#CCCCCC",
                    fill_list=guess_results[1],
                    text_data={
                        "string_list": guess_results[0],
                        "color": "black",
                        "font": "Arial",
                        "size": 16,
                    },
                )

        # User Input
        entry_width = rect_width / 3
        entry_height = 45
        entry_relx = 0.47
        entry_rely = 0.92
        submit_button_x = (self.parent.window_width * entry_relx) + (entry_width / 2)
        submit_button_y = (self.parent.window_height * entry_rely) - entry_height + 1

        user_input = tk.StringVar()
        ttk.Style().configure("pad.TEntry", padding="5 1 1 1")

        entry = ttk.Entry(
            self.parent,
            font=("Arial", 16, "normal"),
            textvariable=user_input,
            style="pad.TEntry",
        )

        def replace_text(input):
            entry.delete(0, len(input))
            entry.insert(0, input)

        def make_dropdown(event, input):
            if len(input) == 1 and event.keysym == "BackSpace":
                self.dropdown_Frame.destroy()
                return

            if event == "bitch":
                name = input
            elif event.keycode == 8 or (event.keycode >= 65 and event.keycode <= 90):
                name = input + event.char if event.keycode != 8 else input[:-1]

            if name:
                pokemon_name_list = sorted(
                    [pokemon_name.lower() for pokemon_name in pokemon_data]
                )

                # Destroy existing dropdown frame if it exists
                if hasattr(self, "dropdown_Frame"):
                    self.dropdown_Frame.destroy()

                self.dropdown_Frame = tk.Frame(self)
                self.dropdown_Frame.place(
                    relx=entry_relx, rely=0.888, anchor="s"
                )

                matched_pokemon_lists = []
                for i in range(len(pokemon_name_list)):
                    if pokemon_name_list[i].startswith(name):
                        new_top = pokemon_name_list[i:]
                        pokemon_name_list[i:] = []
                        pokemon_name_list = new_top + pokemon_name_list
                        break

                for pokemon in pokemon_name_list:
                    if name.lower() in pokemon:
                        matched_pokemon_lists.append(pokemon)
                matched_pokemon_lists.reverse()

                for matched_pokemon in matched_pokemon_lists:
                    dropdown_label = tk.Label(
                        self.dropdown_Frame, text=matched_pokemon.title(), font="Arial 16", relief="groove", width=29,
                    )
                    dropdown_label.bind(
                        "<Button-1>",
                        lambda event, current_matched=matched_pokemon: replace_text(
                            current_matched.capitalize()
                        ),
                    )

                    dropdown_label.pack(side="top")

        def submit_input(input):
            print(f"Submitted: {input}")
            guess_attempt.guess(input)
            make_grid_maker()

        def entry_focused(event):
            if event.type == "9":
                make_dropdown("bitch", user_input.get())
            if event.type == "10":
                if hasattr(self, "dropdown_Frame"):
                    self.dropdown_Frame.destroy()

        entry.bind("<FocusIn>", entry_focused)
        entry.bind("<FocusOut>", entry_focused)
        entry.bind("<Key>", lambda event: make_dropdown(event, user_input.get()))
        entry.bind("<Return>", lambda event: submit_input(user_input.get()))

        # TODO: Fix submit button error
        submit_button = RabRectangle(
            self,
            submit_button_x,
            submit_button_y,
            70,
            entry_height,
            20,
            top_left_arc=False,
            bottom_left_arc=False,
            text_data={
                "string": "Submit",
                "color": "black",
                "font": "Arial",
                "size": 15,
            },
            fill="#CCCCCC",
            button=True,
            command=submit_input,
        )

        entry.place(
            relx=entry_relx,
            rely=entry_rely,
            width=entry_width,
            height=entry_height,
            anchor="center",
        )

        separator = self.create_rectangle(
            submit_button_x,
            submit_button_y,
            submit_button_x + 1,
            submit_button_y + entry_height,
            fill="black",
        )


class App(tk.Tk):
    """
    Represents the main application window.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        mouse_x (int): The x-coordinate of the mouse.
        mouse_y (int): The y-coordinate of the mouse.
        window_width (int): The width of the application window.
        window_height (int): The height of the application window.
        title_bar_y (int): The y-coordinate of the title bar.

    Methods:
        __init__(self, *args, **kwargs): Initializes the App class.
        start_move_window(self, event): Moves the window based on the mouse event coordinates.
        move_window(self, event): Moves the window based on the mouse event coordinates.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mouse_x = 0
        self.mouse_y = 0

        self.overrideredirect(True)  # turns off title bar, geometry
        self.window_width = 1280
        self.window_height = 780
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.geometry(
            f"+{int((self.winfo_screenwidth()/2)-(self.window_width/2))}+{int((self.winfo_screenheight()/2)-(self.window_height/2))}"
        )

        # self.wm_attributes("-topmost", 1)
        self.wm_attributes("-transparentcolor", "DarkOliveGreen4")
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        # TODO: How to add text to title bar/exit button without alloc error?
        title_bar_canvas = tk.Canvas(
            bd=0, highlightthickness=0, bg="DarkOliveGreen4", height=22, width=0
        )
        title_bar = RabRectangle(
            title_bar_canvas,
            0,
            0,
            self.window_width,
            22,
            20,
            fill="red",
            top_left_arc=True,
            top_right_arc=True,
            bottom_left_arc=False,
            bottom_right_arc=False,
        )

        close_button_width = 40
        close_button = RabRectangle(
            title_bar_canvas,
            self.window_width - (close_button_width * 0.8),
            0,
            close_button_width,
            close_button_width,
            25,
            fill="black",
            button=True,
            command=self.destroy,
            top_left_arc=False,
            top_right_arc=True,
            bottom_left_arc=False,
            bottom_right_arc=False,
        )

        title_bar_canvas.pack(expand=False, fill="x", side="top")  # Pack the title bar
        self.title_bar_y = (
            title_bar_canvas.winfo_reqheight()
        )  # Get the y of the title bar

        # Create an instance of WindowCanvas
        window = Window(self, bg="DarkOliveGreen4", bd=0, highlightthickness=0)
        window.pack(expand=True, fill="both", side="top")

        # bind title bar drag to the move window function
        title_bar_canvas.bind("<ButtonPress-1>", self.start_move_window)
        title_bar_canvas.bind("<B1-Motion>", self.move_window)

    def start_move_window(self, event):
        """
        Moves the window based on the mouse event coordinates.

        Args:
            event (MouseEvent): The mouse event that triggered the method.

        Returns:
            None
        """
        self.mouse_x = event.x
        self.mouse_y = event.y

    def move_window(self, event):
        """
        Moves the window based on the mouse event coordinates.

        Args:
            event (MouseEvent): The mouse event that triggered the method.

        Returns:
            None
        """
        self.geometry(f"+{event.x_root - self.mouse_x}+{event.y_root - self.mouse_y}")


App().mainloop()
