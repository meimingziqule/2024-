import sensor, image, lcd, time, math
import KPU as kpu
import gc, sys
from machine import UART, Timer
from fpioa_manager import fm

lcd.init(freq=15000000)

while(True):
    img = sensor.snapshot()
    lcd.display(img)