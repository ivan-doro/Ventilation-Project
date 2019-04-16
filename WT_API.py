# Wireless Tag humidity and temperature sensors API
 
import requests
import json
from decimal import Decimal
import Configuration as conf
from datetime import datetime
from datetime import timedelta
 
_BASEURL = "https://my.wirelesstag.net"
 
_SIGNIN = _BASEURL + "/ethAccount.asmx/SignIn"
_ISSIGNED = _BASEURL + "/ethAccount.asmx/IsSignedIn"
_GETTAGLIST = _BASEURL + "/ethClient.asmx/GetTagList"
_GETTEMPDATA = _BASEURL + "/ethLogShared.asmx/GetLatestTemperatureRawDataByUUID"
 
_HEADERS = { "content-type": "application/json; charset=utf-8" }
 
roundDecimals = 5
outOfRangeTime = conf.outOfRangeTime
 
class WirelessTagData:
    def getTemperature(uuid):
        data = {"uuid": uuid}
        r = requests.post(_GETTEMPDATA, headers=_HEADERS, data=json.dumps(data))
        parsedResponse = r.json()
        roundedTemp = round(float(parsedResponse["d"]["temp_degC"]), roundDecimals)
        return roundedTemp
 
    def getHumidity(uuid):
        data = {"uuid": uuid}
        r = requests.post(_GETTEMPDATA, headers=_HEADERS, data=json.dumps(data))
        parsedResponse = r.json()
        return parsedResponse["d"]["cap"]
 
    def getBatteryVolt(self, uuid):
        data = {"uuid": uuid}
        r = requests.post(_GETTEMPDATA, headers=_HEADERS, data=json.dumps(data))
        parsedResponse = r.json()
        return parsedResponse["d"]["battery_volts"]
 
    def outOfRange(uuid):
        sensorOutOfRange = False
        data = {"uuid": uuid}
        r = requests.post(_GETTEMPDATA, headers=_HEADERS, data=json.dumps(data))
        parsedResponse = r.json()
        sensorTime = parsedResponse["d"]["time"]
        year = int(sensorTime[:-21])
        month = int(sensorTime[5:-18])
        day = int(sensorTime[8:-15])
        hours = int(sensorTime[11:-12])# + conf.WT_TimeCorrection
        minutes = int(sensorTime[14:-9])
        seconds = int(sensorTime[17:-6])
        time = datetime(year, month, day, hours, minutes, seconds)
        timeCor = timedelta(hours = conf.WT_TimeCorrection)
        time = time + timeCor
        deltaT = datetime.now() - time
        if (deltaT.days != 0 or deltaT.seconds > conf.outOfRangeTime):
            sensorOutOfRange = True
        return sensorOutOfRange
##        return parsedResponse
##print(WirelessTagData.outOfRange("763fa6c3-88ce-43a0-917d-37c144809147"))
##print(datetime.now().time())