# All Appropriate Libraries and classes have been imported

import paho.mqtt.client as mqtt
from sensor_file import TempThread, HRThread
from queue import Queue
from threading import Lock

# The Mqtt client id Team 28 is defined as client
client = mqtt.Client("Team28")

# Client connects to the below IP address
client.connect("130.113.129.17")

# Queue is enabled to make sure that both threads can run simultaneously and the mutex commands prevents any possible delays and promotes sharing of vales
h_queue = Queue()
t_queue = Queue()
mutex = Lock()

# HRThread and TempThread are both prompted to start
if __name__ == "__main__":
    h = HRThread(h_queue, mutex, client)
    t = TempThread(t_queue, mutex, client)
    h.start()
    t.start()
