##Temperature Code: Mariam Dawood
##Heartrate / SPO2 w Code: Mithil
## Buzzer and LED: Gurleen
## App / MQTT Client : Varun Jain

# All Appropriate Libraries and classes have been imported

import PCF8591 as ADC
import threading
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from gpiozero import LED
import time
import math
from max30100 import MAX30100
from time import sleep
from queue import Queue
import paho.mqtt.client as mqtt
from datetime import datetime
from twilio.rest import Client

#class temp _user(object):
   # def __init__(self,

account_sid = 'INSERT ACCOUNT SID HERE'
auth_token = 'INSERT AUTH TOKEN HERE'
# Insert phone number here for text messages when warning is detected
phone_number = "+INSERT PHONE NUMBER HERE"
twilio_client = Client(account_sid, auth_token)

# This class reads and calculates temperature values from the Thermistor
class TempThread(threading.Thread):
    def __init__(self, queue, mutex, client):
        self.q = queue
        self.client = client
        # Mutex is used in order to have the program thread access the sensors simultaneously without delay
        self.mutex = mutex
        super().__init__()
    def run(self):
        self.mutex.acquire()
        # ADC is setup so that digital values can be read from the Thermistor
        ADC.setup(0x48)
        self.mutex.release()
        # Buzzer is set at GPIO pin 17
        buzz = Buzzer(17)
        # LED is set at GPIO pin 19
        led = LED(19)
        # LED is on to signal that the device is on and working
        led.on()
        while True:
            # A file is created and opened with the name TempOutput.txt
            out_file = open('TempOutput.txt', "a+")
            # A blank list is created called mean_value to hold the mean temperature value
            mean_value = []

            for i in range(20):
                self.mutex.acquire()
                # The Analog Value is read from the ADC
                analogVal = ADC.read(0)
                self.mutex.release()
                # The following calculations convert the analog value to temperature in degrees celsius as seen from Sunfounder
                Vr = 5 * float(analogVal) / 255
                Rt = 10000 * Vr / (5 - Vr)
                temp = 1 / (((math.log(Rt / 10000)) / 3950) + (1 / (273.15 + 25)))
                temp = temp - 273.15
                # The temp value is added on to the mean_value list
                mean_value.append(temp)
                # The following commands allow for a rolling list to ensure that a consistent average is always calculated
                if len(mean_value) > 20:
                    mean_value.remove(mean_value[0])
                sleep(0.1)
            # The average_temp variable calculates the average temperature as per the mean_value list
            average_temp = sum(mean_value)/len(mean_value)
            # The average temperature is published to the Team 28 Temp Value Topic on the MQTT Server
            self.client.publish("Team28/TempValue", average_temp)
            # The average temperature is also written to the outfile
            out_file.write(str(average_temp) + "\n")
            # Queue prevents delay in running the threads
            self.q.put_nowait(average_temp)
            # The following are if statements to classify whether or not a certain reading induces a warning
            if 36.1 <= average_temp <= 38:
                # This makes sure the buzz is off when the temperature is in the optimal range
                buzz.off()
                # A blank string is published to the Team 28 Temp Warning Topic on the MQTT Server
                self.client.publish("Team28/TempWarning", (""))
                time.sleep(10)
            elif average_temp > 38:
                # The following commands are to determine whether a warning is already in place and if so to continue the buzzer
                if buzz.is_active == False:
                    buzz.on()
                # A High Temp Warning is published to the Team 28 Temp Warning Topic on the MQTT Server
                self.client.publish("Team28/TempWarning", ("High Temperature! Risk of fever! " + "\n" + str(datetime.now())))
                # A warning will be sent to the phone number below via Twilio
                message = twilio_client.messages \
                    .create(
                        body='High Temperature WARNING',
                        from_='+15878020288',
                        to=phone_number
                    )
                print(message.sid)
                # insert name of function that reads data from sensor
            else:
                # The following commands are to determine whether a warning is already in place and if so to continue the buzzer
                if buzz.is_active == False:
                    buzz.on()
                # A Low Temp Warning is published to the Team 28 Temp Warning Topic on the MQTT Server
                self.client.publish("Team28/TempWarning", ("Low Temperature! Risk of fever! " + "\n" + str(datetime.now())))
                # A warning will be sent to the phone number below via Twilio
                message = twilio_client.messages \
                    .create(
                        body='Low Temperature WARNING',
                        from_='+15878020288',
                        to=phone_number
                    )
                print(message.sid)
                # The next line closes the outfile
            out_file.close()
            # The following lines open the TempOutput file and publishes it to the MQTT Server via the Team 28 TempOutFile Topic
            with open("TempOutput.txt", "r") as temp_file:
                self.client.publish("Team28/TempOutFile", temp_file.read())

