import tkinter as tk
from transformations import *

HEIGHT = 800
WIDTH = 1400
PANEL_WIDTH = 400
DRAW_SCALE = 20

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

colour_index = 0
selected_vector_idx = None
vector_buttons = []
button_idx = 0
angle = 0
draw_scale=DRAW_SCALE


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


def draw_vector(canvas: tk.Canvas, v: Vector,color=None):

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

def process_vector_buttons(button_id):
    global selected_vector_idx
    selected_vector_idx = button_id

    for button in vector_buttons:
        button.config(bg="white")

    vector_buttons[button_id].config(bg=Vector.all_vectors[button_id].color)


def create_vector(root, x_entry, y_entry, x_label, y_label, button, canvas):
    global button_idx

    x = x_entry.get().strip()
    y = y_entry.get().strip()

    if not x or not y:
        return

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
        text=f"vector {current_idx + 1}",
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


def start_rotation(canvas, entry_angle, label, rotate_btn):
    global angle

    text_angle = entry_angle.get().strip()

    if selected_vector_idx is None or not text_angle:
        print("Vector not selected or angle input empty!")
        return

    angle = 0

    entry_angle.pack_forget()
    label.pack_forget()
    rotate_btn.pack_forget()

    base_vector = Vector.all_vectors[selected_vector_idx]
    start_components = base_vector.components[:]  # snapshot of current state

    animate_vector_rotation(
        canvas=canvas,
        target_angle=float(text_angle),
        base_vector=base_vector,
        start_components=start_components,
    )


def animate_vector_rotation(canvas, target_angle, base_vector, start_components):
    global angle

    angle += 2

    temp_vector = Vector(start_components[:])
    rotated_vector = rotate_vector(temp_vector, angle)

    end_x, end_y = rotated_vector.components
    sx, sy = world_to_screen(end_x, end_y, draw_scale)

    canvas.coords(
        base_vector.vector_id,
        screen_origin[0],
        screen_origin[1],
        sx,
        sy,
    )

    if angle >= target_angle:
        final_temp = Vector(start_components[:])
        final_vector = rotate_vector(final_temp, target_angle)

        # update the SAME original vector object
        base_vector.components = final_vector.components[:]

        update_vector_on_canvas(canvas, base_vector)
        return

    canvas.after(
        20,
        lambda: animate_vector_rotation(
            canvas, target_angle, base_vector, start_components
        ),
    )


def process_scale(canvas, text_scale_x, text_scale_y, x_label, y_label, scale_btn):
    if selected_vector_idx is None:
        print("please select a vector")
        return

    x_scale = text_scale_x.get().strip()
    y_scale = text_scale_y.get().strip()

    if not x_scale or not y_scale:
        print("Enter both scale values")
        return

    selected_vector = Vector.all_vectors[selected_vector_idx]

    scaled_vector = scale_vector(
        selected_vector,
        sx=float(x_scale),
        sy=float(y_scale),
    )

    # update same vector object so future rotations use scaled values
    selected_vector.components = scaled_vector.components[:]

    update_vector_on_canvas(canvas, selected_vector)

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

def display_vector_reflection(canvas,label,x_btn,y_btn,axis=None):

  
    if axis==1:
        
        new_vector=reflect_on_x_axis(Vector.all_vectors[selected_vector_idx])

        Vector.all_vectors[selected_vector_idx].components=new_vector.components

        update_vector_on_canvas(canvas,new_vector)



    elif axis == 0:

        new_vector=reflect_on_y_axis(Vector.all_vectors[selected_vector_idx])

        Vector.all_vectors[selected_vector_idx].components=new_vector.components

        update_vector_on_canvas(canvas,new_vector)
    
    x_btn.pack_forget()
    y_btn.pack_forget()
    label.pack_forget()

def get_reflection_axis(root,canvas):
    
    if selected_vector_idx ==None:
        print("please select a vector")
        return  
    label=tk.Label(root,text="select axis")

    x_btn=tk.Button(root,text="x-axis",width=200)
    y_btn=tk.Button(root,text="y-axis",width=200)
    label.pack(side="top")
    x_btn.pack(padx=2,pady=5,side="top")
    y_btn.pack(padx=2,pady=5,side="top")

    x_btn.config(command=lambda : display_vector_reflection(canvas,label,x_btn,y_btn,axis=1))
    y_btn.config(command=lambda : display_vector_reflection(canvas,label,x_btn,y_btn,axis=0))

def update_slider_value(canvas, slider_value):
    
    global draw_scale, screen_origin
    
    draw_scale = float(slider_value)
    
    screen_origin = world_to_screen(0, 0, draw_scale)
    
    colors=[]
    for v in Vector.all_vectors:
        colors.append(v.color)

    canvas.delete("all")
    draw_coordinate_plane(canvas, draw_scale)
   

    for i,v in enumerate(Vector.all_vectors):
        draw_vector(canvas, v,colors[i])
        

def main():
    root = tk.Tk()
    root.title("Linear Algebra Visualizer")
    root.geometry(f"{WIDTH}x{HEIGHT}")

    canvas = tk.Canvas(root, width=WIDTH - PANEL_WIDTH, height=HEIGHT, bg="black")
    canvas.pack(side="left", padx=2)

    draw_coordinate_plane(canvas, DRAW_SCALE)

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
    add.pack(side="top", pady=5, padx=2)

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
    rotate_btn.pack(side="top", pady=5, padx=2)

    scale_btn = tk.Button(
        root,
        width=PANEL_WIDTH,
        height=2,
        text="Scale vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: get_scale_factor(root, canvas),
    )
    scale_btn.pack(side="top", pady=5, padx=2)

    reflect_btn = tk.Button(
        root,
        width=PANEL_WIDTH,
        height=2,
        text="reflect vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: get_reflection_axis(root, canvas),
    )
    reflect_btn.pack(side="top", pady=5, padx=2)
    zoom=tk.Scale(root,resolution=1,from_=5,to=50,orient=tk.HORIZONTAL)
    zoom.config(command=lambda v:update_slider_value(canvas,v))
    zoom.pack(side="top",padx=2,pady=5)
    zoom.set(20)
    root.mainloop()


if __name__ == "__main__":
    main()