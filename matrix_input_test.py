import tkinter as tk

def get_matrix():
    matrix = []
    for i in range(rows):
        row = []
        for j in range(cols):
            # Fetch the value from each entry box
            val = entries[i][j].get()
            row.append(float(val) if val else 0.0)
        matrix.append(row)
    print("User Matrix:", matrix)

root = tk.Tk()
root.title("Matrix Input Grid")

rows, cols = 3, 3
entries = []

# Loop to dynamically generate the matrix grid layout
for i in range(rows):
    row_entries = []
    for j in range(cols):
        entry = tk.Entry(root, width=5, justify='center')
        entry.grid(row=i, column=j, padx=5, pady=5)
        row_entries.append(entry)
    entries.append(row_entries)

btn = tk.Button(root, text="Submit Matrix", command=get_matrix)
btn.grid(row=rows, column=0, columnspan=cols, pady=10)

root.mainloop()
