import tkinter as tk
from transformations import *

HEIGHT = 800
WIDTH = 1400
PANEL_WIDTH = 400

canvas_colors = [
    "crimson",
    "dodger blue",
    "forest green",
    "gold",
    "dark orchid",
    "dark orange",
    "turquoise",
    "hot pink",
    "slate gray",
    "saddle brown",
]


def world_to_screen(x, y, Scale):
    x_screen = Scale * x + (WIDTH - PANEL_WIDTH) / 2
    y_screen = Scale * (-y) + HEIGHT / 2
    return (x_screen, y_screen)


import tkinter as tk


def draw_coordinate_plane(canvas, scale):

    offset = 10
    canvas_width = WIDTH - PANEL_WIDTH
    center_x = canvas_width / 2
    center_y = HEIGHT / 2

    x = center_x
    while x >= 0:
        canvas.create_line(x, offset, x, HEIGHT - offset, fill="light grey", width=1)
        x -= scale

    x = center_x + scale
    while x <= canvas_width:
        canvas.create_line(x, offset, x, HEIGHT - offset, fill="light grey", width=1)
        x += scale

    y = center_y
    while y >= 0:
        canvas.create_line(
            offset, y, canvas_width - offset, y, fill="light grey", width=1
        )
        y -= scale

    y = center_y + scale
    while y <= HEIGHT:
        canvas.create_line(
            offset, y, canvas_width - offset, y, fill="light grey", width=1
        )
        y += scale

    # 3. Draw main axes on top of the grid
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
        center_x, offset, center_x, HEIGHT - offset, fill="blue", width=2, arrow=tk.BOTH
    )


colour_index = 0
selected_vector = None
screen_origin = world_to_screen(0, 0, 20)
vector_buttons = []
button_idx = 0


def draw_vector(canvas: tk.Canvas, v: Vector):
    global colour_index
    x = v.components[0]
    y = v.components[1]
    vector_position = world_to_screen(x, y, 20)
    vector_id = canvas.create_line(
        screen_origin[0],
        screen_origin[1],
        vector_position[0],
        vector_position[1],
        fill=canvas_colors[colour_index],
        arrow=tk.LAST,
        width=2,
    )
    v.color = canvas_colors[colour_index]
    colour_index = (colour_index + 1) % len(canvas_colors)
    v.vector_id = vector_id


def process_vector_buttons(button_id):

    global selected_vector

    selected_vector = Vector.all_vectors[button_id]

    for button in vector_buttons:
        button.config(bg="white")

    vector_buttons[button_id].config(bg=selected_vector.color)

    print(selected_vector.components)


def create_vector(root, x_entry, y_entry, x_label, y_label, button, canvas):
    global button_idx
    x = x_entry.get()
    y = y_entry.get()

    if not x or not y:
        return  # Guard against empty fields

    x_entry.pack_forget()
    y_entry.pack_forget()
    x_label.pack_forget()
    y_label.pack_forget()
    button.pack_forget()

    v = Vector([float(x), float(y)])

    current_idx = button_idx
    vector_btn = tk.Button(
        root,
        width=PANEL_WIDTH,
        relief="solid",
        padx=2,
        pady=2,
        text=f"vector {current_idx+1}",
        command=lambda idx=current_idx: process_vector_buttons(idx),
    )
    button_idx += 1
    vector_btn.pack(side="top")
    vector_buttons.append(vector_btn)
    draw_vector(canvas, v)


def add_vector_to_ui(root, canvas):

    x_label = tk.Label(root, text="x component")
    x_label.pack(side="top", pady=5)
    x_text = tk.Entry(root, width=PANEL_WIDTH)
    x_text.pack(side="top", pady=5)

    y_label = tk.Label(root, text="y component")
    y_label.pack(side="top", pady=5)
    y_text = tk.Entry(root, width=PANEL_WIDTH)
    y_text.pack(side="top", pady=5)

    submit_btn = tk.Button(
        root,
        width=10,
        borderwidth=1,
        relief="solid",
        padx=2,
        pady=2,
        text="submit",
        command=lambda: create_vector(
            root, x_text, y_text, x_label, y_label, submit_btn, canvas
        ),
    )
    submit_btn.pack(side="top", pady=5)


