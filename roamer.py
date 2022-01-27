import numpy as np

class RobotRoamer:
    def __init__(self, canvasSize):
        self.direction = 0 #Direction of the roamer
        self.coords = [canvasSize/2, canvasSize/2] #Starting position of the roamer
        self.commands = [] #List of programmed commands
        self.programming = False #Bool to indicate whether we are currently programming the turtle
    
    def move_forward(self, interface):
        if (self.programming):
            self.commands.append("FORWARD")
            interface.add_command_label("FORWARD")
        else:
            self.animate_movement(interface, 0)
    
    def animate_movement(self, interface, dist):
        if (dist >= interface.turtleSize):
            interface.draw_roamer()
            return

        startCoords = self.coords.copy()
        self.coords[0] += np.sin(self.direction*(np.pi/180))*2
        self.coords[1] -= np.cos(self.direction*(np.pi/180))*2
        interface.add_roamer_line(startCoords, self.coords)
        interface.draw_roamer()
        interface.master.after(5, self.animate_movement, interface, dist+2)


    def rotate_left(self, interface):
        if (self.programming):
            self.commands.append("ROTATE LEFT")
            interface.add_command_label("ROTATE LEFT")
        else:
            self.animate_rotation(interface, 0, "l")
    
    def rotate_right(self, interface):
        if (self.programming):
            self.commands.append("ROTATE RIGHT")
            interface.add_command_label("ROTATE RIGHT")
        else:
            self.animate_rotation(interface, 0, "r")
    
    def animate_rotation(self, interface, angle, direction):
        if (angle >= 90):
            interface.draw_roamer()
            return
        if direction == "r":
            self.direction += 2
        elif direction == "l":
            self.direction -= 2
        interface.draw_roamer()
        interface.master.after(5, self.animate_rotation, interface, angle+2, direction)

    def start_programming(self):
        self.programming = True
    
    def play_programming(self, interface):
        self.programming = False
        self.run_commands(interface, iter(self.commands), 0)
        #I feel like there should be a way to do this without the number using enumerate
        #instead of iter but I can't figure it out right now

    def run_commands(self, interface, commands, num):
        command = next(commands, None)
        if command is None:
            interface.highlight_command(num+1)
            return
        interface.highlight_command(num)
        delay = 1000
        if (command == "FORWARD"):
            interface.master.after(delay, self.move_forward, interface)
        if (command == "ROTATE LEFT"):
            interface.master.after(delay, self.rotate_left, interface)
        if (command == "ROTATE RIGHT"):
            interface.master.after(delay, self.rotate_right, interface)
        interface.master.after(delay, self.run_commands, interface, commands, num+1)