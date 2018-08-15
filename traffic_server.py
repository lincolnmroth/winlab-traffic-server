import time
import RPi.GPIO as GPIO
import atexit
from flask import Flask, request, redirect, url_for
import urllib.request, json
import random
app = Flask(__name__)

PINS = { 8, 9, 4, 5, 6, 7}#Follows Green, Yellow, Red Pattern (First 3 are for 0 and the other are for 1)
GREEN_LIGHT_DELAY = 5
YELLOW_LIGHT_DELAY = 2
RED_LIGHT_DELAY = 1
dir = 'Forward'
state = 'on'

##@app.route('/newexperiment', methods = ['GET', 'POST'])
##def turn():
##    try:
##        for i in range (10000):
##            time.sleep(5)
##            thing()
##    except KeyboardInterrupt:
##        return redirect('/experimentone')
##
##

@app.route('/', methods = ['GET', 'POST'])
def test():
    return 'hello'
##
##@app.route('/experiment', methods = ['GET', 'POST'])
##def experiment():
##    getDir()
##    thing()
##    thing()
##    return 'Really'
##@app.route('/experimentone', methods = ['GET', 'POST'])
##def experimentone():
##    try:
##        for i in range (10000):
##            time.sleep(5)
##            thing()
##    except KeyboardInterrupt:
##        return redirect('/changing')
##
##@app.route('/changing')
##def experimenttwo():
##    global YELLOW_LIGHT_DELAY
##    global RED_LIGHT_DELAY
##    YELLOW_LIGHT_DELAY = random.randint(2,4)*1
##    RED_LIGHT_DELAY = random.randint(2,4)*1
##    return redirect('/newexperiment')
##

@app.route('/changeDir', methods=['POST'])
def thing():
    global dir
    if dir == 'Forward':
        print("Changing to Y")
        GPIO.output(8, False) #Green off on 1st side
        GPIO.output(9, True)  #Yellow on on 1st side
        time.sleep(YELLOW_LIGHT_DELAY)

        GPIO.output(9, False)         #Yellow off on 1st side
        GPIO.output(4, True)           #Red on on 1st side
        time.sleep(RED_LIGHT_DELAY)

        GPIO.output(7, False)         # Red off on 2nd side
        GPIO.output(5, True)          #Green on 2nd side
        dir = 'Backward'
        return "changing to Y"
    elif dir == 'Backward':
        print("Changing to X")
        GPIO.output(5, False) #Green off on 1st side
        GPIO.output(6, True)  #Yellow on on 1st side
        time.sleep(YELLOW_LIGHT_DELAY)
   
        GPIO.output(6, False)         #Yellow off on 1st side
        GPIO.output(7, True)           #Red on on 1st side
        time.sleep(RED_LIGHT_DELAY)
   
        GPIO.output(4, False)         # Red off on 2nd side
        GPIO.output(8, True)          #Green on 2nd side
        dir = 'Forward'
        return "changing to X"
    else:
        return "Wrong"


@app.route('/setDirY', methods=['POST'])
def setDirY():
    GPIO.output(8, False) #Green off on 1st side
    GPIO.output(4, True)           #Red on on 1st side
    time.sleep(RED_LIGHT_DELAY)

    GPIO.output(7, False)         # Red off on 2nd side
    GPIO.output(5, True)          #Green on 2nd side
    dir = 'Backward'
    return "Changing to Y"          
        
@app.route('/setDirX', methods=['POST'])
def setDirX():
    GPIO.output(5, False) #Green off on 1st side
    GPIO.output(7, True)           #Red on on 1st side
    time.sleep(RED_LIGHT_DELAY)
   
    GPIO.output(4, False)         # Red off on 2nd side
    GPIO.output(8, True)          #Green on 2nd side
    dir = 'Forward'
    return "Changing to X"
    


@app.route('/getDir', methods=['POST'])
def getDir():
    return dir
  
def setup():
    GPIO.setmode(GPIO.BCM)
    for i in PINS:
        GPIO.setup(i,GPIO.OUT)
    app.run(host='192.168.206.14', port=5000)


try:
    setup()
except KeyboardInterrupt:
    GPIO.cleanup()
    print('cleanup')
    


