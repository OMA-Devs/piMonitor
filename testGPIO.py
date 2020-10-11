#!/usr/bin/env python3

#Logging Python
#import logging
from time import sleep
#Control GPIO
import RPi.GPIO as gpio
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

## yellow
gpio.setup(23, gpio.OUT)
gpio.output(23, 1)

## green
gpio.setup(12, gpio.OUT)
pwm = gpio.PWM(12, 100) #100 es la frecuencia en HERTZIOS
pwm.start(0)
for i in range(100):
	pwm.ChangeDutyCycle(i)
	sleep(0.1)

gpio.cleanup()