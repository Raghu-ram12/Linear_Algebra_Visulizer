
from state import * 
from transformations import * 
from tkinter import * 
import tkinter as tk

def world_to_screen(x, y, scale):
    x_screen = scale * x + (WIDTH - PANEL_WIDTH) / 2
    y_screen = scale * (-y) + HEIGHT / 2
    return (x_screen, y_screen)



screen_origin = world_to_screen(0, 0, draw_scale)


def draw_coordinate_plane(canvas, scale):
    offset = 10
    canvas_width = WIDTH - PANEL_WIDTH
    center_x = canvas_width / 2
    center_y = HEIGHT / 2

    x = center_x
    while x >= 0:
        canvas.create_line(x, offset, x, HEIGHT - offset, fill="light grey", width=0.2)
        x -= scale

    x = center_x + scale
    while x <= canvas_width:
        canvas.create_line(x, offset, x, HEIGHT - offset, fill="light grey", width=0.2)
        x += scale

    y = center_y
    while y >= 0:
        canvas.create_line(
            offset, y, canvas_width - offset, y, fill="light grey", width=0.2
        )
        y -= scale

    y = center_y + scale
    while y <= HEIGHT:
        canvas.create_line(
            offset, y, canvas_width - offset, y, fill="light grey", width=0.2
        )
        y += scale

    canvas.create_line(
        offset,
        center_y,
        canvas_width - offset,
        center_y,
        fill="blue",
        width=2,
        arrow=tk.BOTH,
    )
    canvas.create_line(
        center_x,
        offset,
        center_x,
        HEIGHT - offset,
        fill="blue",
        width=2,
        arrow=tk.BOTH,
    )


def update_vector_on_canvas(canvas, v):
    x, y = v.components[0], v.components[1]
    x_screen, y_screen = world_to_screen(x, y, draw_scale)
    canvas.coords(
        v.vector_id,
        screen_origin[0],
        screen_origin[1],
        x_screen,
        y_screen,
    )


def draw_vector_on_canvas(canvas: tk.Canvas, v: Vector, color=None):

    global colour_index

    x = v.components[0]
    y = v.components[1]
    vector_position = world_to_screen(x, y, draw_scale)

    if not color:
        color_to_use = canvas_colors[colour_index]
        v.color = canvas_colors[colour_index]
        colour_index = (colour_index + 1) % len(canvas_colors)
    else:
        color_to_use = color
        v.color = color

    vector_id = canvas.create_line(
        screen_origin[0],
        screen_origin[1],
        vector_position[0],
        vector_position[1],
        fill=color_to_use,
        arrow=tk.LAST,
        width=2,
    )

    v.vector_id = vector_id



def update_slider_value(canvas, slider_value):

    global draw_scale, screen_origin

    draw_scale = float(slider_value)

    screen_origin = world_to_screen(0, 0, draw_scale)

    colors = []

    for v in Vector.all_vectors:
        colors.append(v.color)

    canvas.delete("all")

    draw_coordinate_plane(canvas, draw_scale)

    for i, v in enumerate(Vector.all_vectors):
        draw_vector_on_canvas(canvas, v, colors[i])



