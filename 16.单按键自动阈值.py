#需连接按键
#按键  openmv
# 1     P0
# 2     P1
# 3     P2
# 4     P3
# 5     P7
# 6     P8
# 7     P9

########注意注意注意注意注意！！！！！！！！！！！！！！  这里是独立开来的，按键有所改变

#按键1开启自动阈值模式
import sensor, image, time, pyb, math,display
from pyb import UART, LED, Pin, Timer
import math
pin_value = [1]  # 0 1 0 1  高低电平设置，与pin一一对应
pin_num = [0]  #pin口选择
jia_jian_flag = 0#手动阈值加减模式切换标志位，包含roi模式切换标志位
red_thresholds_num = [0, 100, 38, 77, 5, 69]
#roi
roi_change_step  = 2#roi变化步长
roi_jiajian_flag = 0#roi加减模式切换标志位
roi_set_one_flag= 1#roi初始化一次标志位
auto_thresholds_roi_num= [73,61,10,10]
auto_thresholds_roi = (int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3]))#自动阈值roi

sensor.reset() # 初始化sensor
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QQVGA2) # 128x160大小的特定液晶屏

#初始阈值
red_thresholds = (red_thresholds_num[0], red_thresholds_num[1], red_thresholds_num[2], red_thresholds_num[3], red_thresholds_num[4], red_thresholds_num[5])   

lcd = display.SPIDisplay() # 初始化lcd屏幕
clock = time.clock()
Time = 0.0

def handle_buttons(image):#传入画面
    #红色阈值，roi，阈值加减模式标志位，roi加减模式标志位，roi步长
    global red_thresholds_num,red_thresholds,auto_thresholds_roi_num,auto_thresholds_roi,jia_jian_flag,roi_jiajian,roi_jiajian_flag,roi_change_step
    img.draw_rectangle(int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3]), color=(255,255,255))

    if pin_value[0] == 0:
        img.draw_rectangle((int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3])), color = (255,255,255))
        statistics_Data = img.get_statistics(roi = (int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3])) )
        color_L_median = statistics_Data.l_median()     #分别赋值LAB的众数
        color_A_median = statistics_Data.a_median()
        color_B_median = statistics_Data.b_median()
        #计算颜色阈值，这样写的话，颜色阈值是实时变化的，后续想要什么效果可以自己修改
        
        red_thresholds_num[0] = color_L_median-20
        red_thresholds_num[1] = color_L_median+20
        red_thresholds_num[2] = color_A_median-20
        red_thresholds_num[3] = color_A_median+20
        red_thresholds_num[4] = color_B_median-20
        red_thresholds_num[5] = color_B_median+20
        red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])
        img.binary([red_thresholds]) #二值化看图像效果                    
        pyb.delay(200)   #有问题找延时         


def pin_IN(pin_num):
    for i in range(len(pin_num)):#设置引脚为输入引脚并获取引脚值
        p_in = Pin('P'+str(pin_num[i]), Pin.IN, Pin.PULL_UP)
        pin_value[i] = p_in.value()

while(True):
    img = sensor.snapshot()
    img = img.rotation_corr(180)
    img.draw_string(0, 0, str(Time), color = (255,0,0))
    pin_IN(pin_num)#设置GPIO引脚输入
    handle_buttons(img)#处理按钮按键响应
    lcd.write(img) # 拍照并显示图像
    Time = clock.fps()