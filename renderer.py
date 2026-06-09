import tkinter as tk
import math # Used as placeholder for transformations logic if needed

class Vector:
    all_vectors = []
    def __init__(self, components):
        self.components = components
        self.color = "white"
        self.vector_id = None
        Vector.all_vectors.append(self)

def rotate_vector(vector, angle_degrees):
    # Standard 2D rotation matrix math
    rad = math.radians(angle_degrees)
    x, y = vector.components[0], vector.components[1]
    x_new = x * math.cos(rad) - y * math.sin(rad)
    y_new = x * math.sin(rad) + y * math.cos(rad)
    return Vector([x_new, y_new])


HEIGHT = 800
WIDTH = 1400
PANEL_WIDTH = 400 

canvas_colors = [
    "crimson", "dodger blue", "forest green", "gold", "dark orchid",
    "dark orange", "turquoise", "hot pink", "slate gray", "saddle brown"
]

def world_to_screen(x, y, Scale):
    x_screen = Scale * x + (WIDTH - PANEL_WIDTH) / 2
    y_screen = Scale * (-y) + HEIGHT / 2
    return (x_screen, y_screen)

def draw_coordinate_plane(canvas, scale):
    offset = 10
    canvas_width = WIDTH - PANEL_WIDTH
    canvas.create_line(0 + offset, (HEIGHT / 2), canvas_width - offset, (HEIGHT / 2), fill="blue", width=2, arrow=tk.BOTH)
    canvas.create_line((canvas_width / 2), 0 + offset, ((canvas_width / 2)), HEIGHT - offset, fill="blue", width=2, arrow=tk.BOTH)
    
    for x in range(0, int(canvas_width), int(scale)):
        canvas.create_line(x, 0 + offset, x, HEIGHT - offset, fill="grey", width=0.5)
    for y in range(0, int(HEIGHT), int(scale)):
        canvas.create_line(0 + offset, y, WIDTH - PANEL_WIDTH - offset, y, fill="grey", width=0.5)

colour_index = 0
selected_vector = None  # Start as None until user selects one
screen_origin = world_to_screen(0, 0, 30)
vector_buttons = []
button_idx = 0

def draw_vector(canvas: tk.Canvas, v: Vector):
    global colour_index
    x = v.components[0]
    y = v.components[1]
    
    vector_position = world_to_screen(x, y, 30)
    vector_id = canvas.create_line(screen_origin[0], screen_origin[1], vector_position[0], vector_position[1], fill=canvas_colors[colour_index], arrow=tk.LAST, width=2)
    v.color = canvas_colors[colour_index]
    colour_index = (colour_index + 1) % len(canvas_colors)
    v.vector_id = vector_id

def process_vector_buttons(button_id):
    global selected_vector 
    selected_vector = Vector.all_vectors[button_id]
    for button in vector_buttons:
        button.config(bg="white")
    vector_buttons[button_id].config(bg=selected_vector.color)

def create_vector(root, x_entry, y_entry, x_label, y_label, button, canvas):
    global button_idx
    x = x_entry.get()
    y = y_entry.get()
    
    if not x or not y: return  # Guard against empty fields
    
    x_entry.pack_forget()
    y_entry.pack_forget()
    x_label.pack_forget()
    y_label.pack_forget()
    button.pack_forget()
    
    v = Vector([float(x), float(y)])
    # Fixed the indexing mapping error here by using sequential IDs cleanly
    current_idx = button_idx
    vector_btn = tk.Button(root, width=PANEL_WIDTH, relief="solid", padx=2, pady=2, text=f"vector {current_idx}", command=lambda idx=current_idx: process_vector_buttons(idx))
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

    submit_btn = tk.Button(root, width=10, borderwidth=1, relief="solid", padx=2, pady=2, text="submit", command=lambda: create_vector(root, x_text, y_text, x_label, y_label, submit_btn, canvas))
    submit_btn.pack(side="top", pady=5) 

def get_rotation_angle(root, canvas):

    label = tk.Label(root, text="angle of rotation")
    label.pack(side="top", pady=5)
    entry_angle = tk.Entry(root, width=PANEL_WIDTH) 
    entry_angle.pack(side="top")

    # We read the entry inside the command function, ONLY when the user clicks the button
    rotate_btn = tk.Button(root, text="rotate", width=PANEL_WIDTH, relief="solid", borderwidth=1, padx=2, pady=2)
    rotate_btn.config(command=lambda: start_rotation(canvas, entry_angle, label, rotate_btn))
    rotate_btn.pack(side="top", pady=5) 

angle=0 

def start_rotation(canvas, entry_angle, label, rotate_btn):
    text_angle = entry_angle.get()
    if not text_angle or not selected_vector:
        print("Vector not selected or angle input empty!")
        return

    global angle 
    angle=0
    entry_angle.pack_forget()
    label.pack_forget()
    rotate_btn.pack_forget()
    animate_vector_rotation(canvas ,target_angle=float(text_angle), base_vector=selected_vector)

def animate_vector_rotation(canvas, target_angle, base_vector):
    global selected_vector
    global angle 

    angle+=2
    
    rotated_vector = rotate_vector(base_vector, angle)
    x_new = rotated_vector.components[0]
    y_new = rotated_vector.components[1]
    screen_target = world_to_screen(x_new, y_new, 30)

    
    canvas.coords(
        base_vector.vector_id,
        screen_origin[0], screen_origin[1],
        screen_target[0], screen_target[1]
    )

   
    if angle>= target_angle:
        # Snap completely to terminal position and assign state global variables
        final_vector = rotate_vector(base_vector, target_angle)
        final_target = world_to_screen(final_vector.components[0], final_vector.components[1], 30)
        canvas.coords(base_vector.vector_id, screen_origin[0], screen_origin[1], final_target[0], final_target[1])
        base_vector.components = final_vector.components
        return

   
    canvas.after(20, lambda: animate_vector_rotation(canvas, target_angle, base_vector))

def main():
    root = tk.Tk()
    root.title("Linear Algebra Visualizer")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    canvas = tk.Canvas(root, width=WIDTH-PANEL_WIDTH, height=HEIGHT, bg="black")
    canvas.pack(side="left")
    draw_coordinate_plane(canvas, 30)

    add = tk.Button(root, width=PANEL_WIDTH, height=3, text="Add vector", padx=50, pady=10, borderwidth=1, relief="solid", command=lambda: add_vector_to_ui(root, canvas))
    add.pack(side="top")

    rotate_btn = tk.Button(root, width=PANEL_WIDTH, height=3, text="Rotate vector", padx=50, pady=10, borderwidth=1, relief="solid", command=lambda: get_rotation_angle(root, canvas))
    rotate_btn.pack(side="top", pady=5)
    root.mainloop() 

if __name__ == "__main__":
    main()
