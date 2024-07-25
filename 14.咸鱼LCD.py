# 此代码适用于1.8寸屏幕，4.5.5的固件版本

import sensor, image, display, time

sensor.reset() # 初始化sensor
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种

sensor.set_framesize(sensor.QQVGA2) # 128x160大小的特定液晶屏
lcd = display.SPIDisplay() # 初始化lcd屏幕

clock = time.clock()
Time = 0.0

while(True):
    clock.tick()
    img = sensor.snapshot().lens_corr(strength = 1.8, zoom = 1.0)
    img = img.rotation_corr(180) # 将图像翻转180°  因为安装的时候openmv就是反着装的
    img.draw_string(0, 0, str(Time), color = (255,0,0))
    lcd.write(img) # 拍照并显示图像
    Time = clock.fps()
