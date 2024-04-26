import tkinter as tk
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
    "number",
    "type_main",
    "type_secondary",
    "evolution_stage",
    "height",
    "weight",
]


def resizeImage(image, width=False, height=False, resize_resolution=10):
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
    def __init__(self, correct_pokemon):
        self.correct_pokemon = correct_pokemon
        self.guessed_pokemon_list = []

    def compare_range(self, guessed_value, key):
        correct_value = self.correct_pokemon.key(key)
        if correct_value == guessed_value:
            return "Equal"
        if correct_value > guessed_value:
            return "Greater"
        if correct_value < guessed_value:
            return "Less"
        return "Error"

    def compare_boolean(self, guessed_value, key):
        if self.correct_pokemon.key(key) == guessed_value:
            return True
        else:
            return False

    def guess_display(self):
        # display = []
        for guessed_pokemon in self.guessed_pokemon_list:
            for category in guess_display_order:
                print(category)
                if guessed_pokemon["results"]["Correct"]:
                    print("Correct")
                else:

                    print(guessed_pokemon["results"][category])
                print("\n")

    def guess(self, guessed_pokemon_name):
        result = {}
        guessed_pokemon = Pokemon(
            (guessed_pokemon_name, pokemon_data[guessed_pokemon_name])
        )
        # print(guessed_pokemon)
        if self.correct_pokemon.number == guessed_pokemon.number:
            result = {"Correct": True}
        else:
            result = {"Correct": False}
            for key, value in better_pokemon_data_keys_dict.items():
                guessed_value = guessed_pokemon.key(key)
                if value["data_type"] == "range":
                    result[key] = {
                        "guessed_value": guessed_value,
                        "result": self.compare_range(guessed_value, key),
                    }
                elif value["data_type"] == "boolean":
                    result[key] = {
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
        # self.guess_display()
        # return self.guessed_pokemon_list


class Pokemon:
    def __init__(self, pokemon_tuple):
        self.name = pokemon_tuple[0]
        self.data = pokemon_tuple[1]

    def __getattr__(self, attr_name):
        return self.data[better_pokemon_data_keys_dict[attr_name]["key"]]

    def key(self, key):
        return self.data[better_pokemon_data_keys_dict[key]["key"]]


# Load Pokemon data
with open("Pokemon.json", encoding="utf-8") as file:
    pokemon_data = json.load(file)

# Select a random Pokemon
pokemon_data = pokemon_data[0]
# target_pokemon = random.choice(list(pokemon_data.items()))
target_pokemon = ("Bulbasaur", pokemon_data["Bulbasaur"])
# print(target_pokemon)
correctPokemon = Pokemon(target_pokemon)
# print(f"Correct Pokemon: {correctPokemon.name}")

# Create a Guess object
guess = Guess(correctPokemon)

# guess.guess("Bulbasaur")


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
            print(f'Creating Text: {self.text_data["string"]}')
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

    def make_rectangle(self):
        points = []
        if self.top_left_arc:
            # print("Top Left Arc")
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
            # print("Top Left No Arc")
            points.extend([self.x, self.y, self.x, self.y])

        # points.extend([self.x + self.width, self.y])  # Top right corner
        # print("Top Right Corner")

        if self.top_right_arc:
            # Top right arc
            # print("Top Right Arc")
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
            # print("Top Right No Arc")
            points.extend([self.x + self.width, self.y])

        # points.extend(
        #     [self.x + self.width, self.y + self.height]
        # )  # Bottom right corner
        # print("Bottom Right Corner")

        if self.bottom_right_arc:
            # Bottom right arc
            # print("Bottom Right Arc")
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
            # print("Bottom Right No Arc")
            points.extend([self.x + self.width, self.y + self.height])

        # points.extend([self.x, self.y + self.height])  # Bottom left corner
        # print("Bottom Left Corner")

        if self.bottom_left_arc:
            # Bottom left arc
            # print("Bottom Left Arc")
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
            # print("Bottom Left No Arc")
            points.extend([self.x, self.y + self.height])

        # points.extend([self.x, self.y])  # Top left corner
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
        self.canvas.configure(relief="sunken")

    def _on_release(self, event):
        self.canvas.configure(relief="raised")
        if self.command is not None:
            self.command()


class GridMaker:
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
        fill="black"
    ):
        self.parent = parent
        self.canvas = canvas
        self.grid_width = grid_width
        self.grid_starting_x = (self.parent.window_width - self.grid_width) / 2
        self.amount_of_rectangles = amount_of_rectangles
        self.rect_gap = rect_gap
        self.list_of_rectangles = []
        self.test_data = text_data
        self.combined = combined
        self.arcs = arcs
        self.grid_height = grid_height
        self.grid_y = grid_y
        self.fill = fill

        self.rect_width = (
            self.grid_width - (self.amount_of_rectangles - 1) * self.rect_gap
        ) / self.amount_of_rectangles

        self.rect_height = 50

        for i in range(self.amount_of_rectangles):
            rect = RabRectangle(
                self.canvas,
                (self.grid_starting_x + (i * rect_gap) + (i * self.rect_width)),
                self.grid_y,
                self.rect_width,
                self.grid_height,
                10,
                self.fill,
                text_data={
                    "string": self.test_data["string_list"][i],
                    "color": self.test_data["color"],
                    "font": self.test_data["font"],
                    "size": 16,
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


class Window(tk.Canvas):
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

        # print(f"Title-Bar is : {self.parent.title_bar_height}")
        background = RabRectangle(
            self,
            0,
            0,
            self.parent.window_width,
            self.parent.window_height - self.parent.title_bar_height,
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
            amount_of_rectangles=6,
            rect_gap=2,
            fill="#CCCCCC",
            text_data={
                "string_list": ["Pokèdex Number","Main Type","Secondary Type","Evolution Stage","Height","Weight"], #Should this be dynamic? I assume we can be lazy and leave it literal
                "color": "black",
                "font": "Arial",
                "size": 16,
            },
            combined=True,
            arcs=[True, True, True, True],
        )
        # Let's do this with Rab ! Logic: How to make a multi-row grid to fit all guesses? Need to add functions to GridMaker? Or append and shift all guesses after each guess?
        guesses_grid = GridMaker(
            self.parent,
            self,
            grid_y=self.parent.window_height - 230,
            grid_width=rect_width,
            amount_of_rectangles=4,
            rect_gap=2,
            text_data={
                "string_list": ["Rawr", "Hehe", "X3", "uwu"],
                "color": "black",
                "font": "Arial",
                "size": 16,
            },
        )
        '''<---------------------------------------------------- COMMENTED OUT BIG BOX IN CENTRE : SHOULD CHANGE BOX TO POKEMON PICTURE ---------------------------------------------------->
        test_rect = RabRectangle(
            self,
            self.parent.window_width / 2 - rect_width / 2,
            self.parent.window_height / 2 - rect_height / 2,
            rect_width,
            rect_height,
            rect_radius,
            text_data={
                "string": "Test",
                "color": "black",
                "font": "Arial",
                "size": 16,
            },
            fill=rect_color,
            button=True,
            command=test,
        )'''

        # User Input
        entry = tk.Entry(self.parent, bd=0, font=("Arial",16,"normal"), fg="#999999", bg="#CCCCCC")

        entry_width = rect_width / 3
        entry_height = 45
        entry_relx = 0.47
        entry_rely = 0.92
        submit_button_x = (self.parent.window_width * entry_relx) + (entry_width / 2)
        submit_button_y = (self.parent.window_height * entry_rely) - entry_height + 1

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
            command=lambda: print("Submit Button Pressed"),
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
        # <---------------------------------------------------------- How to add text to title bar/exit button without alloc error? ---------------------------------------------------------->
        title_bar = tk.Canvas(
            bd=0, highlightthickness=0, bg="DarkOliveGreen4", height=22, width=0
        )
        RabRectangle(
            title_bar,
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

        # title_bar = tk.Frame(self, bg="red", height=0, bd=0)
        close_button_width = 40
        close_button = RabRectangle(
            title_bar,
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
        # close_button.pack(side="right")

        # pack the widgets
        title_bar.pack(expand=False, fill="x", side="top")
        self.title_bar_height = title_bar.winfo_reqheight()
        # print(f"Title-Bar is : {self.title_bar_height}")

        # Create an instance of WindowCanvas
        window = Window(self, bg="DarkOliveGreen4", bd=0, highlightthickness=0)
        window.pack(expand=True, fill="both", side="top")

        # bind title bar motion to the move window function
        title_bar.bind("<ButtonPress-1>", self.start_move_window)
        title_bar.bind("<B1-Motion>", self.move_window)

    def start_move_window(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def move_window(self, event):
        self.geometry(f"+{event.x_root - self.mouse_x}+{event.y_root - self.mouse_y}")


App().mainloop()
