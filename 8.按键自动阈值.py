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

#1. 1-4分别为x,y,w,h的增加按键
#2. 1，2一起按切换“--”模式，再次1,2一起按切换回“++”模式
#3. 按键3,4切换为自动阈值模式，按键1,2,3,4为二值化图像预览
import sensor, image, time, pyb, math,display
from pyb import UART, LED, Pin, Timer
import math
sensor.reset()
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time = 2000)
pin_value = [1,1,1,1,1,1,1,1]  # 0 1 0 1  高低电平设置，与pin一一对应
pin_num = [0,1,2,3,6,7,8,9]  #pin口选择
jia_jian_flag = 0#手动阈值加减模式切换标志位，包含roi模式切换标志位 
red_thresholds_num = [0, 100, 38, 77, 5, 69]
#roi
roi_change_step  = 2#roi变化步长
roi_jiajian_flag = 0#roi加减模式切换标志位
roi_set_one_flag= 1#roi初始化一次标志位
auto_thresholds_roi_num= [73,61,6,7]
auto_thresholds_roi = (int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3]))#自动阈值roi

#初始阈值
red_thresholds = (red_thresholds_num[0], red_thresholds_num[1], red_thresholds_num[2], red_thresholds_num[3], red_thresholds_num[4], red_thresholds_num[5])   

def handle_buttons(image):#传入画面
    #红色阈值，roi，阈值加减模式标志位，roi加减模式标志位，roi步长
    global red_thresholds_num,red_thresholds,auto_thresholds_roi_num,auto_thresholds_roi,jia_jian_flag,roi_jiajian,roi_jiajian_flag,roi_change_step
    img.draw_rectangle(int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3]), color=(255,255,255))
    #默认roi++模式  6,7按键同时按下为切换
    if roi_jiajian_flag == 0:
        img.draw_string(80,0,"roi++", color=(0,0,255))
        if pin_value[0] == 0 and pin_value[1] == 0:
            roi_jiajian_flag = 1
            pyb.delay(500)
        if pin_value[0] == 0:
            auto_thresholds_roi_num[0] += roi_change_step
            if auto_thresholds_roi_num[0] >= image.width():
                auto_thresholds_roi_num[0] = 0
            pyb.delay(200)#消除按键抖动
        if pin_value[1] == 0:
            auto_thresholds_roi_num[1] += roi_change_step
            if auto_thresholds_roi_num[1] >= image.height():
                auto_thresholds_roi_num[1] = 0
            pyb.delay(200)    
        if pin_value[2] == 0:
            auto_thresholds_roi_num[2] += roi_change_step
            if auto_thresholds_roi_num[2] >= image.width()-auto_thresholds_roi_num[0]:
                auto_thresholds_roi_num[2] = roi_change_step
            pyb.delay(200)    
        if pin_value[3] == 0:
            auto_thresholds_roi_num[3] += 5
            if auto_thresholds_roi_num[3] >=image.height()-auto_thresholds_roi_num[1]:
                auto_thresholds_roi_num[3] = roi_change_step
            pyb.delay(200)   #有问题找延时
        if pin_value[2] == 0 and pin_value[3] == 0:
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
            #按键1，2，3，4 
        if pin_value[0] == 0 and pin_value[1] == 0 and pin_value[2] == 0 and pin_value[3] == 0:
            img.binary([red_thresholds]) #二值化看图像效果
    #roi模式下1,2同时按切换成roi--模式        
    elif roi_jiajian_flag ==1:
        img.draw_string(80,0,"roi--", color=(0,0,255))
        if pin_value[0] == 0 and pin_value[1] == 0:
            roi_jiajian_flag = 0
            pyb.delay(500)
        if pin_value[0] == 0:
            auto_thresholds_roi_num[0] -= roi_change_step
            if auto_thresholds_roi_num[0] <= 0:
                auto_thresholds_roi_num[0] = image.width()
            pyb.delay(200)#消除按键抖动
        if pin_value[1] == 0:
            auto_thresholds_roi_num[1] -= roi_change_step
            if auto_thresholds_roi_num[1] <= 0:
                auto_thresholds_roi_num[1] = image.height()
            pyb.delay(200)    
        if pin_value[2] == 0:
            auto_thresholds_roi_num[2] -= roi_change_step
            if auto_thresholds_roi_num[2] <= roi_change_step:
                auto_thresholds_roi_num[2] = image.width()-auto_thresholds_roi_num[0]
            pyb.delay(200)    
        if pin_value[3] == 0:
            auto_thresholds_roi_num[3] -= roi_change_step
            if auto_thresholds_roi_num[3] <=roi_change_step:
                auto_thresholds_roi_num[3] = image.height()-auto_thresholds_roi_num[1]
            pyb.delay(200)   #有问题找延时
        if pin_value[2] == 0 and pin_value[3] == 0:
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
        #按键1，2，3，4
        if pin_value[0] == 0 and pin_value[1] == 0 and pin_value[2] == 0 and pin_value[3] == 0:
            img.binary([red_thresholds]) #二值化看图像效果

def pin_IN(pin_num):
    for i in range(len(pin_num)):#设置引脚为输入引脚并获取引脚值
        p_in = Pin('P'+str(pin_num[i]), Pin.IN, Pin.PULL_UP)
        pin_value[i] = p_in.value()

while(True):
    img = sensor.snapshot()
    img = img.rotation_corr(180)
    pin_IN(pin_num)#设置GPIO引脚输入
    handle_buttons(img)#处理按钮按键响应
    