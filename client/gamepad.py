#!/usr/bin/env python

from servo import Servo
import pygame
import serial

class GamePad:
    
    joy = []
    x1 = 0
    y1 = 0
    serial = serial.Serial('/dev/tty.usbserial-A8008Hsz', 115200)
        
    # handle joystick event
    def handleJoyEvent(self, e, servo):
        if e.type == pygame.JOYAXISMOTION:
            axis = e.dict['axis']
            
            if (axis == 0):
                self.x1 = e.dict['value']
                servo.setMotorPosition(self.x1, self.y1, self.serial)

            if (axis == 1):
                self.y1 = e.dict['value']
                servo.setMotorPosition(self.x1, self.y1, self.serial)

            if (axis == 2):
                servo.setVelocity(1, e.dict['value'], self.serial)    

            if (axis == 3):
                servo.setVelocity(2, e.dict['value'], self.serial)
                servo.setVelocity(3, e.dict['value'], self.serial)
                servo.setVelocity(4, e.dict['value'], self.serial)

        elif e.type == pygame.JOYBUTTONDOWN:
            # Button 0 (trigger) to quit
            if (e.dict['button'] == 9):
                print "Bye!\n"
                quit()

            if (e.dict['button'] == 1):
                servo.decrement(5, 5, self.serial)
                servo.decrement(6, 5, self.serial)

            if (e.dict['button'] == 3):
                servo.increment(5, 5, self.serial)
                servo.increment(6, 5, self.serial)
                
        else:
            pass

    # wait for joystick input
    def joystickControl(self, servo):
        while True:
            e = pygame.event.wait()
            if (e.type == pygame.JOYAXISMOTION or e.type == pygame.JOYBUTTONDOWN or e.type == pygame.JOYBUTTONUP):
                self.handleJoyEvent(e, servo)

    # main method
    def main(self):
        servo = Servo()
        # initialize pygame
        pygame.joystick.init()
        pygame.display.init()
        if not pygame.joystick.get_count():
            print "\nPlease connect a joystick and run again.\n"
            print pygame.joystick.get_count()
            quit()
        print "\n%d joystick(s) detected." % pygame.joystick.get_count()
        for i in range(pygame.joystick.get_count()):
            myjoy = pygame.joystick.Joystick(i)
            myjoy.init()
            self.joy.append(myjoy)
            print "Joystick %d: " % (i) + self.joy[i].get_name()
        print "Depress trigger (button 10) to quit.\n"

        # run joystick listener loop
        self.joystickControl(servo)

# allow use as a module or standalone script
if __name__ == "__main__":
    gamePad = GamePad()
    gamePad.main()
    
