import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Treeview Background Color Example")

# Create a Treeview widget
tree = ttk.Treeview(root)
tree.grid(row=0, column=0)

# Configure the tag to set background color
tree.tag_configure("bg", background="lightblue")  # Set the background color

# Insert items into the Treeview
tree.insert("", "end", text="Item 1", tags=("bg",))
tree.insert("", "end", text="Item 2", tags=("bg",))
tree.insert("", "end", text="Item 3", tags=("bg",))

root.mainloop()
