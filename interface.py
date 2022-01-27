import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from roamer import RobotRoamer
import sys
import os

class Interface:
    def __init__(self, master, canvasSize, turtleSize):
        #Initialise the interface
        self.master = master
        self.canvasSize = canvasSize
        self.turtleSize = turtleSize #Turtle size, determines size of turtle and step size
        self.roamer = RobotRoamer(self.canvasSize)
        self.labels = [] #List of labels so am able to highlight as they play
        self.canvas = tk.Canvas(master, bg="white", width=canvasSize+200, height=canvasSize)
        self.canvas.grid(column=0, row=0, columnspan=7)

        #Draw the turtle
        turtle = Image.open("images/turtle.png")
        turtle = turtle.resize((self.turtleSize,self.turtleSize), Image.ANTIALIAS)
        self.turtleTkImg = ImageTk.PhotoImage(turtle)
        self.canvasTurtle = self.canvas.create_image(self.roamer.coords[0]-self.turtleSize/2,self.roamer.coords[1]-self.turtleSize/2, anchor=tk.NW, image=self.turtleTkImg)

        # Add buttons
        tk.Button(self.master, 
                  text="↰", 
                  height=6,
                  width=10,
                  command=lambda: self.roamer.rotate_left(self)).grid(column=0, row=1)
        tk.Button(self.master, 
                  text="↑",
                  height=6,
                  width=10,
                  command=lambda: self.roamer.move_forward(self)).grid(column=1, row=1)
        tk.Button(self.master, 
                  text="↱", 
                  height=6,
                  width=10,
                  command=lambda: self.roamer.rotate_right(self)).grid(column=2, row=1)

        tk.Button(self.master, 
                  text="Start \nProgramming", 
                  height=6,
                  width=10,
                  command=lambda: self.roamer.start_programming()).grid(column=0, row=2)
        tk.Button(self.master, 
                  text="Play", 
                  height=6,
                  width=10,
                  command=lambda: self.roamer.play_programming(self)).grid(column=1, row=2)
        tk.Button(self.master, 
                  text="Reset",
                  height=6,
                  width=10,
                  command=self.reset_board).grid(column=2, row=2)

    #Function to add a label for the programming
    def add_command_label(self,text):
        label = Label(self.master, 
                      text=text,
                      height = 1,
                      font=('Helvetica','20'))
        label.place(x=self.canvasSize,y=30*(len(self.labels)))
        self.labels.append(label)

    #Funtion to draw the roamer line on moving
    def add_roamer_line(self, startCoords, finCoords):
        self.canvas.create_line(startCoords[0], 
                                startCoords[1], 
                                finCoords[0], 
                                finCoords[1], 
                                fill="black", 
                                width=1)

    #Function to redraw the roamer/turtle
    def draw_roamer(self):
        turtle = Image.open("images/turtle.png")
        turtle = turtle.resize((self.turtleSize,self.turtleSize), Image.ANTIALIAS)
        self.turtleTkImg = ImageTk.PhotoImage(turtle.rotate(-self.roamer.direction))
        self.canvasTurtle = self.canvas.create_image(self.roamer.coords[0]-self.turtleSize/2,self.roamer.coords[1]-self.turtleSize/2, anchor=tk.NW, image=self.turtleTkImg)

    #Function to highlight the programming commands as they are called
    def highlight_command(self, num):
        if (num < 1): 
            return
        for i in range(len(self.labels)):
            if (i == num):
                self.labels[i-1].config(bg="light green")
            else:
                self.labels[i-1].config(bg="white")
    
    #Function to reset the roamer
    def reset_board(self):
        #I was going to clear all visible lines and labels and reset coords and direction
        #But this is much easier
        python = sys.executable
        os.execl(python, python, * sys.argv)

    