# All the support function the VentillationController programm may need
import Configuration as conf
class Support:
    #Absolute Humidity calculation
    def getAHum (temp, RHum):
        Pow = pow(2.71828, 17.67*temp/(temp+234.5))
        AHum = (6.112*Pow*RHum*2.1674)/(temp+273.15)
        AHum = round(AHum, 2)
        return(AHum)
 
    def messageFormation (errorsCounters):
        message = ""
        for i in range (0, len(errorsCounters)):
            if(errorsCounters[i] != 0):
                message = message + conf.errorsMessages[i] + "  Error occured " + str(errorsCounters[i]) + " times\n"
        if(message == ""):
            message = "During the period all sensors functioned correctly"
        return message        
   
    def timeCorrection (time):
        time = str(time)
        time2 = ""
        for i in range (0, len(time)):
            if (i < len(time) - 7):
                time2 = time2 + time[i]
        return time2