# This class reads and calculates the SPO2 and Heart Rate values from the MAX30100 sensor
class HRThread(threading.Thread):
    def __init__(self, queue, mutex, client):
        self.q = queue
        self.client = client
        # Mutex is used in order to have the program thread access the sensors simultaneously without delay
        self.mutex = mutex
        super().__init__()
    def run(self):
        self.mutex.acquire()
        # The variable hr is assigned to the MAX30100 class
        hr = MAX30100()
        self.mutex.release()
        # Buzzer is set at GPIO pin 25
        buzz = Buzzer(25)
        # Count is to ensure that the HR values do not constantly publish to the app as this may cause the program to crash
        count = 0
        while True:
            self.mutex.acquire()
            # Updates the hr values from the sensors to display updated results
            hr.update()
            self.mutex.release()
            # Obtains the current bpm of the user
            bpm = hr.get_bpm()
            # Obtains the average bpm of the user over the course of 0.1 seconds
            average_bpm = hr.get_avg_bpm()
            # Calculates the SPO2 of the user
            spo2 = hr.calculate_spo2()
            # Every 200 values, the values are displayed and sent to the outfille
            if count % 200 == 0:
                # Out files for SPO2 and HR are opened
                out_file_hr = open('HROutput.txt', "a+")
                out_file_spo2 = open('SPO2Output.txt', "a+")
                # If the bpm is a proper value then it will publish to the MQTT server via the Team 28 HR Value Topic
                if bpm != None:
                    self.client.publish("Team28/HRValue", bpm)                
                    self.q.put_nowait(bpm)
                    # The bpm will also be written in the outfile
                    out_file_hr.write(str(bpm) + "\n")
                # If the Average bpm and the bpm are equal to a proper value then the following code will be executed
                if average_bpm != None and bpm!= None:
                    # if the bpm is at a certain threshold away from the average, a warning is triggered
                    if bpm > (average_bpm + 20) or bpm < (average_bpm - 20):
                        # A warning is published to the Team 28 HR Warning Topic via the MQTT Server
                        self.client.publish("Team28/HRWarning",("Abnormal HeartRate Detected " + "\n" + str(datetime.now())))
                        # A warning will be sent to the phone number below via Twilio
                        message = twilio_client.messages \
                            .create(
                                body='Heart Rate WARNING',
                                from_='+15878020288',
                                to=phone_number
                            )
                        print(message.sid)
                        # The following code is to ensure that if the buzzer is already on,it stay on and if off it turns on
                        if buzz.is_active == False:
                            buzz.on()
                    else:
                        buzz.off()
                        # A blank string is published and displayed to the user via the HRWarning Topic sent to the MQTT Server
                        self.client.publish("Team28/HRWarning",(""))
                # The spo2 value is published and displayed to the user via the SPO2 value Topic sent to the MQTT server
                self.client.publish("Team28/SPO2Value", spo2)
                self.q.put_nowait(spo2)
                # The SPO2 value is the written to the outfile
                out_file_spo2.write(str(spo2) + "\n")
                # If the SPO2 value is less than 90 then a warning will be excuted
                if spo2 < 90:
                    # A warning is published to the Team 28 SPO2 Warning Topic via the MQTT Server
                    self.client.publish("Team28/SPO2Warning",("Abnormal SPO2 Levels Detected " + "\n" + str(datetime.now())))
                    # A warning will be sent to the phone number below via Twilio
                    message = twilio_client.messages \
                        .create(
                            body='SPO2 WARNING',
                            from_='+15878020288',
                            to=phone_number
                        )
                    print(message.sid)
                    # The following code is to ensure that if the buzzer is already on,it stay on and if off it turns on
                    if buzz.is_active == False:
                        buzz.on()
                else:
                    # A blank string is published and displayed to the user via the SPO2Warning Topic sent to the MQTT Server
                    self.client.publish("Team28/SPO2Warning",(""))
                    buzz.off()
                # Out files are closed
                out_file_hr.close()
                out_file_spo2.close()
                # The following lines open the HROutput and SPO2Output file and publishes it to the MQTT Server via the Team 28 Topics
                with open("HROutput.txt", "r") as hr_file:
                    self.client.publish("Team28/HROutFile", hr_file.read())
                with open("SPO2Output.txt", "r") as spo2_file:
                    self.client.publish("Team28/SPO2OutFile", spo2_file.read())
            # Count is added by 1 as 1 process has been completed
            count += 1
            sleep(0.01)
'''
a = SoundThread()
b = IMUThread()
a.start()
b.start()
while True: pass
'''
    
