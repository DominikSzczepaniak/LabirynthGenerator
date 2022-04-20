import tkinter as tk
# from tkinter import ttk
from PIL import Image

def main():
    root = tk.Tk()
    width_var = tk.StringVar()
    height_var = tk.StringVar()
    frm = tk.Frame(root)
    frm.grid()
    tk.Label(frm, text="Height:").grid(column=0, row=0)
    tk.Label(frm, text="Width:").grid(column=0, row=1)
    tk.Entry(frm, textvariable=height_var).grid(column=1, row=0)
    tk.Entry(frm, textvariable=width_var).grid(column=1, row=1)
    tk.Button(frm, text="Generate", command=root.quit).grid(column=0, row=3)
    root.mainloop()
    height = height_var.get()
    width = width_var.get()
    print(height, width)
    root.destroy()
    Lab = tk.Tk()
    Lab.geometry("{0}x{1}".format(width, height))
    Lab.title("Labirynt gotowy!")
    Lab.mainloop()

if(__name__ == "__main__"):
    main()



