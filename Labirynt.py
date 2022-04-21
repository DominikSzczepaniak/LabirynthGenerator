import tkinter as tk
from collections import defaultdict
from tkinter import messagebox
from PIL import Image

class SpanningTree:
    def __init__(self, width, height):
        self.adj = defaultdict(list)
        rozmiar = width * height
        self.parent = range(rozmiar+5)
        self.size = [1] * (rozmiar+5)
    def FindSet(self, a):
        if(a == self.parent[a]):
            return a
        par = self.FindSet(self.parent[a])
        self.parent[a] = par
        return par
    def connect(self, a, b):
        a = self.FindSet(a)
        b = self.FindSet(b)
        if(a != b):
            if(self.size[a] < self.size[b]):
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b]
    def wypisz(self):
        for i in self.adj:
            print(i)

class Labirynth:
    def __init__(self):
        self.SizesGet()
    def SizesGet(self):
        DataInput = tk.Tk()
        width_var = tk.StringVar()
        height_var = tk.StringVar()
        tk.Label(DataInput, text="Height:").grid(column=0, row=0)
        tk.Label(DataInput, text="Width:").grid(column=0, row=1)
        tk.Entry(DataInput, textvariable=height_var).grid(column=1, row=0)
        tk.Entry(DataInput, textvariable=width_var).grid(column=1, row=1)
        tk.Button(DataInput, text="Generate", command=lambda: self.checkSizes(height_var.get(), width_var.get(), DataInput)).grid(column=0, row=3)
        DataInput.mainloop()
        height = height_var.get()
        width = width_var.get()
        DataInput.destroy()
        return self.generate(width, height)
    def checkSizes(self, height, width, DataInput):
        try:
            height = int(height)
            width = int(width)
        except:
            messagebox.showerror("Błąd", "Wartość powinna być z przedziału od 100 do 1000! Popraw wejście")
            return
        if(height < 100 or height > 1000 or width < 100 or width > 1000):
            messagebox.showerror("Błąd", "Wartość powinna być z przedziału od 100 do 1000! Popraw wejście")
            return
        else:
            DataInput.quit()
    def generate(self, width, height):
        Lab = tk.Tk()
        Lab.geometry("{0}x{1}".format(width, height))
        Lab.title("Labirynt gotowy!")
        Lab.resizable(False, False)
        Lab.mainloop()
    def AskAgain(self):
        pass
        #funkcja pytajaca czy uzytkownik chce utworzyc labirynt jeszcze raz na podstawie innych wymiarow (pozniej mozna zmienic to, ze w jednym oknie bedzie wszystko dzialac i przy kliknieciu generate bedzie tworzyc nowy labirynt)
    

def main():
    newLab = Labirynth()

if(__name__ == "__main__"):
    main()



