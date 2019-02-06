##Temperature Code: Mariam Dawood 

import PCF8591 as ADC
import RPi.GPI0 as GPI0
import time
import math
from MPU650 import MPU6050
from time import sleep
from queue import Queue #do we need this? 
from datetime import datetime

#class temp _user(object):
   # def __init__(self,

class TempThread(threading.Thread):
    def __init__(self, queue):
        self.q = queue
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
                sleep(0.1)
            mean = sum(mean_value)/len(mean_value)
            out_file.write(str(mean) + "\n")
            self.q.put_nowait(mean)
            if 36.1 <= average_temp <= 37.2:
                time.sleep(10)
                # insert name of function that reads data from sensor
            elif average_temp >= 38:
                # insert code for app alerts
                print("High Temperature! Risk of fever!")
                out_file.write("High Temperature! Risk of fever!")
                out_file.write(str(datetime.now()))
                out_file.write("\n")
                # insert name of function that reads data from sensor
                else:
                # insert code for app alerts
                print("Low Temperature! Risk of fever!")
                out_file.write("Low Temperature! Risk of fever!")
                out_file.write(str(datetime.now()))
                out_file.write("\n")
                # insert name of function that reads data from sensor
            out_file.close()
            
#no idea how to do wifi part
    
    
    
