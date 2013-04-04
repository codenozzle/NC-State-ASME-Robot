import pygame
import serial
import math
from Config import Config

class GamePad:
    
    joy = []
    x1 = 0
    y1 = 0
    x2 = 0
    serial = None
    servo = None
        
    def __init__(self):
        config = Config()
        try:
            print "Connecting to robot..."
            self.serial = serial.Serial(config.getComPort(), config.getBaudRate())
            self.servo = Servo(self.serial)
        except serial.SerialException, e:
            print "   Error: ", e
            self.exit()
            
        print "   Successfully connected to %s\n" % config.getComPort()
        
        # initialize pygame
        print "Connecting to gamepad..."
        pygame.joystick.init()
        pygame.display.init()
        if not pygame.joystick.get_count():
            print "   Please connect a gamepad and try again\n"
            self.exit()
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joy.append(joystick)
            print "   Successfully connected to %s" % self.joy[i].get_name()
        print "\nPress button 10 to quit\n"

        # run joystick listener loop
        self.joystickControl()
        
    # handle joystick event
    def handleJoyEvent(self, event):
        if event.type == pygame.JOYAXISMOTION:
            axis = event.dict['axis']
            value = event.dict['value']
            
            if (axis == 0):
                self.x1 = value
                self.servo.wheelControl(self.x1, self.y1, self.x2)

            if (axis == 1):
                self.y1 = value
                self.servo.wheelControl(self.x1, self.y1, self.x2)

            if (axis == 2):
                self.x2 = value
                self.servo.wheelControl(self.x1, self.y1, self.x2)

        elif event.type == pygame.JOYBUTTONDOWN:
            button = event.dict['button']
            
            # Button 0 (trigger) to quit
            if (button == 9):
                self.exit()

            if (button == 0):
                self.servo.update(Servo.CLAW, -1)

            if (button == 2):
                self.servo.update(Servo.CLAW, 0.8)

            if (button == 1):
                self.servo.update(Servo.ARM, 0.7)

            if (button == 3):
                self.servo.update(Servo.ARM, -1)
                
            if (button == 7):
                self.servo.decrement(Servo.CLAW, 5)
                
            if (button == 6):
                self.servo.decrement(Servo.ARM, 10)

            if (button == 5):
                self.servo.increment(Servo.CLAW, 5)
            
            if (button == 4):
                self.servo.increment(Servo.ARM, 10)
                
        else:
            pass
        
    # wait for joystick input
    def joystickControl(self):
        while True:
            event = pygame.event.wait()
            if (event.type == pygame.JOYAXISMOTION or 
                event.type == pygame.JOYBUTTONDOWN or 
                event.type == pygame.JOYBUTTONUP):
                self.handleJoyEvent(event)

    def exit(self):
        if (self.serial is not None):
            self.serial.close()
        print "Shutting down"
        quit()
        
class Servo:

    # Servo rotation
    STANDARD = 0
    INVERTED = 1

    # Servo points and direction
    START = 0
    CENTER = 1
    END = 2
    DIRECTION = 3

    # Rotation degrees
    POSITION = 0
    
    # Servo IDs
    LEFT_FRONT_MOTOR = 1
    RIGHT_FRONT_MOTOR = 2
    REAR_MOTOR = 3
    ARM = 4
    CLAW = 5
    
    # Arduino serial start Flag for next byte tuple
    START_FLAG = 255
    
    servos = (
        [26, 96, 166, STANDARD],  # Left Front Motor
        [20, 90, 160, STANDARD],  # Right Front Motor
        [20, 90, 160, STANDARD],  # Rear Motor
        [90, 150, 180, STANDARD],  # Arm
        [0, 90, 180, STANDARD]   # Claw
    )

    servoPositions = (
        [servos[0][CENTER]],
        [servos[1][CENTER]],
        [servos[2][CENTER]],
        [servos[3][CENTER]],
        [servos[4][CENTER]]
    )
    serial = None
    
    def __init__(self, serial):
        self.serial = serial
        for servoNumber in xrange(1, len(self.servos)):
            self.update(servoNumber+1, 0.5)

    def increment(self, servoNumber, amount):
        if (self.servos[servoNumber - 1][self.DIRECTION] == 1):
            amount = amount * -1
        servoPosition = self.servoPositions[servoNumber - 1][self.POSITION] + amount
        if (servoPosition > self.servos[servoNumber - 1][self.END]):
            servoPosition = self.servos[servoNumber - 1][self.END]
        if (servoPosition < self.servos[servoNumber - 1][self.START]):
            servoPosition = self.servos[servoNumber - 1][self.START]
        self.servoPositions[servoNumber - 1][self.POSITION] = int(round(servoPosition))
        self.updateArduino(servoNumber)

    def decrement(self, servoNumber, amount):
        if (self.servos[servoNumber - 1][self.DIRECTION] == 1):
            amount = amount * -1
        servoPosition = self.servoPositions[servoNumber - 1][self.POSITION] - amount
        if (servoPosition > self.servos[servoNumber - 1][self.END]):
            servoPosition = self.servos[servoNumber - 1][self.END]
        if (servoPosition < self.servos[servoNumber - 1][self.START]):
            servoPosition = self.servos[servoNumber - 1][self.START]
        self.servoPositions[servoNumber - 1][self.POSITION] = int(round(servoPosition))
        self.updateArduino(servoNumber)
        
    def update(self, servoNumber, rotation):
        servoRotation = 0
        
        if (self.servos[servoNumber - 1][self.DIRECTION] == 1):
            rotation = rotation * -1

        if (rotation == 0):
            servoRotation = self.servos[servoNumber - 1][self.CENTER]
        elif (rotation > self.servos[servoNumber - 1][self.CENTER]):
            resolution = (self.servos[servoNumber - 1][self.END] - self.servos[servoNumber - 1][self.CENTER])
            servoRotation = self.servos[servoNumber - 1][self.CENTER] + (resolution * rotation)
        elif (rotation < self.servos[servoNumber - 1][self.CENTER]):
            resolution = (self.servos[servoNumber - 1][self.CENTER] - self.servos[servoNumber - 1][self.START])
            servoRotation = self.servos[servoNumber - 1][self.CENTER] - (resolution * rotation)

        self.servoPositions[servoNumber - 1][self.POSITION] = int(round(servoRotation))
        self.updateArduino(servoNumber)
        #print "servoNumber: " + repr(servoNumber) + " servoRotation: " + repr(servoRotation)

    def wheelControl(self, x, y, r):
