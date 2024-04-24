import tkinter as tk
import math


class Window(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

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
        # self.create_line(x + c, y, x + w - c, y, fill=fill, width=width)
        # self.create_line(x + c, y + h, x + w - c, y + h, fill=fill, width=width)
        # self.create_line(x, y + c, x, y + h - c, fill=fill, width=width)
        # self.create_line(x + w, y + c, x + w, y + h - c, fill=fill, width=width)

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
