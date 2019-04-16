# Main program that controls ventilation
from EmailSender import Send

# Imports from standard packages
import RPi.GPIO as GPIO
import sys
import os
import traceback
import logging
import time
import math
from datetime import datetime

# Path to Adafruit_DHT library (used in DHT22_lib)
sys.path.insert(0, '/home/pi/.local/lib/python3.5/site-packages')

# Imports from my packages
import Configuration as conf
from EmailSender import Send
from WT_API import WirelessTagData
from DHT22_lib import DHT22
from Support import Support
from array import array

# Initiation of GPIO ports numeration
GPIO.setmode(GPIO.BCM)
 
# Pins for directly connected humidity/temperature sensors
DHT22_INSIDE_PIN = 10
DHT22_OUTSIDE_PIN = 9
 
# Pin for the ventilation fan power relay
Vent_PIN = 6
GPIO.setup(Vent_PIN, GPIO.OUT)
 
# Resetting sensors state
workingDHT_IN = True
workingDHT_OUT = True
workingWT_IN = True
workingWT_OUT = True
workingSensorsIN = True
workingSensorsOUT = True
 
# Sensors error counters array
errorsCounters = []
errorsCounters.append(0) # Error#0 (not used for now)
 
# Counters of DHT Internal errors
errorsCounters.append(0) # Error#1 Problem getting value from Internal DHT, out of oder
errorsCounters.append(0) # Error#2 Internal DHT returns NULL values, out of order    
errorsCounters.append(0) # Error#3 Internal DHT calibrated temperature, out of normal range, out of order
errorsCounters.append(0) # Error#4 Internal DHT calibrated humidity, out of normal range, out of order
 
# Counters of DHT External errors
errorsCounters.append(0) # Error#5 Problem getting value from External DHT, out of oder
errorsCounters.append(0) # Error#6 External DHT returns NULL values, out of order
errorsCounters.append(0) # Error#7 External DHT calibrated temperature, out of normal range, out of order
errorsCounters.append(0) # Error#8 External DHT calibrated humidity, out of normal range, out of order
 
# Counters of WT Internal errors
errorsCounters.append(0) # Error#9 Problem contacting Internal WT server, out of oder
errorsCounters.append(0) # Error#10 Internal WT returns NULL values, out of order
errorsCounters.append(0) # Error#11 Internal WT calibrated temperature, out of normal range, out of order
errorsCounters.append(0) # Error#12 Internal WT calibrated humidity, out of normal range, out of order
errorsCounters.append(0) # Error#13 Internal WT values are outdated, out of order
errorsCounters.append(0) # Error#14 Problem getting time from Internal WT, out of order
 
# Counters of WT External errors
errorsCounters.append(0) # Error#15 Problem contacting External WT server, out of oder
errorsCounters.append(0) # Error#16 External WT returns NULL values, out of order
errorsCounters.append(0) # Error#17 External WT calibrated temperature, out of normal range, out of order
errorsCounters.append(0) # Error#18 External WT calibrated humidity, out of normal range, out of order
errorsCounters.append(0) # Error#19 External WT values are outdated, out of order
errorsCounters.append(0) # Error#20 Problem getting time from External WT, out of order

 
# Messages of errors that make ventilation control impossible
errorsCounters.append(0) # Error#21 Both inside sensors are out of order
errorsCounters.append(0) # Error#22 Both outside sensors are out of order

# E-mail sending errors
errorsCounters.append(0) #Error#23 Problem with e-mail sending
errorsCounters.append(0) #Error#24 Problem with critical error e-mail sending
 
# Fan motor state after program start
working = False
 
#?vvv
t= datetime.now() #Temporary
totalWorkingTime = datetime.now() - t
startTime = datetime.now()
#?vvv
lastSentTime = datetime.now()
 
# 10 seconds fan ON test
GPIO.output(Vent_PIN, GPIO.HIGH)
time.sleep(10)
GPIO.output(Vent_PIN, GPIO.LOW)
 
