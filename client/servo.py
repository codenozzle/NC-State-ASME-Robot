from Constants import Constants

class Servo:

    servos = (
        [0, 90, 180, Constants.INVERTED],  # Turret Base
        [0, 90, 180, Constants.STANDARD],  # Camera Vertical
        [0, 90, 180, Constants.INVERTED],  # Left Shoulder Vertical
        [0, 90, 180, Constants.STANDARD],  # Right Shoulder Vertical
        [0, 90, 180, Constants.INVERTED],  # Left Cannon
        [0, 90, 180, Constants.STANDARD],  # Right Cannon
        [0, 90, 180, Constants.STANDARD],  # Left Motor
        [0, 90, 180, Constants.STANDARD]  # Right Motor
    )

    servoPositions = (
        [servos[0][Constants.CENTER]],
        [servos[1][Constants.CENTER]],
        [servos[2][Constants.CENTER]],
        [servos[3][Constants.CENTER]],
        [servos[4][Constants.CENTER]],
        [servos[5][Constants.CENTER]],
        [servos[6][Constants.CENTER]],
        [servos[7][Constants.CENTER]]
    )
    serial = None
    
    def __init__(self, serial):
        self.serial = serial
        
    def move(self, servoNumber):
        self.serial.write(chr(255))
        self.serial.write(chr(servoNumber))
        self.serial.write(chr(self.servoPositions[servoNumber - 1][Constants.POSITION]))

    def increment(self, servoNumber, amount):
        if (self.servos[servoNumber - 1][Constants.DIRECTION] == 1):
            amount = amount * -1
        servoPosition = self.servoPositions[servoNumber - 1][Constants.POSITION] + amount
        if (servoPosition > self.servos[servoNumber - 1][Constants.END]):
            servoPosition = self.servos[servoNumber - 1][Constants.END]
        if (servoPosition < self.servos[servoNumber - 1][Constants.START]):
            servoPosition = self.servos[servoNumber - 1][Constants.START] 
        self.setServoPosition(servoNumber, servoPosition)

    def decrement(self, servoNumber, amount):
        if (self.servos[servoNumber - 1][Constants.DIRECTION] == 1):
            amount = amount * -1
        servoPosition = self.servoPositions[servoNumber - 1][Constants.POSITION] - amount
        if (servoPosition > self.servos[servoNumber - 1][Constants.END]):
            servoPosition = self.servos[servoNumber - 1][Constants.END]
        if (servoPosition < self.servos[servoNumber - 1][Constants.START]):
            servoPosition = self.servos[servoNumber - 1][Constants.START] 
        self.setServoPosition(servoNumber, servoPosition)
        
    def setVelocity(self, servoNumber, velocity):
        rotation = 0
        
        if (self.servos[servoNumber - 1][Constants.DIRECTION] == 1):
            velocity = velocity * -1

        if (velocity == 0):
            rotation = self.servos[servoNumber - 1][Constants.CENTER]
        elif (velocity > self.servos[servoNumber - 1][Constants.CENTER]):
            resolution = (self.servos[servoNumber - 1][Constants.END] - self.servos[servoNumber - 1][Constants.CENTER])
            rotation = self.servos[servoNumber - 1][Constants.CENTER] + (resolution * velocity)
        elif (velocity < self.servos[servoNumber - 1][Constants.CENTER]):
            resolution = (self.servos[servoNumber - 1][Constants.CENTER] - self.servos[servoNumber - 1][Constants.START])
            rotation = self.servos[servoNumber - 1][Constants.CENTER] - (resolution * velocity)

        self.setServoPosition(servoNumber, rotation)

    def setServoPosition(self, servoNumber, rotation):
        # print repr(servoNumber) + ": " + repr(rotation)
        # if (servoNumber == 1):
        self.servoPositions[servoNumber - 1][Constants.POSITION] = int(round(rotation))
        self.move(servoNumber)

    def setMotorPosition(self, x, y):
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


        self.setVelocity(7, left)
        self.setVelocity(8, right)
        # print "x: " + repr(x) + " y: " + repr(y) + " d: " + repr(distance)
        # print "left: " + repr(left) + " right: " + repr(right)







        
