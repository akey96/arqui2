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
        self.temperature = None
        self.humidity = None
        self.connectionDB = ConnectionMariaDB()
        self.connectionDB.connect(host=config('host'), user=config('user'), password=config('password'), database=config('database'))
        self.connectionMQTT = ConnectionMQTT()
        self.threadC = Thread(target=self.threadSensor)
        self.threadC.setDaemon(True)
        self.threadC.start()

    def threadSensor(self):

        while True:
            self.humidity, self.temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 18)
            #print(self.humidity, self.temperature)
            self.saveTemperatureAndHumidity()
            self.sendTemperatureAndHumidity()
            sleep(19)

    def saveTemperatureAndHumidity(self):
        self.connectionDB.query("INSERT INTO `data` (`temperature`, `humidity`) VALUES ({}, {})".format(self.temperature, self.humidity))

    def sendTemperatureAndHumidity(self):
        query = self.connectionDB.query("SELECT * FROM `data` ORDER by id desc LIMIT 8")
        objQuery = {'data': query.fetchall()}
        for i in range(len(objQuery['data'])):
            objQuery['data'][i]['date'] = objQuery['data'][i]['date'].strftime('%d-%m-%Y %H:%M:%S')
        objJSON = json.dumps(objQuery, sort_keys=True, indent=4 * ' ')
        self.connectionMQTT.addPublished(config('topic') , objJSON)
