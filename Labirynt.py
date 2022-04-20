import tkinter as tk
# from tkinter import ttk
from PIL import Image

def getSize():
    DataInput = tk.Tk()
    width_var = tk.StringVar()
    height_var = tk.StringVar()
    tk.Label(DataInput, text="Height:").grid(column=0, row=0)
    tk.Label(DataInput, text="Width:").grid(column=0, row=1)
    tk.Entry(DataInput, textvariable=height_var).grid(column=1, row=0)
    tk.Entry(DataInput, textvariable=width_var).grid(column=1, row=1)
    tk.Button(DataInput, text="Generate", command=DataInput.quit).grid(column=0, row=3)
    DataInput.mainloop()
    height = height_var.get()
    width = width_var.get()
    DataInput.destroy()
    return width, height

def generate(width, height):
    Lab = tk.Tk()
    Lab.geometry("{0}x{1}".format(width, height))
    Lab.title("Labirynt gotowy!")
    
    Lab.mainloop()

def main():
    width, height = getSize()
    generate(width, height)

if(__name__ == "__main__"):
    main()