def get_rotation_angle(root, canvas):

    label = tk.Label(root, text="angle of rotation")
    label.pack(side="top", pady=5)
    entry_angle = tk.Entry(root, width=PANEL_WIDTH)
    entry_angle.pack(side="top")

    # We read the entry inside the command function, ONLY when the user clicks the button
    rotate_btn = tk.Button(
        root,
        text="rotate",
        width=PANEL_WIDTH,
        relief="solid",
        borderwidth=1,
        padx=2,
        pady=2,
    )
    rotate_btn.config(
        command=lambda: start_rotation(canvas, entry_angle, label, rotate_btn)
    )
    rotate_btn.pack(side="top", pady=5)


angle = 0


def start_rotation(canvas, entry_angle, label, rotate_btn):
    text_angle = entry_angle.get()
    if not text_angle or not selected_vector:
        print("Vector not selected or angle input empty!")
        return

    global angle
    angle = 0
    entry_angle.pack_forget()
    label.pack_forget()
    rotate_btn.pack_forget()
    animate_vector_rotation(
        canvas, target_angle=float(text_angle), base_vector=selected_vector
    )


def process_scale(canvas, text_scale_x, text_scale_y, x_label, y_label, scale_btn):

    if not selected_vector:
        print("please select a vector")

    x_scale = text_scale_x.get()
    y_scale = text_scale_y.get()

    scaled_vector = scale_vector(selected_vector, sx=float(x_scale), sy=float(y_scale))
    idx=Vector.all_vectors[selected_vector]
    Vector.all_vectors[idx].components=selected_vector.components
    screen_cords = world_to_screen(
        scaled_vector.components[0], scaled_vector.components[1], 20
    )
    canvas.coords(
        selected_vector.vector_id,
        screen_origin[0],
        screen_origin[1],
        screen_cords[0],
        screen_cords[1],
    )

    text_scale_x.pack_forget()
    text_scale_y.pack_forget()
    x_label.pack_forget()
    y_label.pack_forget()
    scale_btn.pack_forget()


def get_scale_factor(root, canvas):

    text_scale_x = tk.Entry(root, width=PANEL_WIDTH)

    x_label = tk.Label(root, text="x scale")

    text_scale_y = tk.Entry(root, width=PANEL_WIDTH)

    y_label = tk.Label(root, text="y scale")

    x_label.pack(side="top")
    text_scale_x.pack(side="top")
    y_label.pack(side="top")
    text_scale_y.pack(side="top")

    scale_btn = tk.Button(
        root,
        text="scale",
        width=PANEL_WIDTH,
        relief="solid",
        borderwidth=1,
        padx=2,
        pady=2,
        command=lambda: process_scale(
            canvas, text_scale_x, text_scale_y, x_label, y_label, scale_btn
        ),
    )
    scale_btn.pack(side="top")


def animate_vector_rotation(canvas, target_angle, base_vector):
    global selected_vector
    global angle

    angle += 2

    rotated_vector = rotate_vector(base_vector, angle)
    x_new = rotated_vector.components[0]
    y_new = rotated_vector.components[1]
    screen_target = world_to_screen(x_new, y_new, 30)

    canvas.coords(
        base_vector.vector_id,
        screen_origin[0],
        screen_origin[1],
        screen_target[0],
        screen_target[1],
    )

    if angle >= target_angle:
        # Snap completely to terminal position and assign state global variables
        final_vector = rotate_vector(base_vector, target_angle)
        final_target = world_to_screen(
            final_vector.components[0], final_vector.components[1], 30
        )
        canvas.coords(
            base_vector.vector_id,
            screen_origin[0],
            screen_origin[1],
            final_target[0],
            final_target[1],
        )
        base_vector.components = final_vector.components
        return

    canvas.after(20, lambda: animate_vector_rotation(canvas, target_angle, base_vector))


def main():
    root = tk.Tk()
    root.title("Linear Algebra Visualizer")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    canvas = tk.Canvas(root, width=WIDTH - PANEL_WIDTH, height=HEIGHT, bg="black")
    canvas.pack(side="left",padx=2)
    draw_coordinate_plane(canvas, 20)

    add = tk.Button(
        root,
        width=PANEL_WIDTH,
        height=2,
        text="Add vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: add_vector_to_ui(root, canvas),
    )
    add.pack(side="top",pady=5,padx=2)

    rotate_btn = tk.Button(
        root,
        width=PANEL_WIDTH,
        height=2,
        text="Rotate vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: get_rotation_angle(root, canvas),
    )
    rotate_btn.pack(side="top", pady=5,padx=2)

    scale_btn = tk.Button(
        root,
        width=PANEL_WIDTH,
        height=2,
        text="scale vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: get_scale_factor(root, canvas),
    )
    scale_btn.pack(side="top", pady=5,padx=2)

    root.mainloop()


if __name__ == "__main__":
    main()
