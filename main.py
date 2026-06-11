from renderer import *

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
        text="create vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: add_vector_to_ui(root, canvas),
    )
    add.pack(side="top", pady=5, padx=2)

    delete_btn = tk.Button(
        root,
        width=PANEL_WIDTH,
        height=2,
        text="Delete vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: delete_vector(canvas),
    ) 

    delete_btn.pack(side="top", pady=5, padx=2)

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
        text="Reflect vector",
        padx=50,
        pady=10,
        borderwidth=1,
        relief="solid",
        command=lambda: get_reflection_axis(root, canvas),
    )
    reflect_btn.pack(side="top", pady=5, padx=2)
    zoom = tk.Scale(root, resolution=1, from_=5, to=50, orient=tk.HORIZONTAL)
    zoom.config(command=lambda v: update_slider_value(canvas, v))
    zoom.pack(side="top", padx=2, pady=5)
    zoom.set(20)

    root.mainloop()


if __name__ == "__main__":
    main()