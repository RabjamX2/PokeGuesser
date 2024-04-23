import tkinter as tk
import math
import json
import random

better_pokemon_data_keys_dict = {
    "name": {"key": "Pokemon", "data_type": "boolean"},
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
    "name",
    "type_main",
    "type_secondary",
    "evolution_stage",
    "height",
    "weight",
]


class Guess:
    def __init__(self, correct_pokemon):
        self.correct_pokemon = correct_pokemon
        self.guessed_pokemon_list = []

    def compare_range(self, guessed_value, key):
        correct_value = self.correct_pokemon.key(key)
        if correct_value == guessed_value:
            return "Equal"
        if correct_value > guessed_value:
            return "Less"
        if correct_value < guessed_value:
            return "Greater"
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
                print(guessed_pokemon["results"][category])
                print("\n")

    def guess(self, guessed_pokemon):
        result = {}
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
        self.guess_display()
        # return self.guessed_pokemon_list


class Pokemon:
    def __init__(self, json_data):
        self.data = json_data

    def __getattr__(self, attr_name):
        return self.data[better_pokemon_data_keys_dict[attr_name]["key"]]

    def key(self, key):
        return self.data[better_pokemon_data_keys_dict[key]["key"]]


# Load Pokemon data
with open("Pokemon.json", encoding="utf-8") as file:
    pokemon_data = json.load(file)

# Select a random Pokemon
target_pokemon = random.choice(pokemon_data)
print(target_pokemon["#"], target_pokemon["Pokemon"])
correctPokemon = Pokemon(target_pokemon)

# Create a Guess object
guess = Guess(correctPokemon)


def hex_to_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return "#%02x%02x%02x" % (red, green, blue)


class RoundedButton(tk.Canvas):
    def __init__(
        self, parent, width, height, cornerradius, padding, color, bg, command=None
    ):
        tk.Canvas.__init__(
            self,
            parent,
            bd=0,
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            bg=bg,
        )
        self.command = command

        if cornerradius > 0.5 * width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5 * height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2 * cornerradius

        def shape():
            self.create_polygon(
                (
                    padding,
                    height - cornerradius - padding,
                    padding,
                    cornerradius + padding,
                    padding + cornerradius,
                    padding,
                    width - padding - cornerradius,
                    padding,
                    width - padding,
                    cornerradius + padding,
                    width - padding,
                    height - cornerradius - padding,
                    width - padding - cornerradius,
                    height - padding,
                    padding + cornerradius,
                    height - padding,
                ),
                fill=color,
                outline=color,
            )
            self.create_arc(
                (padding, padding + rad, padding + rad, padding),
                start=90,
                extent=90,
                fill=color,
                outline=color,
            )
            self.create_arc(
                (width - padding - rad, padding, width - padding, padding + rad),
                start=0,
                extent=90,
                fill=color,
                outline=color,
            )
            self.create_arc(
                (
                    width - padding,
                    height - rad - padding,
                    width - padding - rad,
                    height - padding,
                ),
                start=270,
                extent=90,
                fill=color,
                outline=color,
            )
            self.create_arc(
                (padding, height - padding - rad, padding + rad, height - padding),
                start=180,
                extent=90,
                fill=color,
                outline=color,
            )

        shape()
        (x0, y0, x1, y1) = self.bbox("all")
        width = x1 - x0
        height = y1 - y0
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def rounded_rect(self, x, y, w, h, c):
        self.create_arc(x, y, x + 2 * c, y + 2 * c, start=90, extent=90, style="arc")
        self.create_arc(
            x + w - 2 * c,
            y + h - 2 * c,
            x + w,
            y + h,
            start=270,
            extent=90,
            style="arc",
        )
        self.create_arc(
            x + w - 2 * c, y, x + w, y + 2 * c, start=0, extent=90, style="arc"
        )
        self.create_arc(
            x, y + h - 2 * c, x + 2 * c, y + h, start=180, extent=90, style="arc"
        )
        self.create_line(x + c, y, x + w - c, y)
        self.create_line(x + c, y + h, x + w - c, y + h)
        self.create_line(x, y + c, x, y + h - c)
        self.create_line(x + w, y + c, x + w, y + h - c)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()


class RoundedBox(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, bg):
        tk.Canvas.__init__(
            self, parent, borderwidth=0, relief="flat", highlightthickness=0, bg=bg
        )

        if cornerradius > 0.5 * width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5 * height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2 * cornerradius

        def shape():
            self.create_polygon(
                (
                    padding,
                    height - cornerradius - padding,
                    padding,
                    cornerradius + padding,
                    padding + cornerradius,
                    padding,
                    width - padding - cornerradius,
                    padding,
                    width - padding,
                    cornerradius + padding,
                    width - padding,
                    height - cornerradius - padding,
                    width - padding - cornerradius,
                    height - padding,
                    padding + cornerradius,
                    height - padding,
                ),
                fill=color,
                outline=color,
            )
            self.create_arc(
                (padding, padding + rad, padding + rad, padding),
                start=90,
                extent=90,
                fill=color,
                outline=color,
            )
            self.create_arc(
                (width - padding - rad, padding, width - padding, padding + rad),
                start=0,
                extent=90,
                fill=color,
                outline=color,
            )
            self.create_arc(
                (
                    width - padding,
                    height - rad - padding,
                    width - padding - rad,
                    height - padding,
                ),
                start=270,
                extent=90,
                fill=color,
                outline=color,
            )
            self.create_arc(
                (padding, height - padding - rad, padding + rad, height - padding),
                start=180,
                extent=90,
                fill=color,
                outline=color,
            )

        shape()
        (x0, y0, x1, y1) = self.bbox("all")
        width = x1 - x0
        height = y1 - y0
        self.configure(width=width, height=height)


