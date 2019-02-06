class HRThread(threading.Thread):
    def __init__(self, queue):
        self.q = queue
        super().__init__()
    def run(self):
        hr = max30100()
        while True:
            out_file = open('HROutput.txt', "a+")
            hr.update()
            average_bpm = hr.get_avg_bpm()
            value = hr.get_bpm()
            out_file.write(str(value) + "\n")
            self.q.put_nowait(value)
            if value > average_bpm + 20 or value < average_bpm - 20:
                print("Abnormal HeartRate Detected")
                out_file.write("Abnormal HeartRate Detected ")
                out_file.write(str(datetime.now()))
                out_file.write("\n")
            out_file.close()
            out_file = open('SPO2Output.txt', "a+")
            hr.update()
            value = hr.calculate_spo2()
            out_file.write(str(value) + "\n")
            self.q.put_nowait(value)
            if value < 90:
                print("Abnormal SPO2 Levels Detected")
                out_file.write("Abnormal SPO2 levels Detected ")
                out_file.write(str(datetime.now()))
                out_file.write("\n")
            out_file.close()
            sleep(0.5)
'''
a = SoundThread()
b = IMUThread()
a.start()
b.start()
while True: pass