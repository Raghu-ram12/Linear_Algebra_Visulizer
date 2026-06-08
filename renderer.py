HEIGHT = 700
WIDTH = 1000

def  world_to_screen(x,y,Scale):

    x_screen=Scale*(x)+(WIDTH)/2
    y_screen=Scale*(-y)+(HEIGHT)/2
    return (x_screen,y_screen)

def draw_coordinate_plane(canvas,scale):

    # draw x-axis 
    offset=10
    canvas.create_line(0+offset,(HEIGHT/2),WIDTH-offset,(HEIGHT/2),fill="black",width=2)
    #draw y axis 
    canvas.create_line((WIDTH/2),0+offset,(WIDTH/2),HEIGHT-offset,fill="black",width=2)
    lim_x=int(WIDTH)
    
    for x in range(-lim_x,lim_x,int(scale)):
        # draw vertical grid lines

        canvas.create_line(x,0+offset,x,HEIGHT-offset,fill="grey",width=0.5)
    lim_y=int(HEIGHT)
    for y in range(-lim_y,lim_y,scale):

        canvas.create_line(0+offset,y,WIDTH-offset,y,fill="grey",width=0.5)

from tkinter import * 

root=Tk() 
root.title("Linear algebra visualizer")
playground=Canvas(root,width=WIDTH,height=HEIGHT)
x,y=world_to_screen(0,0,100)
x2,y2=world_to_screen(-5,-5,50)
x3,y3=world_to_screen(3,4,50)
draw_coordinate_plane(playground,10)
playground.create_line(x,y,x2,y2,fill="red",width=1)
playground.create_line(x,y,x3,y3,fill="green",width=1)
playground.pack()
root.mainloop()

