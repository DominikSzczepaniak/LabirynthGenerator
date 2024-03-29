import tkinter as tk
from collections import defaultdict
from tkinter import *
from tkinter import filedialog, messagebox, Scale
from PIL import Image, ImageDraw, ImageTk
from random import seed
from random import randint
import time

#TODO:
#- umozliwianie zmieniania wielkosci cell na pixele i pokazywanie obok przy ruszaniu suwakiem jak wygladalby labirynt 2x2 z takimi wymiarami 1/2 DONE (tylko liczby parzyste)
#pobierz od uzytkownika wielkosc monitora i wyswietl informacje jesli labirynt nie zmiesci sie na jego ekranie przy obecnie wybranych wymiarach
#- pokazywanie labiryntu w oknie "gotowe" DONE
#- mozliwosc zapisania labiryntu do pliku (pdf, jpg, png etc.) w dowolnie wybranym miejscu na dysku
#- pokazanie sciezki aby dojsc do celu
#- wizualizacja jak rozne algorytmy wybieralyby sciezki aby przejsc labirynt.

class SpanningTree:
    def __init__(self, width, height):
        size = width * height
        self.parent = [i for i in range(size+5)]
        self.size = [1] * (size+5)
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

class Labirynth:
    def __init__(self):
        self.SizesGet()
    def SizesGet(self):
        """
        Function that gets sizes of labirynt from user.
        """
        DataInput = tk.Tk()
        width_var = tk.StringVar()
        height_var = tk.StringVar()
        cellSize_var = tk.StringVar()
        tk.Label(DataInput, text="Height:").grid(column=0, row=0)
        tk.Label(DataInput, text="Width:").grid(column=0, row=1)
        tk.Entry(DataInput, textvariable=height_var).grid(column=1, row=0)
        tk.Entry(DataInput, textvariable=width_var).grid(column=1, row=1)
        tk.Label(DataInput, text="Cell size:").grid(column=0, row=3)
        tk.Scale(DataInput, from_=4, to=64,variable=cellSize_var, orient=tk.HORIZONTAL).grid(column=1, row=3)
        tk.Button(DataInput, text="Generate", command=lambda: self.checkSizes(height_var.get(), width_var.get(), DataInput)).grid(column=1, row=4)
        DataInput.geometry("400x200")
        DataInput.title("Labirynth generator")
        DataInput.mainloop()
        cellSize = int(cellSize_var.get())
        if(cellSize%2==1):
            cellSize-=1
        height = int(height_var.get())
        width = int(width_var.get())
        DataInput.destroy()
        return self.LabiryntWindow(width, height, cellSize)
    def checkSizes(self, height, width, DataInput):
        try:
            height = int(height)
            width = int(width)
        except:
            messagebox.showerror("Error", "Value should be between 10 and 200!")
            return
        if(height < 10 or height > 200 or width < 10 or width > 200):
            messagebox.showerror("Error", "Value should be between 10 and 200!")
            return
        else:
            DataInput.quit()
    def LabiryntWindow(self, width, height, cellSize=12):
        Lab = tk.Tk()
        Lab.geometry("{0}x{1}".format(width*cellSize+200, height*cellSize+200))
        Lab.title("Labirynt gotowy!")
        Lab.resizable(False, False)
        img = self.GenerateLabirynt(width, height, cellSize)
        photo = ImageTk.PhotoImage(img)
        PhotoObject = Label(Lab, image = photo, anchor="center",bd='20')
        PhotoObject.pack()
        Lab.mainloop()
    def AskAgain(self):
        #funkcja pytajaca czy uzytkownik chce utworzyc labirynt jeszcze raz na podstawie innych wymiarow (pozniej mozna zmienic to, ze w jednym oknie bedzie wszystko dzialac i przy kliknieciu generate bedzie tworzyc nowy labirynt)
        pass
    def RandomiseEdges(self, width, height):
        edgesForMap = [] #list of edges to generate map for labirynth
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
                edgesForMap.append([int(i), int(node), int(wartosc)])
        edgesForMap.sort(key = lambda edges:edges[2])
        return edgesForMap
    def GeneratePath(self, width, height, adj):
        q = []
        visited = [False] * int(height*width+5)
        odl = [1000000] * int(height*width+5)
        q.append(1)
        visited[1] = True
        odl[1] = 0
        while(len(q) > 0):
            node = q.pop(0)
            for u in adj[node]:
                if(visited[u] == False):
                    odl[u] = odl[node]+1
                    visited[u] = True
                    q.append(u)
        pathLength = odl[width*height]
        CurrentNode = width*height
        path = []
        while(pathLength > 0):
            path.append(CurrentNode)
            for u in adj[CurrentNode]:
                if(odl[u] == pathLength-1):
                    CurrentNode = u 
                    pathLength = odl[u]
        path.append(1)
        path.reverse()
        return path
    def GenerateLabirynt(self, width, height, cellSize):
        edges = self.RandomiseEdges(width, height)
        MSP = SpanningTree(width, height)
        polaczone = []
        adj = defaultdict(list)
        for a, b, c in edges:
            if(MSP.FindSet(a) == MSP.FindSet(b)):
                continue
            MSP.Union(a, b)
            polaczone.append([a, b])
            adj[a].append(b)
            adj[b].append(a)
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
        LabIm = Image.new("RGB", (width*cellSize+1, height*cellSize+1), color='white')
        LabImDraw = ImageDraw.Draw(LabIm)
        LabImDraw.rectangle([(0,0),(width*cellSize, height*cellSize)], fill='white', outline='black')
        id = 1
        for j in range(1, height+1):
            for i in range(1,width+1):
                self.DrawWalls(LabImDraw, i, j, Mapinfo[id], cellSize)
                id+=1 
        LabImDraw.rectangle([(0, 1), (0, cellSize-1)], fill = 'white', outline = 'white')
        LabImDraw.rectangle([(width*cellSize, 1+(height-1)*cellSize), (width*cellSize, height*cellSize-1)], fill = 'white', outline = 'white')
        path = self.GeneratePath(width, height, adj)
        #by hand do line to middle of cell 1 and last cell and write algorithm to connect other cells based on path nodelist
        return LabIm
    def DrawWalls(self, LabImDraw, x, y, infoDraw, cellSize):
        # center = [[int(2+(x-1)*4)],[int(2+(y-1)*4)]]
        centerx = int(cellSize//2+(x-1)*cellSize)
        centery = int(cellSize//2+(y-1)*cellSize)
        lewygornyrog = (centerx-cellSize//2, centery-cellSize//2)
        lewydolnyrog = (centerx-cellSize//2, centery+cellSize//2)
        prawydolnyrog = (centerx+cellSize//2, centery+cellSize//2)
        prawygornyrog = (centerx+cellSize//2, centery-cellSize//2)
        if(infoDraw[0] == 1):
            LabImDraw.rectangle([lewygornyrog, lewydolnyrog], fill='black')
        if(infoDraw[1] == 1):
            LabImDraw.rectangle([lewygornyrog, prawygornyrog], fill = 'black')
        if(infoDraw[2] == 1):
            LabImDraw.rectangle([prawygornyrog, prawydolnyrog], fill = 'black')
        if(infoDraw[3] == 1):
            LabImDraw.rectangle([lewydolnyrog, prawydolnyrog], fill = 'black')
    def DrawPath(self, LabImDraw, x, y, whereFrom, whereTo, cellsize):
        #whereFrom - info where did u come from (left, above, right, below)
        #whereTo - info where are u going next (left, above, right, below)
        #both these informations are used to color cells accordingly 

        pass





def main():
    newLab = Labirynth()
    

if(__name__ == "__main__"):
    main()


