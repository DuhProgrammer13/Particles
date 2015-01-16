__author__ = 'Kody'

import time

lastTime = time.time()
deltaTime = 0
def __init__():
    print "Hello"

def getTime():
    global lastTime
    deltaTime = time.time() - (lastTime)
    deltaTime *= 100
    lastTime = time.time()
    return deltaTime
