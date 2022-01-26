from turtle import turtles
import numpy as np
import tkinter as tk
from PIL import Image,ImageTk

window = tk.Tk()

coords = [250, 250]

#in degrees from forward (+ve clockwise)
direction = 0

canvas = tk.Canvas(window, bg="white", height=500, width=500)
canvas.grid(column=0, row=0, columnspan=4)

# image = Image.open(Image_Location)
# image = image.resize((250, 250), Image.ANTIALIAS) ## The (250, 250) is (height, width)
# self.pw.pic = ImageTk.PhotoImage(image)

turtleSize = 40
turtle = Image.open("images/turtle.png")
turtle = turtle.resize((turtleSize,turtleSize), Image.ANTIALIAS)
turtle = ImageTk.PhotoImage(turtle)
turtleImg = canvas.create_image(250-turtleSize/2,250-turtleSize/2, anchor=tk.NW, image=turtle)


def move_forward():
    canvas.create_line(coords[0], coords[1], coords[0] + np.sin(direction*(np.pi/180))*turtleSize, coords[1] - np.cos(direction*(np.pi/180))*turtleSize, fill="black", width=1)
    coords[0] += np.sin(direction*(np.pi/180))*turtleSize
    coords[1] -= np.cos(direction*(np.pi/180))*turtleSize
    canvas.move(turtleImg, np.sin(direction*(np.pi/180))*turtleSize, -np.cos(direction*(np.pi/180))*turtleSize)

def turn_left():
    global direction
    direction -= 90

def turn_right():
    global direction
    direction += 90

tk.Button(window, 
          text="↰", 
          height=7,
          width=10,
          command=turn_left).grid(column=0, row=1)
tk.Button(window, 
          text="↑",
          height=7,
          width=10,
          command=move_forward).grid(column=1, row=1)
tk.Button(window, 
          text="↱", 
          height=7,
          width=10,
          command=turn_right).grid(column=2, row=1)


window.mainloop()
