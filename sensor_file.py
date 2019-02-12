##Temperature Code: Mariam Dawood
##Heartrate / SPO2 w Code: Mithil

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math
from MPU6050 import MPU6050
from time import sleep
from queue import Queue
from datetime import datetime

#class temp _user(object):
   # def __init__(self,

class TempThread(threading.Thread,client):
    def __init__(self, queue):
        self.q = queue
        self.client = client
        super().__init__()
    def run(self):
        ADC.setup(0x48)
        while True:
            out_file = open('TempOutput.txt', "a+")
            mean_value = []

            for i in range(20):
                analogVal = ADC.read(0)
                Vr = 5 * float(analogVal) / 255
                Rt = 10000 * Vr / (5 - Vr)
                temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
                temp = temp - 273.15
                mean_value.append(temp)
                if len(mean_value) > 20:
                    mean_value.remove(mean_value[0])
                sleep(0.1)
            average_temp = sum(mean_value)/len(mean_value)
            client.publish("Team28/TempValue", average_temp) 
            out_file.write(str(average_temp) + "\n")
            self.q.put_nowait(average_temp)
            if 36.1 <= average_temp <= 37.2:
                time.sleep(10)
                # insert name of function that reads data from sensor
            elif average_temp >= 38:
                # insert code for app alerts
                client.publish("Team28/TempHigh", ("High Temperature! Risk of fever! " + "\n" + str(datetime.now())))
                # insert name of function that reads data from sensor
            else:
                # insert code for app alerts
                client.publish("Team28/TempLow", ("Low Temperature! Risk of fever! " + "\n" + str(datetime.now())))
                # insert name of function that reads data from sensor
            out_file.close()
            with open("TempOutput.txt","r") as temp_file:
                client.publish("Team28/TempOutFile", temp_file.read())

            
class HRThread(threading.Thread,client):
    def __init__(self, queue):
        self.q = queue
        self.client = client
        super().__init__()
    def run(self):
        hr = max30100()
        while True:
            out_file = open('HROutput.txt', "a+")
            hr.update()
            average_bpm = hr.get_avg_bpm()
            value = hr.get_bpm()
            client.publish("Team28/HRValue", value)
            self.q.put_nowait(value)
            if value > average_bpm + 20 or value < average_bpm - 20:
                client.publish("Team28/HRWarning",("Abnormal HeartRate Detected " + "\n" + str(datetime.now())))
            out_file.close()
            with open("HROutput.txt","r") as hr_file:
                client.publish("Team28/HROutFile", hr_file.read())
            out_file = open('SPO2Output.txt', "a+")
            hr.update()
            value = hr.calculate_spo2()
            client.publish("Team28/SPO2Value", value)
            self.q.put_nowait(value)
            if value < 90:
                client.publish("Team28/SPO2Warning",("Abnormal SPO2 Levels Detected " + "\n" + str(datetime.now())))
            out_file.close()
            with open("SPO2Output.txt","r") as spo2_file:
                client.publish("Team28/SPO2OutFile", spo2_file.read())
            sleep(0.5)
'''
a = SoundThread()
b = IMUThread()
a.start()
b.start()
while True: pass
'''
    
    
