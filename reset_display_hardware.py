from ctypes import *
import os
import time
file_dir = os.path.dirname(os.path.realpath(__file__))

gpio = CDLL(os.path.join(file_dir,"SC16IS752GPIO.so"))


def REST_Hardware():
	gpio.SC16IS752GPIO_Init()
	gpio.SC16IS752GPIO_Mode(0,1)
	gpio.SC16IS752GPIO_Write(0,0)
	time.sleep(1)
	gpio.SC16IS752GPIO_Write(0,1)
	time.sleep(1)