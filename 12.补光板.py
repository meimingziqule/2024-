import sensor, image, time, pyb,math,lcd
from pyb import UART, LED,Pin, Timer

# 50kHz pin6 timer2 channel1
light = Timer(2, freq=50000).channel(1, Timer.PWM, pin=Pin("P6"))
light.pulse_width_percent(50) # 控制亮度 0~100