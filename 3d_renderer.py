import tkinter as tk
from state import *
import math
from vector_math import *
import transformations

class Render:

    def __init__(self, height, width, canvas):

        self.cos_30 = math.cos(math.radians(30))
        self.sin_30 = math.sin(math.radians(30))

        self.width = width
        self.height = height
        self.screen_origin = None
        self.scale = 20
        self.axis_len = 10
        self.all_vectors = []
        self.canvas = canvas
        self.colour_index = 0
        self.theta_x = 35.26
        self.theta_y = 45
        self.theta_z = 0
        self._update_trig()
        self.projection = "orthographic"

    def _get_next_color(self):
        vector_colors = [
            "red",  # #FF0000
            "blue",  # #0000FF
            "green2",  # #00EE00
            "magenta2",  # #FF1493
            "cyan2",  # #00EEEE
            "gold",  # #FFD700
            "orange",  # #FFA500
            "purple1",  # #9B30FF
            "turquoise3",  # #00C5CD
            "firebrick1",  # #FF3030
        ]

        color = vector_colors[self.colour_index]
        self.colour_index = (self.colour_index + 1) % len(vector_colors)
        return color

    def _update_trig(self):

        self.sx = math.sin(math.radians(self.theta_x))
        self.cx = math.cos(math.radians(self.theta_x))

        self.sy = math.sin(math.radians(self.theta_y))
        self.cy = math.cos(math.radians(self.theta_y))

        self.sz = math.sin(math.radians(self.theta_z))
        self.cz = math.cos(math.radians(self.theta_z))

    def _rotate(self, x, y, z):

        y1 = y * self.cx - z * self.sx
        z1 = y * self.sx + z * self.cx
        x1 = x

        x2 = x1 * self.cy + z1 * self.sy
        z2 = -x1 * self.sy + z1 * self.cy
        y2 = y1

        x3 = x2 * self.cz - y2 * self.sz
        y3 = x2 * self.sz + y2 * self.cz
        z3 = z2

        return x3, y3, z3

    def world_to_screen(self, x, y):

        x_screen = x * self.scale + (self.width) / 2
        y_screen = -(y) * self.scale + (self.height) / 2

        return x_screen, y_screen

    def isometric_projection_screen(self, x, y, z):

        x, y, z = self._rotate(x, y, z)

        if self.projection == "isometric":
            x, y, z = self._rotate(x, y, z)

            x_2d = (x - y) * self.cos_30

            y_2d = (x + y) * self.sin_30 - z

            return self.world_to_screen(x_2d, y_2d)

        elif self.projection == "orthographic":

            return self.world_to_screen(x, y)

    def draw_coordinate_plane(self, grid=False):

        self.screen_origin = self.isometric_projection_screen(0, 0, 0)
        if grid:
            current = -self.axis_len
            while current <= self.axis_len:

                start = self.isometric_projection_screen(-self.axis_len, 0, current)
                end = self.isometric_projection_screen(self.axis_len, 0, current)
                self.canvas.create_line(
                    start[0], start[1], end[0], end[1], fill="#2a2a2a", width=0.5
                )

                start = self.isometric_projection_screen(current, 0, -self.axis_len)
                end = self.isometric_projection_screen(current, 0, self.axis_len)
                self.canvas.create_line(
                    start[0], start[1], end[0], end[1], fill="#2a2a2a", width=0.5
                )

                current += 1

        x_axis_start = self.isometric_projection_screen(self.axis_len, 0, 0)
        x_axis_end = self.isometric_projection_screen(-self.axis_len, 0, 0)

        y_axis_start = self.isometric_projection_screen(0, self.axis_len, 0)
        y_axis_end = self.isometric_projection_screen(0, -self.axis_len, 0)

        z_axis_start = self.isometric_projection_screen(0, 0, self.axis_len)
        z_axis_end = self.isometric_projection_screen(0, 0, -self.axis_len)

        self.canvas.create_line(
            x_axis_start[0],
            x_axis_start[1],
            x_axis_end[0],
            x_axis_end[1],
            fill="blue",
            width=0.8,
            arrow=tk.BOTH,
        )
        self.canvas.create_line(
            y_axis_start[0],
            y_axis_start[1],
            y_axis_end[0],
            y_axis_end[1],
            fill="red",
            width=0.8,
            arrow=tk.BOTH,
        )
        self.canvas.create_line(
            z_axis_start[0],
            z_axis_start[1],
            z_axis_end[0],
            z_axis_end[1],
            fill="green",
            width=0.8,
            arrow=tk.BOTH,
        )

        self.canvas.create_text(
            x_axis_start[0] + 10,
            x_axis_start[1] - 10,
            text="X",
            fill="blue",
            font=("Arial", 12, "bold"),
        )
        self.canvas.create_text(
            y_axis_start[0] + 10,
            y_axis_start[1] - 10,
            text="Y",
            fill="red",
            font=("Arial", 12, "bold"),
        )
        self.canvas.create_text(
            z_axis_start[0] + 10,
            z_axis_start[1] - 10,
            text="Z",
            fill="green",
            font=("Arial", 12, "bold"),
        )

    def draw_vector_on_canvas(self, v: Vector):

        if not v.color or v.color == "white":
            v.color = self._get_next_color()

        sx, sy = self.isometric_projection_screen(
            v.components[0], v.components[1], v.components[2]
        )
        vector_id = self.canvas.create_line(
            self.screen_origin[0],
            self.screen_origin[1],
            sx,
            sy,
            fill=v.color,
            width=2,
            arrow=tk.LAST,
        )
        v.vector_id = vector_id


