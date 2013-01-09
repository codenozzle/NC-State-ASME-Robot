import pygame
import serial
from Constants import Constants
from Servo import Servo

class GamePad:
    
    joy = []
    x1 = 0
    y1 = 0
    serial = None
    servo = None
        
    def __init__(self):
        try:
            print "Acquiring connection: %s\n" % Constants.CONNECTION_STRING
            self.serial = serial.Serial(Constants.CONNECTION_STRING, Constants.BAUD_RATE)
            self.servo = Servo(self.serial)
        except:
            print "Unable to connect\n"
        print "Successfully connected"
        
        # initialize pygame
        pygame.joystick.init()
        pygame.display.init()
        if not pygame.joystick.get_count():
            print "Please connect a gamepad and try again\n"
            self.exit()
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joy.append(joystick)
            print " - Gamepad %d: " % (i) + self.joy[i].get_name()
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
                self.servo.setMotorPosition(self.x1, self.y1)

            if (axis == 1):
                self.y1 = value
                self.servo.setMotorPosition(self.x1, self.y1)

            if (axis == 2):
                self.servo.setVelocity(Constants.TURRET_BASE, value)    

            if (axis == 3):
                self.servo.setVelocity(Constants.CAMERA, value)
                self.servo.setVelocity(Constants.LEFT_SHOULDER, value)
                self.servo.setVelocity(Constants.RIGHT_SHOULDER, value)

        elif event.type == pygame.JOYBUTTONDOWN:
            button = event.dict['button']
            
            # Button 0 (trigger) to quit
            if (button == 9):
                print "Connection closed\n"
                self.exit()

            if (button == 1):
                self.servo.decrement(Constants.LEFT_ARM, 5)
                self.servo.decrement(Constants.RIGHT_ARM, 5)

            if (button == 3):
                self.servo.increment(Constants.LEFT_ARM, 5)
                self.servo.increment(Constants.RIGHT_ARM, 5)
                
        else:
            pass

    # wait for joystick input
    def joystickControl(self):
        while True:
            event = pygame.event.wait()
            if (event.type == pygame.JOYAXISMOTION or event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP):
                self.handleJoyEvent(event)

    def exit(self):
        self.serial.close()
        quit()

# allow use as a module or stand alone script
if __name__ == "__main__":
    GamePad()
    
