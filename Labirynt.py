import tkinter as tk
from collections import defaultdict
from tkinter import messagebox
from PIL import Image
from random import seed
from random import randint
import time

class SpanningTree:
    def __init__(self, width, height):
        self.adj = defaultdict(list)
        rozmiar = width * height
        self.parent = [i for i in range(rozmiar+5)]
        self.size = [1] * (rozmiar+5)
    def FindSet(self, a):
        if(a == self.parent[a]):
            return a
        par = self.FindSet(self.parent[a])
        self.parent[a] = par
        return par
    def Union(self, a, b):
        a = self.FindSet(a)
        b = self.FindSet(b)
        if(a != b):
            if(self.size[a] < self.size[b]):
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b]
            self.adj[a].append(b)
            self.adj[b].append(a)

class Labirynth:
    def __init__(self):
        # self.SizesGet()
        self.GenerateLabirynt(4,3)
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
        return self.LabiryntWindow(width, height)
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
    def LabiryntWindow(self, width, height):
        Lab = tk.Tk()
        Lab.geometry("{0}x{1}".format(width, height))
        Lab.title("Labirynt gotowy!")
        Lab.resizable(False, False)
        Lab.mainloop()
    def AskAgain(self):
        pass
        #funkcja pytajaca czy uzytkownik chce utworzyc labirynt jeszcze raz na podstawie innych wymiarow (pozniej mozna zmienic to, ze w jednym oknie bedzie wszystko dzialac i przy kliknieciu generate bedzie tworzyc nowy labirynt)
    def GenerateLabirynt(self, width, height):
        #Na podstawie podanych wymiarow tworzymy wierzcholki - jeśli np. width = 50, height = 40, to node 51 jest w tablicy na miejscu [2][1]. Wiersz = n/width, kolumna= n - n/width.
        # Bazowo miedzy wszystkimi miejscami w tablicy jest sciana, a MSP bedziemy je usuwac. Przejdzmy wiec po wszystkich parach a b, gdzie a, b nalezy do przedzialu (1, ilosc wierzcholkow) i wylosujmy liczbe z przedzialu (1, 10^7). Pozniej posortujmy krawedzie i zrobmy MSP na nich. Ustalone MSP bedzie droga poprawna w labiryncie. Wiec odczytamy ta droge i usuniemy poprawne sciany w tablicy. Na koncu wystarczy wybrac dowolny node na wyjscie i wejscie i mamy labirynt. 
        edges = []
        vert = [[1, 0], [-1, 0], [0, 1], [0,-1]]
        for i in range(1, width*height+1):
            line = (i-1)//width+1 #getting line and column in map for node i
            column = i%width
            if(column == 0):
                column = width
            for j in vert: #right left up down
                x = column+j[0]
                y = line + j[1]
                if(x<=0 or x > width or y <= 0 or y > height):
                    continue
                seed(time.time())
                wartosc = randint(1, 10000000) 
                node = (y-1)*width + x #converting map place to node number
                if(node == i):
                    continue
                edges.append([int(i), int(node), int(wartosc)])
        edges.sort(key = lambda edges:edges[2])
        MSP = SpanningTree(width, height)
        polaczone = []
        for a, b, c in edges:
            if(MSP.FindSet(a) == MSP.FindSet(b)):
                continue
            MSP.Union(a, b)
            polaczone.append([a, b])
        #for every node create info as :[0,0,0,0] meaning that there is no wall on the left, above, right, below, if number is 1, there is a wall. originally set every value to 1 and when there is edge in MSP make it 0. 
        Mapinfo = [[1,1,1,1] for i in range(width*height+5)] 
        for i in range(1, width+1): #taking care of above wall for every upmost cell
            Mapinfo[i][1] = 1
        for i in range(1, width*height+1, width):#taking care of left wall for every leftmost cell 
            Mapinfo[i][0] = 1
        for i in range(1 + (height-1)*width, width*height+1):#downmost cells
            Mapinfo[i][3] = 1
        for i in range(width, width*height+1, width): #rightmost cells
            Mapinfo[i][2] = 1
        #entry will be on leftmost up cell and exit will be at rightmost down cell
        Mapinfo[1][1] = 0
        Mapinfo[width*height][3] = 0
        for a, b in polaczone:
            if(a > b):
                a, b = b, a
            if(a == b-1):
                #a is on left to b
                Mapinfo[a][2] = 0
                Mapinfo[b][0] = 0
            elif(a == b+1):
                #a is on right to b
                Mapinfo[a][0] = 0
                Mapinfo[b][2] = 0
            else:
                #a is less than b, so it must be above b
                Mapinfo[a][3] = 0
                Mapinfo[b][1] = 0



def main():
    newLab = Labirynth()
    

if(__name__ == "__main__"):
    main()


