#!/usr/bin/python3.5
# coding: utf-8

from time import sleep
from threading import Thread
import Adafruit_DHT
from connectionMariaDB import ConnectionMariaDB
from decouple import  config
from connectionMQTT import ConnectionMQTT
import simplejson as json

class SensorDHT11():

    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.connectionDB = ConnectionMariaDB()
        self.connectionDB.connect(host=config('host'), user=config('user'), password=config('password'), database=config('database'))
        self.connectionMQTT = ConnectionMQTT()
        self.threadC = Thread(target=self.threadSensor)
        self.threadC.setDaemon(True)
        self.threadC.start()



    def threadSensor(self):
        #self.sendTemperatureAndHumidity()
        while True:
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 18)
            if (humidity >= self.humidity+1 or humidity <= self.humidity-1 ) and (temperature >= self.temperature+1 or temperature <= self.temperature-1 ):
                #print(self.humidity, self.temperature)
                self.humidity, self.temperature = (humidity, temperature)
                self.saveTemperatureAndHumidity()
                self.sendTemperatureAndHumidity()
            sleep(1)

    def saveTemperatureAndHumidity(self):
        self.connectionDB.query("INSERT INTO `data` (`temperature`, `humidity`) VALUES ({}, {})".format(self.temperature, self.humidity))

    def sendTemperatureAndHumidity(self):
        query = self.connectionDB.query("SELECT * FROM `data` ORDER by id desc LIMIT 20")
        objQuery = {'data': query.fetchall()}
        for i in range(len(objQuery['data'])):
            objQuery['data'][i]['date'] = objQuery['data'][i]['date'].strftime('%d-%m-%Y %H:%M:%S')
        objJSON = json.dumps(objQuery, sort_keys=True, indent=4 * ' ')
        self.connectionMQTT.addPublished(config('topic') , objJSON)
