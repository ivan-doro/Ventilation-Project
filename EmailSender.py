# Part responsible for sending E-mails with information
 
import smtplib
import sys
from Support import Support
import Configuration as conf
from datetime import datetime
 
class Send:
    def sendShortMessage(msg):
        header = "To: " + conf.developerEmail + "\n" + "From: " + conf.senderEmail + "\n" + "Subject: " + conf.emailSubject
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(conf.senderEmail, conf.senderPassword)
        server.sendmail(conf.senderEmail, conf.developerEmail, header + "\n\n" + msg)
##        server.sendmail(conf.senderEmail, conf.userDadEmail, header + "\n\n" + msg)
        server.quit()
    def sendStatsReport(cycleCounter, lastSentTime, workingTime, RHum_IN, Temp_IN, AHum_IN, RHum_OUT, Temp_OUT, AHum_OUT, message, ventMessage):
        msg = "Working period - from " + Support.timeCorrection(lastSentTime) + " till "  + Support.timeCorrection(datetime.now()) + " (for " + Support.timeCorrection(datetime.now() - lastSentTime) + " )\n"
        msg = msg +  "During this period fan worked for " + Support.timeCorrection(workingTime) + "\n\n"
        msg = msg + "Inside: \nR. humidity " + str(RHum_IN) + "%" + ",  Temperature " + str(Temp_IN) + ",  A. humidity " + str(AHum_IN) + "\n\n"
        msg = msg + "Outside: \nR. humidity " + str(RHum_OUT) + "%" + ",  Temperature " + str(Temp_OUT) + ",  A. humidity " + str(AHum_OUT) + "\n\n"
        msg = msg + "During the period program has passed " + str(cycleCounter) + " cycles\n\n"
        msg = msg + "Data about sensors errors \n" + message + "\n"
        msg = msg + "Fan operation data \n" + ventMessage
        header = "To: " + conf.developerEmail + "\n" + "From: " + conf.senderEmail + "\n" + "Subject: " + conf.emailSubject
#        print(msg)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(conf.senderEmail, conf.senderPassword)
        server.sendmail(conf.senderEmail, conf.developerEmail, header + "\n\n" + msg)
##        server.sendmail(conf.senderEmail, conf.userDadEmail, msg)
        server.quit()
