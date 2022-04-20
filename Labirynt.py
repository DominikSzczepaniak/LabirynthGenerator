import tkinter as tk
from collections import defaultdict
# from tkinter import ttk
from PIL import Image

class SpanningTree:
    def __init__(self, width, height):
        self.adj = defaultdict(list)
        rozmiar = width * height
        self.FU = range(rozmiar+5)
        self.FUsize = [1] * (rozmiar+5)
    def parent(self, a):
        return self.FU[a]
    def connect(self, a, b):
        if(self.parent(a) != self.parent(b)):
            if(self.FUsize[a] < self.FUsize[b]):
                a, b = b, a
            self.FUsize[a] += self.FUsize[b]
            self.FU[b] = self.FU[a]
            self.adj[a].append(b)
            self.adj[b].append(a)
    def wypisz(self):
        for i in self.adj:
            print(i)

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



