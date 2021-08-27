# Dynamical Fan Controller Script
# Created by sMetase
# 8/27/2021

# Define the channel used by GPIO
Gpchannel = 40
# Set up the fan's turn-on temperature
Temp_threshold = 50.0
#Fan status
Fanopen = False
#Interval
Interval = (0, 5, 0)
#Log
filename = "log.txt"

# Import necessary lib
import time
import atexit
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Failed to import RPi.GPIO. This is probably because you need to run it under superuser privileges.")



def cpu_temp():
    "Read cpu temperature"
    with open("/sys/class/thermal/thermal_zone0/temp", 'r') as f:
        return float(f.read())/1000


def gpio_setup():
    "Set up GPIO"
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Gpchannel, GPIO.OUT, initial=GPIO.LOW)


def log(temp,c):
    "Log"
    with open(filename, 'a') as log:
        log.write(time.ctime() + " " + str(temp) + "C" + " " + c + "\n")
        log.close()


def clean():
    "Free resources"
    GPIO.cleanup()
    print("Goodbye, My little star!")


def main():
    "Dynamically switch the fan"
    gpio_setup()
    while(True):
        temp = cpu_temp()

        if temp > Temp_threshold:
            log(temp,"Open the fan")
            GPIO.output(Gpchannel, GPIO.HIGH)
            Fanopen = True
        else:
            log(temp, "Close the fan")
            GPIO.output(Gpchannel, GPIO.LOW)
            Fanopen = False
        
        time.sleep(Interval[0]*3600+Interval[1]*60+Interval[2])
        

main()
atexit(clean())