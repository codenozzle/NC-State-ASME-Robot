#!/usr/bin/python

import threading
import time
from gamepad import GamePad
from camera import *

def gui():
   print 'GUI'
   gui = GUI()
   gui.main()

def gamePad():
   print 'gamePad'
   gamePad = GamePad()
   gamePad.main()

t = threading.Thread(name='gui', target=gui)
t.start()
t.setDaemon(True)
#time.sleep(3)
#w = threading.Thread(name='gamePad', target=gamePad)
#w.start()
#w.setDaemon(True)