# Sending first e-mail after program start
##try:
Send.sendShortMessage("Ventilation control program started at: " + Support.timeCorrection(datetime.now()))
##except:
##    errorsCounters[23] = errorsCounters[23] + 1

message = ""
ventMessage = ""
cycleCounter = 0
 
# Main cycle
while True:
    try:
        # Data from DHT22 inside sensor and its correctness
        try:
            Temp_DHT_IN = DHT22.getTemp(DHT22_INSIDE_PIN)
            RHum_DHT_IN = DHT22.getHum(DHT22_INSIDE_PIN)
            print(str(Temp_DHT_IN) + " C; " + str(RHum_DHT_IN) + "% - DHT IN")
        except:
            workingDHT_IN = False
            errorsCounters[1] = errorsCounters[1] + 1
        if (workingDHT_IN and (Temp_DHT_IN is None or RHum_DHT_IN is None)):
            workingDHT_IN = False
            errorsCounters[2] = errorsCounters[2] + 1
        elif (workingDHT_IN):
            Temp_DHT_IN = Temp_DHT_IN + conf.calibrationTempOffset_DHT_IN              
            RHum_DHT_IN = RHum_DHT_IN + conf.calibrationRHumOffset_DHT_IN
        if (workingDHT_IN and (Temp_DHT_IN > conf.allowedMaxTemp or Temp_DHT_IN < conf.allowedMinTemp)):
            workingDHT_IN = False
            errorsCounters[3] = errorsCounters[3] + 1
        if (workingDHT_IN and (RHum_DHT_IN > conf.allowedMaxHum or RHum_DHT_IN < conf.allowedMinHum)):
            workingDHT_IN = False
            errorsCounters[4] = errorsCounters[4] + 1
           
        # Data from DHT22 outside sensor and its correctness
        try:
            Temp_DHT_OUT = DHT22.getTemp(DHT22_OUTSIDE_PIN)          
            RHum_DHT_OUT = DHT22.getHum(DHT22_OUTSIDE_PIN)
            print(str(Temp_DHT_OUT)+ " C; " + str(RHum_DNT_OUT))
        except:
            workingDHT_OUT = False
            errorsCounters[5] = errorsCounters[5] + 1
        if (workingDHT_OUT and (Temp_DHT_OUT is None or RHum_DHT_OUT is None)):
            workingDHT_OUT = False
            errorsCounters[6] = errorsCounters[6] + 1
        elif (workingDHT_OUT):
            Temp_DHT_OUT = Temp_DHT_OUT + conf.calibrationTempOffset_DHT_OUT              
            RHum_DHT_OUT = RHum_DHT_OUT + conf.calibrationRHumOffset_DHT_OUT
        if (workingDHT_OUT and (Temp_DHT_OUT > conf.allowedMaxTemp or Temp_DHT_OUT < conf.allowedMinTemp)):
            workingDHT_OUT = False
            errorsCounters[7] = errorsCounters[7] + 1
        if (workingDHT_OUT and (RHum_DHT_OUT > conf.allowedMaxHum or RHum_DHT_OUT < conf.allowedMinHum)):
            workingDHT_OUT = False
            errorsCounters[8] = errorsCounters[8] + 1
            
        # Data from WirelessTag inside sensor and its correctness
        try:
            Temp_WT_IN = WirelessTagData.getTemperature(conf.garageInternalUUID)
            RHum_WT_IN = WirelessTagData.getHumidity(conf.garageInternalUUID)
            print(str(Temp_WT_IN) + " C; " + str(RHum_WT_IN) + "% - WT IN")
        except:
            workingWT_IN = False
            errorsCounters[9] = errorsCounters[9] + 1
        
        if (workingWT_IN and (Temp_WT_IN is None or RHum_WT_IN is None)):
            workingWT_IN = False
            errorsCounters[10] = errorsCounters[10] + 1
        elif (workingWT_IN):
            Temp_WT_IN = Temp_WT_IN + conf.calibrationTempOffset_WT_IN
            RHum_WT_IN = RHum_WT_IN + conf.calibrationRHumOffset_WT_IN
        if (workingWT_IN and (Temp_WT_IN > conf.allowedMaxTemp or Temp_WT_IN < conf.allowedMinTemp)):
            workingWT_IN = False
            errorsCounters[11] = errorsCounters[11] + 1
        if (workingWT_IN and (RHum_WT_IN > conf.allowedMaxHum or RHum_WT_IN < conf.allowedMinHum)):
            workingWT_IN = False
            errorsCounters[12] = errorsCounters[12] + 1
        try:
            if (workingWT_IN and WirelessTagData.outOfRange(conf.garageInternalUUID)):
                workingWT_IN = False
                errorsCounters[13] = errorsCounters[13] + 1
        except:
            workingWT_IN = False
            errorsCounters[14] = errorsCounters[14] + 1
       
           
        # Data from WirelessTag outside sensor and its correctness
        try:
            Temp_WT_OUT = WirelessTagData.getTemperature(conf.saunaExternalUUID)
            RHum_WT_OUT = WirelessTagData.getHumidity(conf.saunaExternalUUID)
            print(str(Temp_WT_OUT)+ " C " + str(RHum_WT_OUT) + "% - WT OUT")
        except:
            workingWT_OUT = False            
            errorsCounters[15] = errorsCounters[15] + 1
        if (workingWT_OUT and (Temp_WT_OUT is None or RHum_WT_OUT is None)):
            workingWT_OUT = False
            errorsCounters[16] = errorsCounters[16] + 1
        elif (workingWT_OUT):
            Temp_WT_OUT = Temp_WT_OUT + conf.calibrationTempOffset_WT_OUT
            RHum_WT_OUT = RHum_WT_OUT + conf.calibrationRHumOffset_WT_OUT
        if(workingWT_OUT and (Temp_WT_OUT > conf.allowedMaxTemp or Temp_WT_OUT < conf.allowedMinTemp)):
            workingWT_OUT = False
            errorsCounters[17] = errorsCounters[17] + 1
        if (workingWT_OUT and (RHum_WT_OUT > conf.allowedMaxHum or RHum_WT_OUT < conf.allowedMinHum)):
            workingWT_OUT = False
            errorsCounters[18] = errorsCounters[18] + 1
