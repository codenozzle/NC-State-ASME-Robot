import pygame
import serial
from Config import Config

class GamePad:
    
    joy = []
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
                self.servo.update(Servo.REAR_MOTOR, value)

            if (axis == 1):
                self.servo.update(Servo.LEFT_FRONT_MOTOR, value)
                self.servo.update(Servo.RIGHT_FRONT_MOTOR, value)

        elif event.type == pygame.JOYBUTTONDOWN:
            button = event.dict['button']
            
            # Button 0 (trigger) to quit
            if (button == 9):
                self.exit()

            if (button == 1):
                self.servo.increment(Servo.CLAW, 5)
                
            if (button == 2):
                self.servo.increment(Servo.ARM, 5)

            if (button == 3):
                self.servo.decrement(Servo.CLAW, 5)
            
            if (button == 4):
                self.servo.decrement(Servo.ARM, 5)
                
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
        [0, 90, 180, INVERTED],  # Left Front Motor
        [0, 90, 180, STANDARD],  # Right Front Motor
        [0, 90, 180, STANDARD],  # Rear Motor
        [0, 90, 180, STANDARD],  # Arm
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

    def steer(self, x, y):
        power = y
        rotation = abs(x)
        rightPower = power
        leftPower = power
        
        if (x > 0):
            rightPower += rotation
            leftPower -= rotation
            
        elif (x < 0):
            rightPower -= rotation
            leftPower += rotation

        self.update(self.LEFT_MOTOR, self.constrain(leftPower, power))
        self.update(self.RIGHT_MOTOR, self.constrain(rightPower, power))
        
        #print "x: " + repr(x) + " y: " + repr(y) + " r: " + repr(rotation)
        #print "left: " + repr(self.constrain(leftPower, power)) + " right: " + repr(self.constrain(rightPower, power))
        
    def constrain(self, currentValue, maxPower):
        returnValue = currentValue
        if (maxPower > 0 and currentValue > maxPower):
            returnValue = maxPower
        elif (maxPower < 0 and currentValue < maxPower):
            returnValue = maxPower
        return returnValue
    
    def updateArduino(self, servoNumber):
        self.serial.write(chr(self.START_FLAG))
        self.serial.write(chr(servoNumber))
        self.serial.write(chr(self.servoPositions[servoNumber - 1][self.POSITION]))

# allow use as a module or stand alone script
if __name__ == "__main__":
    GamePad()
    
