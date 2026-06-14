
from renderer import * 
from tkinter import messagebox 

def trigger_error():

        messagebox.showerror("Value Error","Invalid input! please a number")

def get_vector_components(root, canvas,vector_list):

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
            root, x_text, y_text, x_label, y_label, submit_btn, canvas,vector_list
        ),
    )
    submit_btn.pack(side="top", pady=5) 


def create_vector(root, x_entry, y_entry, x_label, y_label, button, canvas,vector_list):

    global button_idx,colour_index

    x = x_entry.get().strip()
    y = y_entry.get().strip()

    if not x or not y:
        return

    x_entry.pack_forget()
    y_entry.pack_forget()
    x_label.pack_forget()
    y_label.pack_forget()
    button.pack_forget()
    
    try :

       v = Vector([float(x),float(y)])

    except ValueError:

        trigger_error()
        return

    vector_list.insert(tk.END,f"Vector {button_idx +1}")
    
    color_to_use=canvas_colors[colour_index]

    colour_index=(colour_index+1)%len(canvas_colors)

    vector_list.itemconfig(tk.END,fg=color_to_use)
    v.color=color_to_use

    button_idx += 1
    
    draw_vector_on_canvas(canvas, v, color_to_use) 

def get_rotation_angle(root, canvas,vector_list):

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
        command=lambda: start_rotation(canvas, entry_angle, label, rotate_btn,vector_list)
    )
    rotate_btn.pack(side="top", pady=5)


def start_rotation(canvas, entry_angle, label, rotate_btn,vector_list):


    text_angle = entry_angle.get().strip()

    selections =vector_list.curselection()
    entry_angle.pack_forget()
    label.pack_forget()
    rotate_btn.pack_forget()
    
    try:

        input_angle=float(text_angle)

    except ValueError:
        
        trigger_error()
        return


    for idx in selections:

        angle = 0
        base_vector = Vector.all_vectors[idx]
        start_components = base_vector.components[:]
    
        animate_vector_rotation(
        canvas=canvas,
        target_angle=input_angle,
        base_vector=base_vector,
        start_components=start_components,
        angle=0
     )


def animate_vector_rotation(canvas, target_angle, base_vector, start_components,angle):
    
    angle += 2

    temp_vector = Vector(start_components[:],track=False)
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
        final_temp = Vector(start_components[:],track=False)
        final_vector = rotate_vector(final_temp, target_angle)

        base_vector.components = final_vector.components[:]

        update_vector_on_canvas(canvas, base_vector)
        return

    canvas.after(
    20,
    lambda bv=base_vector, sc=start_components, a=angle: animate_vector_rotation(
        canvas, target_angle, bv, sc, a
    ),
)

def process_scale(canvas, text_scale_x, text_scale_y, x_label, y_label, scale_btn,vector_list):
    
    selections=vector_list.curselection()

    x_scale = text_scale_x.get().strip()
    y_scale = text_scale_y.get().strip()

    if not x_scale or not y_scale:
        messagebox.showerror("Enter both scale values")
        return
    
    text_scale_x.pack_forget()
    text_scale_y.pack_forget()
    x_label.pack_forget()
    y_label.pack_forget()
    scale_btn.pack_forget()
    
    try:
        x_scale=float(x_scale)
        y_scale=float(y_scale)

    except ValueError:

        trigger_error()
        return
    
    if len(selections)==0:
        messagebox.showerror(message="Please select at least 1 Vector")
        return
        
    for idx in selections:

        selected_vector = Vector.all_vectors[idx]
        scaled_vector = scale_vector(selected_vector, sx=x_scale, sy=y_scale)
        selected_vector.components = scaled_vector.components[:]
        update_vector_on_canvas(canvas, selected_vector)


def get_scale_factor(root, canvas,vector_list):

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
            canvas, text_scale_x, text_scale_y, x_label, y_label, scale_btn,vector_list
        ),
    )
    scale_btn.pack(side="top")


