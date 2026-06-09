HEIGHT = 800
WIDTH = 1400
PANEL_WIDTH=400 

from transformations import *
import tkinter as tk
canvas_colors = [
    "crimson",      # Vibrant Red
    "dodger blue",  # Bright Blue
    "forest green", # Deep Green
    "gold",         # Rich Yellow
    "dark orchid",  # Deep Purple
    "dark orange",  # Bright Orange
    "turquoise",    # Bright Cyan-Blue
    "hot pink",     # Vibrant Pink
    "slate gray",   # Neutral Dark Gray
    "saddle brown"  # Rich Brown
]

def  world_to_screen(x,y,Scale):

    x_screen=Scale*(x)+(WIDTH-PANEL_WIDTH)/2
    y_screen=Scale*(-y)+(HEIGHT)/2
    return (x_screen,y_screen)

def draw_coordinate_plane(canvas,scale):

    # draw x-axis 
    offset=10
    canvas_width=WIDTH-PANEL_WIDTH
    canvas.create_line(0,(HEIGHT/2),canvas_width,(HEIGHT/2),fill="blue",width=2,arrow=tk.BOTH)

    #draw y axis 
    canvas.create_line((canvas_width/2),0,(canvas_width/2),HEIGHT,fill="blue",width=2,arrow=tk.BOTH)
    lim_x=int(canvas_width)
    
    for x in range(-lim_x,lim_x,int(scale)):
        # draw vertical grid lines

        canvas.create_line(x,0+offset,x,HEIGHT-offset,fill="grey",width=0.5)
    lim_y=int(HEIGHT)
    for y in range(-lim_y,lim_y,scale):

        canvas.create_line(0+offset,y,WIDTH-PANEL_WIDTH-offset,y,fill="grey",width=0.5)

colour_index=0

def draw_vector(canvas: tk.Canvas,v:Vector):
    global colour_index

    x=v.components[0]
    y=v.components[1]
    screen_origin=world_to_screen(0,0,30)
    vector_position=world_to_screen(x,y,30)

    canvas.create_line(screen_origin[0],screen_origin[1],vector_position[0],vector_position[1],fill=canvas_colors[colour_index],arrow=tk.LAST,width=1)

    colour_index=(colour_index+1)%len(canvas_colors)

     
def main():
    root=tk.Tk()
    root.title("Linear Algebra Visualizer")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    canvas=tk.Canvas(root,width=WIDTH-PANEL_WIDTH,height=HEIGHT,bg="black")
    draw_coordinate_plane(canvas,30)
    v1=Vector([5,5])
    v2=Vector([-5,5])
    v3=Vector([5,-5])
    v4=Vector([-5,-5])
    draw_vector(canvas,v1)
    draw_vector(canvas,v2)
    draw_vector(canvas,v3)
    draw_vector(canvas,v4)

    canvas.pack(side="left")
    root.mainloop() 
  
if __name__ =="__main__":
    main() 