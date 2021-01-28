import RPi.GPIO as GPIO  
import time  

led_pin = 12
GPIO.setmode(GPIO.BCM) 
GPIO.setup(led_pin, GPIO.OUT)

pwm = GPIO.PWM(led_pin, 50) #50hz  
pwm.start(100) 

while True: 
    end_key = raw_input(" - Stop to Blink LED, Please enter the 'end' : ") 
    if end_key == "end": 
        break 
    
GPIO.cleanup()