def display_vector_reflection(canvas, label, x_btn, y_btn,vector_list,axis=None):

    selections=vector_list.curselection()

    if len(selections)==0:
        messagebox.showerror(message="Please select at least 1 Vector")
        return

    x_btn.pack_forget()
    y_btn.pack_forget()
    label.pack_forget()

   

    for idx in selections:

        selected_vector = Vector.all_vectors[idx]

        if axis == 1:
            reflected = reflect_on_x_axis(selected_vector)
            selected_vector.components = reflected.components[:]
        

        elif axis == 0:
            reflected = reflect_on_y_axis(selected_vector)
            selected_vector.components = reflected.components[:]
        
        update_vector_on_canvas(canvas, selected_vector)

       

def get_reflection_axis(root, canvas,vector_list):

    label = tk.Label(root, text="select axis")
    x_btn = tk.Button(root, text="x-axis", width=200)
    y_btn = tk.Button(root, text="y-axis", width=200)

    label.pack(side="top")
    x_btn.pack(padx=2, pady=5, side="top")
    y_btn.pack(padx=2, pady=5, side="top")

    x_btn.config(command=lambda: display_vector_reflection(canvas, label, x_btn, y_btn,vector_list, axis=1))
    y_btn.config(command=lambda: display_vector_reflection(canvas, label, x_btn, y_btn,vector_list, axis=0))


def process_input_matrix(canvas,root,matrix,transform_btn,vector_list):
    
    given_matrix=[] 
    try:
        for i in range(2):
            row=[]
            for j in range(2):
                row.append(float(matrix[i][j].get()))
                given_matrix.append(row) 
    
        given_matrix=Matrix(given_matrix)

    except ValueError:
        trigger_error()
        return
    
    matrix[0][0].master.destroy()

    transform_btn.pack_forget()
    selections=vector_list.curselection()

    if len(selections)==0:
        messagebox.showerror(message="Please select at least 1 Vector")
        return 

    for idx in selections:

        transformed_vector=multiply_matrix_vector(Vector.all_vectors[idx],given_matrix)
        
        Vector.all_vectors[idx].components=transformed_vector.components[:]

        update_vector_on_canvas(canvas,Vector.all_vectors[idx])

def get_transform_matrix(root,canvas,vector_list):

    # Create a separate frame for the matrix to use grid geometry manager

    matrix_frame = tk.Frame(root, bg="gray")
    matrix_frame.pack(side="top", padx=5, pady=5)

    matrix=[]

    for i in range(2):
        row=[]
        for j in range(2):

            element=tk.Entry(matrix_frame,width=5,justify="center")

            element.grid(row=i,column=j, padx=10, pady=5)

            row.append(element)

        matrix.append(row)

    transform_btn=tk.Button(matrix_frame,width=5,text="Enter")
    transform_btn.grid(row=2, column=0, columnspan=2, pady=5)
    transform_btn.config(command= lambda m=matrix: process_input_matrix(canvas,root,m,transform_btn,vector_list)) 

def delete_vector(canvas, vector_list):
    global button_idx

    selections = vector_list.curselection()

    if len(selections) == 0:
        messagebox.showerror(message="Please select at least 1 Vector")
        return

    for idx in selections[::-1]:
        canvas.delete(Vector.all_vectors[idx].vector_id)
        vector_list.delete(idx)
        Vector.all_vectors.pop(idx)

    
    for i, v in enumerate(Vector.all_vectors):
        vector_list.delete(i)
        vector_list.insert(i, f"Vector {i + 1}")
        vector_list.itemconfig(i, fg=v.color)

    button_idx = len(Vector.all_vectors)    

def delete_resultant(canvas,resultant,delete_btn):

    canvas.delete(resultant.vector_id) 
    delete_btn.destroy()

def vector_addition(root,canvas,vector_list):

    global colour_index

    selections=vector_list.curselection()
    
    if len(selections)!=2:
        messagebox.showerror(title="Selection Error",message="Please select 2 vectors ")
        return

    v1=Vector.all_vectors[selections[0]]
    v2=Vector.all_vectors[selections[1]]
    resultant=add_vectors(v1,v2)
    
    color_to_use=canvas_colors[colour_index]
    colour_index=(colour_index+1)%len(canvas_colors)
    
    resultant.color=color_to_use 
    draw_vector_on_canvas(canvas,resultant,color_to_use)
    delete_btn=tk.Button(root,text="delete resultant",width=8)

    delete_btn.pack(side="top")
    delete_btn.config(command=lambda : delete_resultant(canvas,resultant,delete_btn))
    
