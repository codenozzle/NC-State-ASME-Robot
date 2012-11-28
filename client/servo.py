#!/usr/bin/env python

class Servo:

    STANDARD = 0
    INVERTED = 1

    START = 0
    CENTER = 1
    END = 2
    DIRECTION = 3

    POSITION = 0

    servos = (
        [0, 90, 180, INVERTED], # Turret Base
        [0, 90, 180, STANDARD], # Camera Vertical
        [0, 90, 180, INVERTED], # Left Shoulder Vertical
        [0, 90, 180, STANDARD], # Right Shoulder Vertical
        [0, 90, 180, INVERTED], # Left Cannon
        [0, 90, 180, STANDARD], # Right Cannon
        [0, 90, 180, STANDARD], # Left Motor
        [0, 90, 180, STANDARD]  # Right Motor
    )

    servoPositions = (
        [servos[0][CENTER]],
        [servos[1][CENTER]],
        [servos[2][CENTER]],
        [servos[3][CENTER]],
        [servos[4][CENTER]],
        [servos[5][CENTER]],
        [servos[6][CENTER]],
        [servos[7][CENTER]]
    )
    
    def move(self, servoNumber, serial):
        serial.write(chr(255))
        serial.write(chr(servoNumber))
        serial.write(chr(self.servoPositions[servoNumber-1][self.POSITION]))

    def increment(self, servoNumber, amount, serial):
        if (self.servos[servoNumber-1][self.DIRECTION] == 1):
            amount = amount * -1
        servoPosition = self.servoPositions[servoNumber-1][self.POSITION] + amount
        if (servoPosition > self.servos[servoNumber-1][self.END]):
            servoPosition = self.servos[servoNumber-1][self.END]
        if (servoPosition < self.servos[servoNumber-1][self.START]):
            servoPosition = self.servos[servoNumber-1][self.START] 
        self.setServoPosition(servoNumber, servoPosition, serial)

    def decrement(self, servoNumber, amount, serial):
        if (self.servos[servoNumber-1][self.DIRECTION] == 1):
            amount = amount * -1
        servoPosition = self.servoPositions[servoNumber-1][self.POSITION] - amount
        if (servoPosition > self.servos[servoNumber-1][self.END]):
            servoPosition = self.servos[servoNumber-1][self.END]
        if (servoPosition < self.servos[servoNumber-1][self.START]):
            servoPosition = self.servos[servoNumber-1][self.START] 
        self.setServoPosition(servoNumber, servoPosition, serial)
        
    def setVelocity(self, servoNumber, velocity, serial):
        rotation = 0
        
        if (self.servos[servoNumber-1][self.DIRECTION] == 1):
            velocity = velocity * -1

        if (velocity == 0):
            rotation = self.servos[servoNumber-1][self.CENTER]
        elif (velocity > self.servos[servoNumber-1][self.CENTER]):
            resolution = (self.servos[servoNumber-1][self.END] - self.servos[servoNumber-1][self.CENTER])
            rotation = self.servos[servoNumber-1][self.CENTER] + (resolution * velocity)
        elif (velocity < self.servos[servoNumber-1][self.CENTER]):
            resolution = (self.servos[servoNumber-1][self.CENTER] - self.servos[servoNumber-1][self.START])
            rotation = self.servos[servoNumber-1][self.CENTER] - (resolution * velocity)

        self.setServoPosition(servoNumber, rotation, serial)

    def setServoPosition(self, servoNumber, rotation, serial):
        #print repr(servoNumber) + ": " + repr(rotation)
        #if (servoNumber == 1):
        self.servoPositions[servoNumber-1][self.POSITION] = int(round(rotation))
        self.move(servoNumber, serial)

    def setMotorPosition(self, x, y, serial):
        distance = abs(x) / 2
        
        if (x > 0):
            right = y + distance
            left = y - distance
            
        elif (x < 0):
            right = y - distance
            left = y + distance
            
        else:
            left = y
            right = y

        if (right < -1.00):
            right = -1

        if (left < -1.00):
            left = -1

        if (right > 1.00):
            right = 1

        if (left > 1.00):
            left = 1


        self.setVelocity(7, left, serial)
        self.setVelocity(8, right, serial)
        #print "x: " + repr(x) + " y: " + repr(y) + " d: " + repr(distance)
        #print "left: " + repr(left) + " right: " + repr(right)







        
