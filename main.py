import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
import sys
import os

class RobotRoamer(object):
    def __init__(self, master, canvasSize, turtleSize, **kwargs):
        #Initialise the roamer
        self.master = master
        self.canvasSize = canvasSize
        self.turtleSize = turtleSize #Turtle size, determines size of turtle and step size
        self.direction = 0 #Direction of the turtle
        self.coords = [canvasSize/2, canvasSize/2] #Starting position of the turtle
        self.commands = [] #List of programmed commands
        self.commandsText = [] #List of texts so able to highlight as they play
        self.programming = False #Bool to indicate whether we are currently programming the turtle
        self.canvas = tk.Canvas(master, bg="white", width=canvasSize+200, height=canvasSize)
        self.canvas.grid(column=0, row=0, columnspan=7)

        #Draw the turtle
        turtle = Image.open("images/turtle.png")
        turtle = turtle.resize((self.turtleSize,self.turtleSize), Image.ANTIALIAS)
        self.turtleTkImg = ImageTk.PhotoImage(turtle)
        self.canvas.create_image(self.coords[0]-self.turtleSize/2,self.coords[1]-self.turtleSize/2, anchor=tk.NW, image=self.turtleTkImg)

        #Add buttons
        tk.Button(window, 
                  text="↰", 
                  height=6,
                  width=10,
                  command=self.turn_left).grid(column=0, row=1)
        tk.Button(window, 
                  text="↑",
                  height=6,
                  width=10,
                  command=self.move_forward).grid(column=1, row=1)
        tk.Button(window, 
                  text="↱", 
                  height=6,
                  width=10,
                  command=self.turn_right).grid(column=2, row=1)

        tk.Button(window, 
                  text="Start \nProgramming", 
                  height=6,
                  width=10,
                  command=self.start_programming).grid(column=0, row=2)
        tk.Button(window, 
                  text="Play", 
                  height=6,
                  width=10,
                  command=self.play_programming).grid(column=1, row=2)
        tk.Button(window, 
                  text="Reset",
                  height=6,
                  width=10,
                  command=self.reset_board).grid(column=2, row=2)


    def move_forward(self):
        if (self.programming):
            self.commands.append("FORWARD")
            label = Label(self.master, 
                          text="FORWARD",
                          height = 1,
                          font=('Helvetica','20'))
            label.place(x=self.canvasSize,y=30*(len(self.commands)))
            self.commandsText.append(label)
        else:
            self.canvas.create_line(self.coords[0], 
                                    self.coords[1], 
                                    self.coords[0] + np.sin(self.direction*(np.pi/180))*self.turtleSize, 
                                    self.coords[1] - np.cos(self.direction*(np.pi/180))*self.turtleSize, fill="black", width=1)
            self.coords[0] += np.sin(self.direction*(np.pi/180))*self.turtleSize
            self.coords[1] -= np.cos(self.direction*(np.pi/180))*self.turtleSize
            self.draw_turtle()


    def turn_left(self):  
        if (self.programming):
            self.commands.append("ROTATE LEFT")
            label = Label(self.master, 
                          text="ROTATE LEFT",
                          height = 1,
                          font=('Helvetica','20'))
            label.place(x=self.canvasSize,y=30*(len(self.commands)))
            self.commandsText.append(label)
        else:
            self.direction -= 90
            self.draw_turtle()

    def turn_right(self):
        if (self.programming):
            self.commands.append("ROTATE RIGHT")
            label = Label(self.master, 
                          text="ROTATE RIGHT",
                          height = 1,
                          font=('Helvetica','20'))
            label.place(x=self.canvasSize,y=30*(len(self.commands)))
            self.commandsText.append(label)
        else:
            self.direction += 90
            self.draw_turtle()
        
    def draw_turtle(self):
        turtle = Image.open("images/turtle.png")
        turtle = turtle.resize((self.turtleSize,self.turtleSize), Image.ANTIALIAS)
        self.turtleTkImg = ImageTk.PhotoImage(turtle.rotate(-self.direction))
        self.canvas.create_image(self.coords[0]-self.turtleSize/2,self.coords[1]-self.turtleSize/2, anchor=tk.NW, image=self.turtleTkImg)

    def start_programming(self):
        self.programming = True

    def play_programming(self):
        self.programming = False
        self.update_turtle(self.master, iter(self.commands), 0)
        #I feel like there should be a way to do this without the number using enumerate
        #instead of iter but I can't figure it out right now

    def update_turtle(self, app, commands, num):
        command = next(commands, None)
        if command is None:
            self.commandsText[num-1].config(bg="light green")
            self.commandsText[num-2].config(bg="white")
            return
        if (num > 0):
            self.commandsText[num-1].config(bg="light green")
        if (num > 1):
            self.commandsText[num-2].config(bg="white")
        delay = 1000
        if (command == "FORWARD"):
            app.after(delay, self.move_forward)
        if (command == "ROTATE LEFT"):
            app.after(delay, self.turn_left)
        if (command == "ROTATE RIGHT"):
            app.after(delay, self.turn_right)
        app.after(delay, self.update_turtle, app, commands, num+1)

    def reset_board(self):
        #I was going to simply clear all visible lines and labels and reset coords and direction
        #But this is much easier
        python = sys.executable
        os.execl(python, python, * sys.argv)
            



window = tk.Tk()
robotRoamer = RobotRoamer(window, 550, 40)

# turtle = Image.open("images/turtle.png")
# turtle = turtle.resize((40,40), Image.ANTIALIAS)
# turtleTkImg = ImageTk.PhotoImage(turtle)
# robotRoamer.canvas.create_image(250,250, anchor=tk.NW, image=turtleTkImg)

window.mainloop()
