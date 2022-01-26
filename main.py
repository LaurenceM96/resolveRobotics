from turtle import turtles, width
import numpy as np
import tkinter as tk
from PIL import Image,ImageTk

class RobotRoamer(object):
    def __init__(self, master, canvasSize, turtleSize, **kwargs):
        self.master = master
        self.canvasSize = canvasSize
        self.turtleSize = turtleSize
        self.direction = 0
        self.coords = [canvasSize/2, canvasSize/2]
        self.canvas = tk.Canvas(master, bg="white", width=canvasSize, height=canvasSize)
        self.canvas.grid(column=0, row=0, columnspan=4)

        turtle = Image.open("images/turtle.png")
        turtle = turtle.resize((self.turtleSize,self.turtleSize), Image.ANTIALIAS)
        self.turtleTkImg = ImageTk.PhotoImage(turtle)
        self.canvas.create_image(self.coords[0]-self.turtleSize/2,self.coords[1]-self.turtleSize/2, anchor=tk.NW, image=self.turtleTkImg)

        tk.Button(window, 
                  text="↰", 
                  height=7,
                  width=10,
                  command=self.turn_left).grid(column=0, row=1)
        tk.Button(window, 
                  text="↑",
                  height=7,
                  width=10,
                  command=self.move_forward).grid(column=1, row=1)
        tk.Button(window, 
                  text="↱", 
                  height=7,
                  width=10,
                  command=self.turn_right).grid(column=2, row=1)


    def move_forward(self):
        self.canvas.create_line(self.coords[0], 
                                self.coords[1], 
                                self.coords[0] + np.sin(self.direction*(np.pi/180))*self.turtleSize, 
                                self.coords[1] - np.cos(self.direction*(np.pi/180))*self.turtleSize, fill="black", width=1)
        self.coords[0] += np.sin(self.direction*(np.pi/180))*self.turtleSize
        self.coords[1] -= np.cos(self.direction*(np.pi/180))*self.turtleSize
        self.draw_turtle()
        #self.canvas.move(turtleImg, np.sin(direction*(np.pi/180))*turtleSize, -np.cos(direction*(np.pi/180))*turtleSize)

    def turn_left(self):    
        self.direction -= 90
        self.draw_turtle()

    def turn_right(self):
        self.direction += 90
        self.draw_turtle()
        
    def draw_turtle(self):
        turtle = Image.open("images/turtle.png")
        turtle = turtle.resize((self.turtleSize,self.turtleSize), Image.ANTIALIAS)
        self.turtleTkImg = ImageTk.PhotoImage(turtle.rotate(-self.direction))
        self.canvas.create_image(self.coords[0]-self.turtleSize/2,self.coords[1]-self.turtleSize/2, anchor=tk.NW, image=self.turtleTkImg)


window = tk.Tk()
robotRoamer = RobotRoamer(window, 500, 40)

# turtle = Image.open("images/turtle.png")
# turtle = turtle.resize((40,40), Image.ANTIALIAS)
# turtleTkImg = ImageTk.PhotoImage(turtle)
# robotRoamer.canvas.create_image(250,250, anchor=tk.NW, image=turtleTkImg)

window.mainloop()
