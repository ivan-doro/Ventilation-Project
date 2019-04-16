# All the variables, that might be changed by user
 
# Calibration offset values for all senaors, for Temperature and Humidity
calibrationTempOffset_DHT_IN = 0.0
calibrationRHumOffset_DHT_IN = 0.0
calibrationTempOffset_DHT_OUT = 0.0
calibrationRHumOffset_DHT_OUT = 0.0
calibrationTempOffset_WT_IN = 0.0
calibrationRHumOffset_WT_IN = 0.0
calibrationTempOffset_WT_OUT = 0.0
calibrationRHumOffset_WT_OUT = 0.0
 
# Reasonable ranges of sensor values
allowedMaxTemp = 40.0
allowedMinTemp = -35.0
allowedMaxHum = 100.0
allowedMinHum = 0.0
 
# Messages of possible errors in program  
errorsMessages = []
errorsMessages.append("") # Error#0
# Messages of DHT Internal errors
errorsMessages.append("Error#1 Problem getting value from Internal DHT, out of oder.")
errorsMessages.append("Error#2 Internal DHT returns NULL values, out of order.")
errorsMessages.append("Error#3 Internal DHT calibrated temperature, out of normal range, out of order.")
errorsMessages.append("Error#4 Internal DHT calibrated humidity, out of normal range, out of order.")
# Messages of DHT External errors
errorsMessages.append("Error#5 Problem getting value from External DHT, out of oder.")
errorsMessages.append("Error#6 External DHT returns NULL values, out of order.")
errorsMessages.append("Error#7 External DHT calibrated temperature, out of normal range, out of order.")
errorsMessages.append("Error#8 External DHT calibrated humidity, out of normal range, out of order.")
# Messages of WT Internal errors
errorsMessages.append("Error#9 Problem getting value from Internal WT, out of oder.")
errorsMessages.append("Error#10 Internal WT returns NULL values, out of order.")
errorsMessages.append("Error#11 Internal WT calibrated temperature, out of normal range, out of order.")
errorsMessages.append("Error#12 Internal WT calibrated humidity, out of normal range, out of order.")
errorsMessages.append("Error#13 Internal WT values are outdated, out of order.")
errorsMessages.append("Error#14 Problem getting time from Internal WT, out of order.")
# Messages of WT External errors)
errorsMessages.append("Error#15 Problem getting value from External WT, out of oder.")
errorsMessages.append("Error#16 External WT returns NULL values, out of order.")
errorsMessages.append("Error#17 External WT calibrated temperature, out of normal range, out of order.")
errorsMessages.append("Error#18 External WT calibrated humidity, out of normal range, out of order.")
errorsMessages.append("Error#19 External WT values are outdated, out of order.")
errorsMessages.append("Error#20 Problem getting time from External WT, out of order.")
# Messages of errors that make ventilation control impossible
errorsMessages.append("Error#21 Both inside sensors are out of order.")
errorsMessages.append("Error#22 Both outside sensors are out of order.")
#E-mail sending errors
errorsMessages.append("Error#23 Problem with e-mail sending")
errorsMessages.append("Error#24 Problem with critical error e-mail sending")
 
# Wireless Tag sensors uuids
garageInternalUUID = "47d8a2d4-12c1-4b0a-859e-662527b434c0"
saunaExternalUUID = "763fa6c3-88ce-43a0-917d-37c144809147"
 
# Interval of sensor not respondibg that considered as sensor out of range
WT_TimeCorrection = 2 # 2 = 2 hours
outOfRangeTime = 14400 #14400 seconds = 4 hours
 
# Email addresses
emailSubject = "Losevo ventilation robot"
developerEmail = "ivandorofeev@icloud.com"
userDadEmail = "dorofeev.alexander@gmail.com"
senderEmail = "losevo.hills@gmail.com"
senderPassword = "wfL-Aw6-Wrg-kPo"
 
# Period of e-mail sending
emailSendingInterval = 1 # 28800 = 8 hours; 1 = 1 day

# Threshold - difference between internal and external absolute humidity
#  when it makes sence to ventilate
threshold = 1.1
 
# Polling interval
sensorsPollingInterval = 1800 # 1800 = 30 min