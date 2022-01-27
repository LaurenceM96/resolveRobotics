import numpy as np

class RobotRoamer:
    def __init__(self, canvasSize):
        self.direction = 0 #Direction of the roamer
        self.coords = [canvasSize/2, canvasSize/2] #Starting position of the roamer
        self.commands = [] #List of programmed commands
        self.programming = False #Bool to indicate whether we are currently programming the turtle
    
    #Function called to either add this command to list, or to perform action
    def move_forward(self, interface):
        if (self.programming):
            self.commands.append("FORWARD")
            interface.add_command_label("FORWARD")
        else:
            self.animate_movement(interface, 0)
    
    #Function to animate the forward movement of the roamer
    def animate_movement(self, interface, dist):
        #When desired distance is reached, stop animation
        if (dist >= interface.turtleSize):
            interface.draw_roamer()
            return

        #Perform small increments to animate movement
        startCoords = self.coords.copy()
        self.coords[0] += int(np.sin(self.direction*(np.pi/180))*2)
        self.coords[1] -= int(np.cos(self.direction*(np.pi/180))*2)
        interface.add_roamer_line(startCoords, self.coords)
        interface.draw_roamer()
        interface.master.after(5, self.animate_movement, interface, dist+2)

    #Function called to either add this command to list, or to perform action
    def rotate_left(self, interface):
        if (self.programming):
            self.commands.append("ROTATE LEFT")
            interface.add_command_label("ROTATE LEFT")
        else:
            self.animate_rotation(interface, 0, "l")
    
    #Function called to either add this command to list, or to perform action
    def rotate_right(self, interface):
        if (self.programming):
            self.commands.append("ROTATE RIGHT")
            interface.add_command_label("ROTATE RIGHT")
        else:
            self.animate_rotation(interface, 0, "r")
    
    #Funtions to animate rotation
    def animate_rotation(self, interface, angle, direction):
        #When desired angle is reached, stop animation
        if (angle >= 90):
            interface.draw_roamer()
            return
        
        #Add small increments to direction on each call to animate
        if direction == "r":
            self.direction += 3
        elif direction == "l":
            self.direction -= 3
        interface.draw_roamer()
        interface.master.after(5, self.animate_rotation, interface, angle+3, direction)

    #Function to begin programming the roamer
    def start_programming(self, interface):
        #Clear the commands first
        self.commands = []
        interface.clear_labels()

        self.programming = True
    
    #This function is called to begin the sequence of inputted commands
    def play_programming(self, interface):
        self.programming = False
        self.run_commands(interface, iter(self.commands), 0, 1000)
        #I feel like there should be a way to do this without the number using enumerate
        #instead of iter but I can't figure it out right now

    # This function enables the commands to run in sequence with time delays between each
    def run_commands(self, interface, commands, num, delay):
        #Get next command, if it is None, then we have reached the end, so stop
        command = next(commands, None)
        if command is None:
            return

        #Highlight the current command being executed and perform it.
        interface.highlight_command(num)
        if (command == "FORWARD"):
            interface.master.after(0, self.move_forward, interface)
        if (command == "ROTATE LEFT"):
            interface.master.after(0, self.rotate_left, interface)
        if (command == "ROTATE RIGHT"):
            interface.master.after(0, self.rotate_right, interface)
        interface.master.after(delay, self.run_commands, interface, commands, num+1, 1000)

    # Function to reset the roamers commands, direction and location to coords given
    def reset_roamer(self, interface, coords):
        self.commands=[]
        interface.clear_labels()
        self.programming = False
        self.direction = 0
        self.coords = coords
        interface.draw_roamer()