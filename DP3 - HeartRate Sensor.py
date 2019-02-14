##Temperature Code: Mariam Dawood
##Heartrate / SPO2 w Code: Mithil

import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math
from MPU6050 import MPU6050
from max30100 import MAX30100
from time import sleep
from queue import Queue
from datetime import datetime
import threading


# class temp _user(object):
# def __init__(self,
def run():
    hr = MAX30100()
    count = 0
    while True:
        hr.update()
        #        print("LOOP", count)
        bpm = hr.get_bpm()
        average_bpm = hr.get_avg_bpm()
        spo2 = hr.calculate_spo2()
        if count % 200 == 0:
            out_file = open('HROutput.txt', "a+")
            out_file_spo2 = open('SPO2Output.txt', "a+")
            if bpm != None:
                print(bpm)
            print(average_bpm)
            if average_bpm != None and bpm != None:
                if bpm > (average_bpm + 20) or bpm < (average_bpm - 20):
                    print("Abnormal HeartRate Detected " + "\n" + str(datetime.now()))
            print(spo2)
            if spo2 < 90:
                print("Abnormal SPO2 Levels Detected " + "\n" + str(datetime.now()))
            out_file.close()
            out_file_spo2.close()

        count += 1
        sleep(0.01)


run()