##        try:
        if (workingWT_OUT and WirelessTagData.outOfRange(conf.saunaExternalUUID)):
            workingWT_OUT = False
            errorsCounters[19] = errorsCounters[19] + 1
##        except:
##            workingWT_OUT = False
##            errorsCounters[20] = errorsCounters[20] + 1
   
        # Defining internal sensors average data
        if ((workingDHT_IN == False and workingWT_IN == False)):
            errorsCounters[21] = errorsCounters[21] + 1
            GPIO.output(Vent_PIN, GPIO.LOW)
            workingSensorsIN = False
            RHum_IN = "Impossible to define"
            Temp_IN = "Impossible to define"
            AHum_IN = "Impossible to define"
        elif (workingDHT_IN == False):
            Temp_IN = round(Temp_WT_IN, 2)
            RHum_IN = round(RHum_WT_IN, 2)
        elif (workingWT_IN == False):
            Temp_IN = round(Temp_DHT_IN, 2)
            RHum_IN = round(RHum_DHT_IN, 2)
        else:
            Temp_IN = round((Temp_DHT_IN + Temp_WT_IN)/2, 2)
            RHum_IN = round((RHum_DHT_IN + RHum_WT_IN)/2, 2)
        # Defining external sensors average data    
        if (workingDHT_OUT == False and workingWT_OUT == False):
            errorsCounters[22] = errorsCounters[22] + 1
            GPIO.output(Vent_PIN, GPIO.LOW)
            workingSensorsOUT = False
            RHum_OUT = "Impossible to define"
            Temp_OUT = "Impossible to define"
            AHum_OUT = "Impossible to define"
        elif (workingDHT_OUT == False):
            Temp_OUT = round(Temp_WT_OUT, 2)
            RHum_OUT = round(RHum_WT_OUT, 2)
        elif (workingWT_OUT == False):
            Temp_OUT = round(Temp_DHT_OUT, 2)
            RHum_OUT = round(RHum_DHT_OUT, 2)
        else:
            Temp_OUT = round((Temp_DHT_OUT + Temp_WT_OUT)/2, 2)
            RHum_OUT = round((RHum_DHT_OUT + RHum_WT_OUT)/2, 2)
 
        # Calculating absolute humidity internal and external
        if (workingSensorsIN):
            AHum_IN = Support.getAHum(Temp_IN, RHum_IN)
        if (workingSensorsOUT):
            AHum_OUT = Support.getAHum(Temp_OUT, RHum_OUT)
       
        message = Support.messageFormation(errorsCounters)
 
        # Ventilation decision
        if (workingSensorsIN and workingSensorsOUT and AHum_IN/AHum_OUT > conf.threshold):
            #Turning ON
            if (working == False):
                GPIO.output(Vent_PIN, GPIO.HIGH)
                working = True
                startTime = datetime.now()
                ventMessage = ventMessage + "Ventilation turning ON at " + Support.timeCorrection(datetime.now()) + ", with absolute humidity inside " + str(AHum_IN) + " and absolute humidity outside " + str(AHum_OUT) + "\n"
 
        else:
            # Turning OFF
            if (working):
                GPIO.output(Vent_PIN, GPIO.LOW)
                working = False
                workingT = datetime.now() - startTime
                ventMessage = ventMessage + "Ventilation turning OFF at " + Support.timeCorrection(datetime.now()) + ", after " + Support.timeCorrection(workingT) + " of working, with absolute humidity inside " + str(AHum_IN) + " and absolute humidity outside " + str(AHum_OUT) + "\n"
                totalWorkingTime = totalWorkingTime + workingT
        
        if (ventMessage == ""):
            ventMessage = "Fan did not change working mode during the period"
        cycleCounter = cycleCounter + 1 # Ventilation control of this cycle finished
        print(cycleCounter)
