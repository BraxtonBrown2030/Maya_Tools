# import maya.cmds as cmds
import tkinter as tk

def update_maya_commaond():
    


def close_window():
    root.destroy()

def show_value(val):
    value_label.config(text=f"Value: {val}")

root = tk.Tk()
root.title("Maya Update Window")
root.geometry("300x200")

slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=show_value)
slider.pack(pady=20)

value_label = tk.Label(root, text="Value: 0")
value_label.pack()

root.mainloop()