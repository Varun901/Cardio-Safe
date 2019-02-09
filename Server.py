import paho.mqtt.client as mqtt
from sensor_file import TempThread, HRThread
from queue import Queue

Client(client_id = "Team20", clean_session = True, userdata = None, protocol = MQTTv311, transport="top")
client = mqtt.Client("Team20")

client.connect("130.113.129.17")

h_queue = Queue()
t_queue = Queue()


if __name__ == "__main__":
    h = HrThread(h_queue, client)
    t = TempThread(t_queue,client)
    h.start()
    t.start()
