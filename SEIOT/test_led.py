import RPi.GPIO as GPIO 
import time
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(channel, GPIO.OUT)
blink_count = 3

for x in range(blink_count):		
	GPIO.output(channel, GPIO.HIGH)
	time.sleep(1)
	#GPIO.output(channel, GPIO.LOW)
	#time.sleep(1)

GPIO.cleanup()