##        power1 = x - (0.5 * r)
##        power2 = (-0.5 * x) - (0.866 * y) - (0.5 * r)
##        power3 = (-0.5 * x) + (0.866 * y) - (0.5 * r) #3/5 added updated formulas and defined above relationships. 
##        wheelPower = self.scale([power1, power2, power3])
##        
##        self.update(self.LEFT_FRONT_MOTOR, wheelPower[2])
##        self.update(self.RIGHT_FRONT_MOTOR, wheelPower[1])
##        self.update(self.REAR_MOTOR, wheelPower[0])

        # Modify the x and y if the velocity vector exceeds 1
        v = math.sqrt((x*x) + (y*y))
        if (v > 1):
            power1 = ((x / v) - (0.5 * r))
            power2 = (-0.5 * (x / v)) - (0.866 * (y / v)) - (0.5 * r)
            power3 = (-0.5 * (x / v)) + (0.866 * (y / v)) - (0.5 * r)
            #print "power1, power2, power3: ", power1, power2, power3
        else:
            scalar = 3
            power1 = (math.pow(x, scalar)) - math.pow(r, scalar)
            power2 = (-0.5 * math.pow(x, scalar)) - (0.866 * math.pow(y, scalar)) - math.pow(r, scalar)
            power3 = (-0.5 * math.pow(x, scalar)) + (0.866 * math.pow(y, scalar)) - math.pow(r, scalar)
            
        #print "x1: " + repr(x) + " y1: " + repr(y) + " x2: " + repr(r) + " p1: " + repr(power1) + " p2: " + repr(power2) + " p3: " + repr(power3)
        self.update(self.LEFT_FRONT_MOTOR, self.constrain(power3))
        self.update(self.RIGHT_FRONT_MOTOR, self.constrain(power2))
        self.update(self.REAR_MOTOR, self.constrain(power1))
        
    def scale(self, wheelPower):
        # Create a temporary list
        tempWheelPower = wheelPower
        
        # Update the temporary list with absolute values
        for index in range(len(tempWheelPower)):
            tempWheelPower[index] = math.fabs(tempWheelPower[index])
            
        # Find max and difference
        max = max(tempWheelPower)
        difference = max - 1
        
        # Scale 
        for index in range(len(tempWheelPower)):
            if (wheelPower[index] > 0):
                wheelPower[index] = wheelPower[index] - difference
            elif (wheelPower[index] < 0):
                wheelPower[index] = wheelPower[index] + difference
            elif (wheelPower[index] == 0):
                wheelPower[index] = difference
                
        return wheelPower
    
    def constrain(self, currentValue):
        returnValue = currentValue
        if (currentValue > 0 and currentValue > 1):
            returnValue = 1
        elif (currentValue < 0 and currentValue < -1):
            returnValue = -1
        return returnValue
    
    def updateArduino(self, servoNumber):
        self.serial.write(chr(self.START_FLAG))
        self.serial.write(chr(servoNumber))
        self.serial.write(chr(self.servoPositions[servoNumber - 1][self.POSITION]))

# allow use as a module or stand alone script
if __name__ == "__main__":
    GamePad()
    
