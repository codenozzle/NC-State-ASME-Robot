class Constants:
    
    # Camera parameters
    CAMERA_IP = "192.168.1.106"
    CAMERA_USERNAME = "admin"
    CAMERA_PASSWORD = "hvyw82500"
    
    # Serial parameters
    CONNECTION_STRING = "/dev/tty.usbserial-A8008Hsz"
    BAUD_RATE = 115200

    # GUI application title
    APP_TITLE = "Live Video Stream: " + CAMERA_IP;

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
    TURRET_BASE = 1
    CAMERA = 2
    LEFT_SHOULDER = 3
    RIGHT_SHOULDER = 4
    LEFT_ARM = 5
    RIGHT_ARM = 6
    LEFT_MOTOR = 7
    RIGHT_MOTOR = 8