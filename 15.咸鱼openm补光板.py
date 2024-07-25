# PWM 控制例子
#
# 这个例子展示了如何使用OpenMV的PWM
 
import time
from pyb import Pin, Timer
 
tim = Timer(4, freq=1000) #设置频率，初始化定时器4，将其设置为1000HZ
# 生成50HZ方波，使用TIM4的channels 1输出占空比为 50%的PWM
ch1 = tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=70)

 
while (True):
    ch1.pulse_width_percent(60)