#需连接按键
#按键  openmv
# 1     P0
# 2     P1
# 3     P2
# 4     P3
# 5     P7
# 6     P8
# 7     P9

#1. 上电默认“++”模式：按键1-6  L-A-B最大最小值  "++"  
#2. 1,2按键一起按：1-6  L-A-B最大最小值  "--"
#3. 2,3按键一起按切换为“++”模式：1-6  L-A-B最大最小值  "++"
#4. ①3,4按键一起按：roi框位置大小调节模型 1-4分别为x,y,w,h的增加按键
#   ②roi模式下，6，7一起按切换“--”模式，再次1,2一起按切换回“++”模式
#5.按键7切换为自动阈值模式，按键8为二值化图像预览

pin_value = [1,1,1,1,1,1,1,1]  # 0 1 0 1  高低电平
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
    if pin_value[0] == 0 and  pin_value[1] == 0 :#按键1,2,同时按下为切换减模式
        jia_jian_flag = 1                
    elif pin_value[1] == 0 and  pin_value[2] == 0 :#按键2,3同时按下为切换加模式
        jia_jian_flag = 0
    elif pin_value[2] == 0 and  pin_value[3] == 0 :#按键3,4同时按下为切换roi框调整模式
        jia_jian_flag = 2
    if jia_jian_flag == 0:
        img.draw_string(80,0,"++", color=(0,0,255))
        if pin_value[0] == 0:
            red_thresholds_num[0] += 2
            if red_thresholds_num[0] >= 100:
                red_thresholds_num[0] = 0
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])
            pyb.delay(200)  # 消除按键抖动

        if pin_value[1] == 0:
            red_thresholds_num[1] += 2
            if red_thresholds_num[1] >= 100:
                red_thresholds_num[1] = 0
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(100)
    
        if pin_value[2] == 0:
            red_thresholds_num[2] += 2
            if red_thresholds_num[2] >= 127:
                red_thresholds_num[2] = 0
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(100)
    
        if pin_value[3] == 0:
            red_thresholds_num[3] += 2
            if red_thresholds_num[3] >= 127:
                red_thresholds_num[3] = 0
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(200)  # 有问题找延时
    
        if pin_value[4] == 0:
            red_thresholds_num[4] += 2
            if red_thresholds_num[4] >= 127:
                red_thresholds_num[4] = 0
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(100)
    
        if pin_value[5] == 0:
            red_thresholds_num[5] += 2
            if red_thresholds_num[5] >= 127:
                red_thresholds_num[5] = 0
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(200)  # 有问题找延时
            #自动阈值模式
        if pin_value[6] == 0:
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
        if pin_value[7] == 0:
            img.binary([red_thresholds]) #二值化看图像效果
    elif jia_jian_flag == 1:
        img.draw_string(80,0,"--", color=(0,0,255))
        if pin_value[0] == 0:
            red_thresholds_num[0] -= 2
            if red_thresholds_num[0] <= 0:
                red_thresholds_num[0] = 100
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])
            pyb.delay(200)  # 消除按键抖动
    
        if pin_value[1] == 0:
            red_thresholds_num[1] -= 2
            if red_thresholds_num[1] <= 0:
                red_thresholds_num[1] = 100
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(100)
    
        if pin_value[2] == 0:
            red_thresholds_num[2] -= 2
            if red_thresholds_num[2] <= 0:
                red_thresholds_num[2] = 127
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(100)
    
        if pin_value[3] == 0:
            red_thresholds_num[3] -= 2
            if red_thresholds_num[3] <= 0:
                red_thresholds_num[3] = 127
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(200)  # 有问题找延时
    
        if pin_value[4] == 0:
            red_thresholds_num[4] -= 2
            if red_thresholds_num[4] <= 0:
                red_thresholds_num[4] = 127
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(100)
    
        if pin_value[5] == 0:
            red_thresholds_num[5] -= 2
            if red_thresholds_num[5] <= 0:
                red_thresholds_num[5] = 127
            red_thresholds = (red_thresholds_num[0],red_thresholds_num[1],red_thresholds_num[2],red_thresholds_num[3],red_thresholds_num[4],red_thresholds_num[5])    
            pyb.delay(200)  # 有问题找延时
            #自动阈值模式
        if pin_value[6] == 0:
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
            #img.binary([red_thresholds]) #二值化看图像效果                    
            #pyb.delay(200)   #有问题找延时         
        if pin_value[7] == 0:
            img.binary([red_thresholds]) #二值化看图像效果
    elif jia_jian_flag == 2:
        #画出roi框
        img.draw_rectangle(int(auto_thresholds_roi_num[0]),int(auto_thresholds_roi_num[1]),int(auto_thresholds_roi_num[2]),int(auto_thresholds_roi_num[3]), color=(255,255,255))
        #默认roi++模式
        if roi_jiajian_flag == 0:
            img.draw_string(80,0,"roi++", color=(0,0,255))
            if pin_value[5] == 0 and pin_value[6] == 0:
                roi_jiajian_flag = 1
                pyb.delay(500)
            if pin_value[0] == 0:
                auto_thresholds_roi_num[0] += roi_change_step
                if auto_thresholds_roi_num[0] >= image.width():
                    auto_thresholds_roi_num[0] = 0
                pyb.delay(100)#消除按键抖动
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
            if pin_value[6] == 0:
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
            if pin_value[7] == 0:
                img.binary([red_thresholds]) #二值化看图像效果
        #roi模式下1,2同时按切换成roi--模式        
        elif roi_jiajian_flag ==1:
            img.draw_string(80,0,"roi--", color=(0,0,255))
            if pin_value[5] == 0 and pin_value[6] == 0:
                roi_jiajian_flag = 0
                pyb.delay(500)
            if pin_value[0] == 0:
                auto_thresholds_roi_num[0] -= roi_change_step
                if auto_thresholds_roi_num[0] <= 0:
                    auto_thresholds_roi_num[0] = image.width()
                pyb.delay(100)#消除按键抖动
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
            if pin_value[6] == 0:
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
            if pin_value[7] == 0:
                img.binary([red_thresholds]) #二值化看图像效果

def pin_IN(pin_num):
    for i in range(len(pin_num)):#设置引脚为输入引脚并获取引脚值
        p_in = Pin('P'+str(pin_num[i]), Pin.IN, Pin.PULL_UP)
        pin_value[i] = p_in.value()

while(True):

    pin_IN(pin_num)#设置GPIO引脚输入
    handle_buttons(img)#处理按钮按键响应