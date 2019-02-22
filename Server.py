import paho.mqtt.client as mqtt
from sensor_file import TempThread, HRThread
from queue import Queue
from threading import Lock

client = mqtt.Client("Team28")

client.connect("130.113.129.17")

h_queue = Queue()
t_queue = Queue()
mutex = Lock()

if __name__ == "__main__":
    h = HRThread(h_queue, mutex, client)
    t = TempThread(t_queue, mutex, client)
    h.start()
    t.start()
