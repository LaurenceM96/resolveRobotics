from audioop import cross
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from roamer import RobotRoamer

class Interface:
    def __init__(self, master, canvasSize, turtleSize):
        #Initialise the interface
        self.master = master
        self.canvasSize = canvasSize
        self.turtleSize = turtleSize #Turtle size, determines size of turtle and step size
        self.roamer = RobotRoamer(self.canvasSize)
        self.labels = [] #List of labels so am able to highlight as they play
        self.lines = []  #List of lines so am able to delete them all when resetting
        self.asteroids = [] #List of asteroids so am able to delete them when playing the game
        self.asteroid_coords = [] #List of asteroid coords so can see when they are eaten
        self.cross_lines = [] #List of crosses so they can be deleted when not playing game
        self.canvas = tk.Canvas(master, bg="white", width=canvasSize+200, height=canvasSize)
        self.canvas.grid(column=0, row=0, columnspan=10)
        
        #Initialise asteroid sprite
        self.asteroidSize = self.turtleSize-10
        asteroid = Image.open("images/asteroid.png")
        asteroid = asteroid.resize((self.asteroidSize,self.asteroidSize), Image.ANTIALIAS)
        self.asteroidTkImg = ImageTk.PhotoImage(asteroid)

        #Draw the turtle
        self.draw_roamer()

        # Add buttons
        tk.Button(self.master, 
                  text="↰", 
                  height=3,
                  width=9,
                  command=lambda: self.roamer.rotate_left(self)).grid(column=0, row=1)
        tk.Button(self.master, 
                  text="↑",
                  height=3,
                  width=9,
                  command=lambda: self.roamer.move_forward(self)).grid(column=1, row=1)
        tk.Button(self.master, 
                  text="↱", 
                  height=3,
                  width=9,
                  command=lambda: self.roamer.rotate_right(self)).grid(column=2, row=1)

        tk.Button(self.master, 
                  text="Start \nProgramming", 
                  height=3,
                  width=9,
                  command=lambda: self.roamer.start_programming(self)).grid(column=0, row=2)
        tk.Button(self.master, 
                  text="Play", 
                  height=3,
                  width=9,
                  command=lambda: self.roamer.play_programming(self)).grid(column=1, row=2)
        tk.Button(self.master, 
                  text="Reset",
                  height=3,
                  width=9,
                  command=self.reset_board).grid(column=2, row=2)
        tk.Button(self.master, 
                  text="Space \nTurtles",
                  height=3,
                  width=9,
                  command=self.set_game_board).grid(column=1, row=3)

    #Function to add a label for the programming
    def add_command_label(self,text):
        label = Label(self.master, 
                      text=text,
                      height = 1,
                      font=('Helvetica','12'))
        label.place(x=self.canvasSize,y=17*(len(self.labels)))
        self.labels.append(label)

    #Funtion to draw the roamer line on moving
    def add_roamer_line(self, startCoords, finCoords):
        self.lines.append(self.canvas.create_line(startCoords[0], 
                                startCoords[1], 
                                finCoords[0], 
                                finCoords[1], 
                                fill="black", 
                                width=1))

    #Function to redraw the roamer/turtle
    def draw_roamer(self):
        turtle = Image.open("images/turtle.png")
        turtle = turtle.resize((self.turtleSize,self.turtleSize), Image.ANTIALIAS)
        self.turtleTkImg = ImageTk.PhotoImage(turtle.rotate(-self.roamer.direction))
        self.canvasTurtle = self.canvas.create_image(self.roamer.coords[0]-self.turtleSize/2,self.roamer.coords[1]-self.turtleSize/2, anchor=tk.NW, image=self.turtleTkImg)

        print(self.roamer.coords)
        #This could probably go elsewhere for efficiency's sake but for now it lies here
        if self.roamer.coords in self.asteroid_coords:
            print("You sunk my battleship")
            self.eat_asteroid(self.roamer.coords)

    #Function to highlight the programming commands as they are called
    def highlight_command(self, num):
        for i in range(len(self.labels)):
            if (i == num):
                self.labels[i].config(bg="light green")
            else:
                #Ensure all other commands aren't highlighted
                self.labels[i].config(bg="white")

    def clear_labels(self):
        #Destroy each label
        for label in self.labels:
            label.destroy()
        
        #Reset list
        self.labels = []
    
    def clear_lines(self):
        #Destroy each line
        for line in self.lines:
            self.canvas.delete(line)
        
        #Reset list
        self.lines = []
    
    #Function to reset the board
    def reset_board(self):
        self.clear_labels()
        self.clear_lines()
        self.clear_all_asteroids()
        self.clear_checkerboard()
        self.roamer.reset_roamer(self, [self.canvasSize/2, self.canvasSize/2])

    #Function to set the game board
    def set_game_board(self):
        #Reset board
        self.clear_labels()
        self.clear_lines()
        self.roamer.reset_roamer(self, [self.canvasSize-self.turtleSize,self.canvasSize-self.turtleSize])

        #Reset any previous asteroids
        self.asteroid_coords = []
        self.clear_all_asteroids()

        #Draw checkerboard
        self.draw_checkerboard()

        #Create asteroids, ensuring they will be on turtles path and not ontop of the turtles spawn
        for i in range(5):
            while True:
                self.asteroid_coords.append([self.canvasSize - np.random.randint(low=1, high=self.canvasSize/self.turtleSize)*self.turtleSize,
                                             self.canvasSize - np.random.randint(low=1, high=self.canvasSize/self.turtleSize)*self.turtleSize])
                if (self.asteroid_coords[i] != [self.canvasSize-self.turtleSize, self.canvasSize-self.turtleSize]):
                    break
            self.draw_asteroid(self.asteroid_coords[i])

    #Draw asteroid at the coordinate
    def draw_asteroid(self, coords):
        print(coords)
        self.asteroids.append(self.canvas.create_image(coords[0]-self.asteroidSize/2,coords[1]-self.asteroidSize/2, anchor=tk.NW, image=self.asteroidTkImg))

    #Clear all asteroids from the board
    def clear_all_asteroids(self):
        for asteroid in self.asteroids:
            self.canvas.delete(asteroid)
        
        #Reset list
        self.asteroids = []
    
    def eat_asteroid(self, coords):
        #Get index of coord in list
        idx = self.asteroid_coords.index(coords)
        
        #Remove from board and list of asteroids
        self.canvas.delete(self.asteroids[idx])
        self.asteroids.remove(self.asteroids[idx])

        #Remove from asteroid coords
        self.asteroid_coords.remove(coords)
    
    #Function to draw dots on the board so it is easier to get asteroids
    def draw_checkerboard(self):
        for i in range(0, self.canvasSize, self.turtleSize):
            for j in range(0, self.canvasSize, self.turtleSize):
                self.draw_cross([self.canvasSize-i, self.canvasSize-j])

    #Helper function for the draw_checkerboard
    def draw_cross(self, coords):
        self.cross_lines.append(self.canvas.create_line(coords[0]-2, 
                                coords[1], 
                                coords[0]+2, 
                                coords[1], 
                                fill="black", 
                                width=1))

        self.cross_lines.append(self.canvas.create_line(coords[0], 
                                coords[1]-2, 
                                coords[0], 
                                coords[1]+2, 
                                fill="black", 
                                width=1))
    
    def clear_checkerboard(self):
        for cross_line in self.cross_lines:
            self.canvas.delete(cross_line)

        self.cross_lines = []

