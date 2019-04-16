# DHT22, directly connected humidity and temperature sensors, library
 
import sys
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
class DHT22:
    def getTemp(pin):
        #t =358
        Rh,t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
        return(t)
   
    def getHum(pin):
        #Rh = 345
        Rh,t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, pin)
        return(Rh)
   
   
#print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t, Rh))
