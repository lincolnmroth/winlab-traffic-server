import time
import RPi.GPIO as GPIO
import atexit
from flask import Flask, request
import urllib.request, json

app = Flask(__name__)

PINS = { 8, 9, 4, 5, 6, 7}#Follows Green, Yellow, Red Pattern (First 3 are for 0 and the other are for 1)
GREEN_LIGHT_DELAY = 5
YELLOW_LIGHT_DELAY = 2
RED_LIGHT_DELAY = 1
dir = 'Forward'
print("Hello")
state = 'on'

@app.route('/')
def test():
    return 'hello'
           
@app.route('/changeDir', methods=['POST'])
def change_dir():
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
    else:
        print("Wrong")

@app.route('/setDir', methods=['POST'])
def setDir():
    direction = request.headers.get('direction')
    if direction == 'Forward':
        print("Changing to X")
        GPIO.output(5, False) #Green off on 1st side
        GPIO.output(7, True)           #Red on on 1st side
        time.sleep(RED_LIGHT_DELAY)
   
        GPIO.output(4, False)         # Red off on 2nd side
        GPIO.output(8, True)          #Green on 2nd side
        dir = 'Forward'
    elif direction == 'Backward':
        print("Changing to Y")
        GPIO.output(8, False) #Green off on 1st side
        GPIO.output(4, True)           #Red on on 1st side
        time.sleep(RED_LIGHT_DELAY)

        GPIO.output(7, False)         # Red off on 2nd side
        GPIO.output(5, True)          #Green on 2nd side
        dir = 'Backward'
    else:
        return 'Not a vaild input, put direction (either Forward or Backward) in the request header under variable direction'

@app.route('/getDir', methods=['POST'])
def getDir():
    return Dir
def setup():
    GPIO.setmode(GPIO.BCM)
    for i in PINS:
        GPIO.setup(i,GPIO.OUT)
    app.run(host='192.168.206.14')


try:
    setup()

except KeyboardInterrupt:
    GPIO.cleanup()
    print('cleanup')
    

