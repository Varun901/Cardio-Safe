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
import threading

#class temp _user(object):
   # def __init__(self,
def run():
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
            print(temp)
            if len(mean_value) > 20:
                mean_value.remove(mean_value[0])
            sleep(0.1)
        average_temp = sum(mean_value)/len(mean_value)
        print(average_temp) 
        out_file.write(str(average_temp) + "\n")
        if 36.1 <= average_temp <= 37.2:
            time.sleep(10)
                # insert name of function that reads data from sensor
        elif average_temp >= 38:
                # insert code for app alerts
            print("High Temperature! Risk of fever! " + "\n" + str(datetime.now()))
                # insert name of function that reads data from sensor
        else:
                # insert code for app alerts
            print("Low Temperature! Risk of fever! " + "\n" + str(datetime.now()))
                # insert name of function that reads data from sensor
        out_file.close()
run()




