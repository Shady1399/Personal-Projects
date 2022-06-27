import numpy as np
import paho.mqtt.client as MQTT
import time
import json

class Publisher:
    def __init__(self, broker, port, topic, clientID):
        self.broker = broker
        self.clientID = clientID
        self.topic = topic
        self.port = port
        self.client = MQTT.Client();
        self.message = ""
        self.client.on_connect = self.onConnect()

    def onConnect(self):
        print("Connected to broker: " + self.broker)

    def start(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, topic, message):
        self.client.publish(topic, json.dumps(message), 2)

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    def encode(self, v, n, u):
        self.message = {
            "bn": self.clientID,
            "e": [{
                "n": n,
                "u": u,
                "t": time.time(),
                "v": v
            }]
        }

if __name__ == "__main__":

    broker = "127.0.0.1"
    port = 1883
    clientID = "/tiot/devices/1234"
    topic = "/tiot/devices/1234"
    device = Publisher(broker, port, topic, clientID)
    device.start()

    while True:
        temp = np.random.uniform(15,30,1)[0]
        device.encode(temp, "temperature", "C")
        device.publish(topic, device.message)
        time.sleep(600)