##Temperature Code: Mariam Dawood
##Heartrate / SPO2 w Code: Mithil

import PCF8591 as ADC
import threading
import RPi.GPIO as GPIO
from gpiozero import Buzzer
import time
import math
from max30100 import MAX30100
from time import sleep
from queue import Queue
import paho.mqtt.client as mqtt
from datetime import datetime

#class temp _user(object):
   # def __init__(self,

class TempThread(threading.Thread):
    def __init__(self, queue, mutex, client):
        self.q = queue
        self.client = client
        self.mutex = mutex
        super().__init__()
    def run(self):
        self.mutex.acquire()
        ADC.setup(0x48)
        self.mutex.release()
        buzz = Buzzer(17)
        while True:
            out_file = open('TempOutput.txt', "a+")
            mean_value = []

            for i in range(20):
                self.mutex.acquire()
                analogVal = ADC.read(0)
                self.mutex.release()
                Vr = 5 * float(analogVal) / 255
                Rt = 10000 * Vr / (5 - Vr)
                temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
                temp = temp - 273.15
                mean_value.append(temp)
                if len(mean_value) > 20:
                    mean_value.remove(mean_value[0])
                sleep(0.1)
            average_temp = sum(mean_value)/len(mean_value)
            self.client.publish("Team28/TempValue", average_temp)
            out_file.write(str(average_temp) + "\n")
            self.q.put_nowait(average_temp)
            if 36.1 <= average_temp <= 38:
                buzz.off()
                self.client.publish("Team28/TempWarning", (""))
                time.sleep(10)
                # insert name of function that reads data from sensor
            elif average_temp > 38:
                if buzz.is_active == False:
                    buzz.on()
                # insert code for app alerts
                self.client.publish("Team28/TempWarning", ("High Temperature! Risk of fever! " + "\n" + str(datetime.now())))
                # insert name of function that reads data from sensor
            else:
                if buzz.is_active == False:
                    buzz.on()
                # insert code for app alerts
                self.client.publish("Team28/TempWarning", ("Low Temperature! Risk of fever! " + "\n" + str(datetime.now())))
                # insert name of function that reads data from sensor
            out_file.close()
            with open("TempOutput.txt", "r") as temp_file:
                self.client.publish("Team28/TempOutFile", temp_file.read())

            
class HRThread(threading.Thread):
    def __init__(self, queue, mutex, client):
        self.q = queue
        self.client = client
        self.mutex = mutex
        super().__init__()
    def run(self):
        self.mutex.acquire()
        hr = MAX30100()
        self.mutex.release()
        buzz = Buzzer(18)
        count = 0
        while True:
            self.mutex.acquire()
            hr.update()
            self.mutex.release()
            bpm = hr.get_bpm()
            average_bpm = hr.get_avg_bpm()
            spo2 = hr.calculate_spo2()
            if count % 200 == 0:
                out_file_hr = open('HROutput.txt', "a+")
                out_file_spo2 = open('SPO2Output.txt', "a+")
                if bpm != None:
                    self.client.publish("Team28/HRValue", bpm)
                    print(bpm)
                    self.q.put_nowait(bpm)
                    out_file_hr.write(str(bpm) + "\n")
                if average_bpm != None and bpm!= None:
                    if bpm > (average_bpm + 20) or bpm < (average_bpm - 20):
                        self.client.publish("Team28/HRWarning",("Abnormal HeartRate Detected " + "\n" + str(datetime.now())))
                        if buzz.is_active == False:
                            buzz.on()
                    else:
                        buzz.off()
                        self.client.publish("Team28/HRWarning",(""))
                self.client.publish("Team28/SPO2Value", spo2)
                self.q.put_nowait(spo2)
                out_file_spo2.write(str(spo2) + "\n")
                if spo2 < 90:
                    self.client.publish("Team28/SPO2Warning",("Abnormal SPO2 Levels Detected " + "\n" + str(datetime.now())))
                    if buzz.is_active == False:
                        buzz.on()
                else:
                    self.client.publish("Team28/SPO2Warning",(""))
                    buzz.off()
                out_file_hr.close()
                out_file_spo2.close()
                with open("HROutput.txt", "r") as hr_file:
                    self.client.publish("Team28/HROutFile", hr_file.read())
                with open("SPO2Output.txt", "r") as spo2_file:
                    self.client.publish("Team28/SPO2OutFile", spo2_file.read())
            count += 1
            sleep(0.01)
'''
a = SoundThread()
b = IMUThread()
a.start()
b.start()
while True: pass
'''
    
    
