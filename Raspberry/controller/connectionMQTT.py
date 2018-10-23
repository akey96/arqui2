#!/usr/bin/python3.5
# coding: utf-8

import paho.mqtt.client as mqtt
from decouple import config

class ConnectionMQTT():

    def __init__(self):
        self.callbacks = {}
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_publish = self.__on_publish
        self.client.on_subscribe = self.__on_subscribe
        self.client.connect(config('hostMQTT'), 1883, 60)
        self.client.loop_start()


    def __on_connect(self, client, userdata, flags, rc):

        if not rc :
            print('Connection successful', userdata, flags)
        else :
            print('error en la conecction')


    def __on_publish(self, client, userdata, mid):
        print("mid: " + str(mid), userdata)

    def __on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))


    def addSubscribe(self, topic, callback):

        self.callbacks[topic] = callback
        self.client.subscribe(topic, 0)


    def addPublished(self, topic, message):
        infot = self.client.publish(topic, message, qos=2)
        infot.wait_for_publish()