def test():
    print("Hello")


class Window(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        # button = RoundedButton(self, 200, 100, 50, 2, "red", None, command=test)
        # button.place(relx=0.1, rely=0.1)

        rect_x = 50
        rect_y = 50
        rect_width = 150
        rect_height = 200
        rect_radius = 40
        rect_color = "#0000FF"
        background_color = "#FFFF00"
        cw = 2
        rect_color_rgb = hex_to_rgb(rect_color)
        background_color_rgb = hex_to_rgb(background_color)
        antialias_r = int((rect_color_rgb[0] + background_color_rgb[0] * cw) / (cw + 1))
        antialias_g = int((rect_color_rgb[1] + background_color_rgb[1] * cw) / (cw + 1))
        antialias_b = int((rect_color_rgb[2] + background_color_rgb[2] * cw) / (cw + 1))
        antialias_color_hex = rgb_to_hex(antialias_r, antialias_g, antialias_b)

        self.rounded_rect_polygon(
            rect_x,
            rect_y,
            rect_width,
            rect_height,
            rect_radius,
            fill=rect_color,
        )

        self.rounded_rect(
            rect_x + 200,
            rect_y,
            rect_width,
            rect_height,
            rect_radius,
            fill=antialias_color_hex,
            width=1.5,
        )

        self.rounded_rect_polygon(
            rect_x + 200, rect_y, rect_width, rect_height, rect_radius, fill=rect_color
        )

    def rounded_rect(self, x, y, w, h, c, fill, width=1):
        """
        Draws a rounded rectangle with the ability to change the thickness and color of the lines.

        Args:
            x (int): X-coordinate of the top-left corner of the rectangle.
            y (int): Y-coordinate of the top-left corner of the rectangle.
            w (int): Width of the rectangle.
            h (int): Height of the rectangle.
            c (int): Radius of the corners.
            fill (str, optional): Color of the rectangle's fill. Defaults to "black".
            width (int, optional): Thickness of the rectangle's fill. Defaults to 1.
        """
        self.create_arc(
            x,
            y,
            x + 2 * c,
            y + 2 * c,
            start=90,
            extent=90,
            style="arc",
            outline=fill,
            width=width,
        )
        self.create_arc(
            x + w - 2 * c,
            y + h - 2 * c,
            x + w,
            y + h,
            start=270,
            extent=90,
            style="arc",
            outline=fill,
            width=width,
        )
        self.create_arc(
            x + w - 2 * c,
            y,
            x + w,
            y + 2 * c,
            start=0,
            extent=90,
            style="arc",
            outline=fill,
            width=width,
        )
        self.create_arc(
            x,
            y + h - 2 * c,
            x + 2 * c,
            y + h,
            start=180,
            extent=90,
            style="arc",
            outline=fill,
            width=width,
        )
        self.create_line(x + c, y, x + w - c, y, fill=fill, width=width)
        self.create_line(x + c, y + h, x + w - c, y + h, fill=fill, width=width)
        self.create_line(x, y + c, x, y + h - c, fill=fill, width=width)
        self.create_line(x + w, y + c, x + w, y + h - c, fill=fill, width=width)

    def rounded_rect_polygon(self, x, y, w, h, c, fill, **kwargs):
        points = []

        # Top left arc
        for i in range(180, 271):
            a = math.radians(i)
            points.extend([x + c + c * math.cos(a), y + c + c * math.sin(a)])

        points.extend([x + w, y])  # Top right corner

        # Top right arc
        for i in range(270, 361):
            a = math.radians(i)
            points.extend([x + w - c + c * math.cos(a), y + c + c * math.sin(a)])

        points.extend([x + w, y + h])  # Bottom right corner

        # Bottom right arc
        for i in range(0, 91):
            a = math.radians(i)
            points.extend([x + w - c + c * math.cos(a), y + h - c + c * math.sin(a)])

        points.extend([x, y + h])  # Bottom left corner

        # Bottom left arc
        for i in range(90, 181):
            a = math.radians(i)
            points.extend([x + c + c * math.cos(a), y + h - c + c * math.sin(a)])

        points.extend([x, y])  # Top left corner

        self.create_polygon(points, fill=fill, smooth=1, splinesteps=1, **kwargs)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mouse_x = 0
        self.mouse_y = 0

        self.overrideredirect(True)  # turns off title bar, geometry
        self.geometry("500x500")
        self.wm_attributes("-topmost", 1)
        self.wm_attributes("-transparentcolor", "DarkOliveGreen4")

        title_bar = tk.Frame(self, bg="red", height=0, bd=0)
        close_button = tk.Button(
            title_bar, text=" X ", command=self.destroy, bd=0, bg="red"
        )
        close_button.pack(side="right")

        # pack the widgets
        title_bar.pack(expand=False, fill="x", side="top")

        # Create an instance of WindowCanvas
        window = Window(self, bg="yellow", bd=0, highlightthickness=0)
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
