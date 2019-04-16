import RPi.GPIO as GPIO
import time
from datetime import datetime
import smtplib

##str = "dghdyrhjhjr:fhdhh:zxdfhgxgh"
##str = str.replace(":", '-')
##print(str)

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

try:
    while True:
        GPIO.output(6, GPIO.HIGH)
        time.sleep(3)
        #GPIO.output(6, GPIO.LOW)
        time.sleep(3)
        
        
except KeyboardInterrupt:
    print("Turning off")
    GPIO.cleanup()