##        print(errorsCounters)
        # Time to send e-mail with report?
        timeFromLastEmail = datetime.now() - lastSentTime
        if (timeFromLastEmail.days >= conf.emailSendingInterval):
            if (working == True):
                totalWorkingTime = totalWorkingTime + datetime.now() - startTime
                startTime = datetime.now()
            try:
                Send.sendStatsReport(cycleCounter, lastSentTime, totalWorkingTime, RHum_IN, Temp_IN, AHum_IN, RHum_OUT, Temp_OUT, AHum_OUT, message, ventMessage)
            
                # reset of all counters
                message = ""
                ventMessage = ""
                t = datetime.now()
                totalWorkingTime = datetime.now() - t
                lastSentTime = datetime.now()
                cycleCounter = 0
                for i in range(0, len(errorsCounters)):
                    errorsCounters[i] = 0
            except:
                errorsCounters[23] = errorsCounters[23] + 1
        workingDHT_IN = True
        workingDHT_OUT = True
        workingWT_IN = True
        workingWT_OUT = True
        workingSensorsIN = True
        workingSensorsOUT = True
        
        time.sleep(conf.sensorsPollingInterval)
 
## WHEN DEBUGGING
## v
    except KeyboardInterrupt:
        print("Turning off")
        GPIO.output(Vent_PIN, GPIO.LOW)
        GPIO.cleanup()
## ^  
##    except Exception as e:
##        print(e)
##        logging.error(traceback.format_exc())
##        print (e.__doc__)
##        try:
##            Send.sendShortMessage("FATAL ERROR " + str(e) + "\n" + str(e.__doc__) + "\nRebooting Raspberry")
##        except:
##            errorsCounters[24] = errorsCounters[24] + 1
##        GPIO.output(Vent_PIN, GPIO.LOW)
##        GPIO.cleanup()
##        time.sleep(100)
##        print("reboot")
##        #os.system("sudo reboot")
##        break