class UI(Render):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.root = tk.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas = tk.Canvas(
            self.root, height=self.height, width=self.width - PANEL_WIDTH, bg="black"
        )
        self.frame = tk.Frame(self.root, height=self.height, width=PANEL_WIDTH)
        self.vector_list = None

        super().__init__(height=height, width=width - PANEL_WIDTH, canvas=self.canvas)

    def build_ui(self):

        self.axis_len = 20
        self.draw_coordinate_plane(
            grid=True,
        )

        self.render_sliders()

        new_vector_btn = tk.Button(self.frame, text="Create New Vector")
        new_vector_btn.config(command=lambda: self.render_vector_input_field())
        new_vector_btn.pack()

        scale_vector_btn=tk.Button(self.frame,text="Scale Vector")
        scale_vector_btn.config(command=lambda: self.render_scale_input())
        scale_vector_btn.pack()

        self.render_vector_list_box()

        self.frame.pack(side="left", expand=True)
        self.canvas.pack(side="right", expand=True)

        self.root.mainloop()

    def update_slider_value(self, x_theta=None, y_theta=None, z_theta=None):

        if x_theta:
            self.theta_x = float(x_theta)
        if y_theta:
            self.theta_y = float(y_theta)
        if z_theta:
            self.theta_x = float(z_theta)
        self.redraw()

    def render_sliders(self):

        sliders_frame = tk.Frame(self.frame, width=PANEL_WIDTH)

        x_slider = tk.Scale(
            sliders_frame, from_=-90, to=90, orient="horizontal", resolution=1
        )
        y_slider = tk.Scale(
            sliders_frame, from_=-90, to=90, orient="horizontal", resolution=1
        )
        z_slider = tk.Scale(
            sliders_frame, from_=-90, to=90, orient="horizontal", resolution=1
        )
        x_slider.set(self.theta_x)
        y_slider.set(self.theta_y)
        z_slider.set(self.theta_z)
        x_slider.config(command=lambda v: self.update_slider_value(x_theta=v))
        y_slider.config(command=lambda v: self.update_slider_value(y_theta=v))
        z_slider.config(command=lambda v: self.update_slider_value(z_theta=v))
        x_slider.pack(fill=tk.X, padx=5, pady=2)
        y_slider.pack(fill=tk.X, padx=5, pady=2)
        z_slider.pack(fill=tk.X, padx=5, pady=2)
        sliders_frame.pack(fill=tk.X, padx=5, pady=5)

    def create_new_vector(self, input_frame):

        widgets = self.frame.winfo_children()
        widgets[1].config(state="normal")

        widgets = input_frame.winfo_children()

        user_entry=widgets[2].get().strip()
        self.vector_list.insert(tk.END,f"vector {len(Vector.all_vectors)}")
        if user_entry:
            comp=list(map(int,user_entry.split()))
            v=Vector(comp)
            self.draw_vector_on_canvas(v)
            input_frame.destroy()

    def render_vector_list_box(self):

        self.vector_list = tk.Listbox(self.frame, width=30)
        self.vector_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def render_vector_input_field(self):

        widgets = self.frame.winfo_children()
        widgets[1].config(state="disabled")

        input_frame = tk.Frame(self.frame, width=PANEL_WIDTH)

        label = tk.Label(input_frame, text="Enter x y z components")

        create_vector_btn = tk.Button(input_frame, relief="solid", text="Create")

        user_input = tk.Entry(input_frame)

        create_vector_btn.config(command=lambda: self.create_new_vector(input_frame))

        label.pack(fill=tk.X, padx=5, pady=2)
        user_input.pack(fill=tk.X, padx=5, pady=2)
        create_vector_btn.pack(fill=tk.X, padx=5, pady=2)
        input_frame.pack(fill=tk.X, padx=5, pady=5)

    def update_vector(self,v:Vector,new_x,new_y):

        self.canvas.coords(v.vector_id,self.screen_origin[0],self.screen_origin[1],new_x,new_y) 
    

    def render_scale_input(self):

        widgets=self.frame.winfo_children()
        widgets[2].config(state="disabled")

        scale_frame=tk.Frame(self.frame,width=PANEL_WIDTH)

        scale_label=tk.Label(scale_frame,text="Enter sx sy sz ")

        scale_input=tk.Entry(scale_frame)

        scale_btn=tk.Button(scale_frame,relief="solid",text="Scale") 

        scale_btn.config(command=lambda : self.scale_vector_on_canvas(scale_frame))

        scale_label.pack(fill=tk.X,padx=5,pady=2)
        scale_input.pack(fill=tk.X,padx=5,pady=2)
        scale_btn.pack(fill=tk.X,padx=5,pady=2)

        scale_frame.pack()

    def scale_vector_on_canvas(self,scale_frame):
        
        widgets=self.frame.winfo_children()
        widgets[2].config(state="normal")

        widgets=scale_frame.winfo_children()

        sx,sy,sz=map(float,widgets[1].get().strip().split())
        
        for idx in self.vector_list.curselection():

            v=Vector.all_vectors[idx]

            new_v=transformations.scale_vector(v,sx,sy,sz) 

            v.components=new_v.components
           
            new_cords=self.isometric_projection_screen(v.components[0],v.components[1],v.components[2])

            self.update_vector(v,new_cords[0],new_cords[1])

        scale_frame.destroy()

    def redraw(self, grid=True):
        self._update_trig()
        self.canvas.delete("all")
        self.draw_coordinate_plane(grid=grid)

        for v in Vector.all_vectors:

            self.draw_vector_on_canvas(v)


app = UI(HEIGHT, WIDTH)
app.projection = "orthographic"
app.build_ui()
