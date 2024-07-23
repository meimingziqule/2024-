#使用这个前记得把自动曝光之类的关了
l_value= 60
baoguang = 20000
baoguang_step = 1500
sensor.set_auto_exposure(False,baoguang)#设置感光度  这里至关重要
auto_exposure_flag = True
auto_exposure_first = True

while(True):
    histogram = img.histogram()
    histogram_statistics = histogram.get_statistics()
    #print(histogram_statistics)

    if auto_exposure_first:
        for i in range(20):
            img = sensor.snapshot()
            # 计算图像的直方图
            histogram = img.histogram()
            histogram_statistics = histogram.get_statistics()
            # 计算图像的直方图
            histogram = img.histogram()
            histogram_statistics = histogram.get_statistics()
            # 提取 mode 值
            if hasattr(histogram_statistics, "mode"):
                mode_value = histogram_statistics.mode()  # 调用 mode 方法
                print("mode 值:", mode_value)
            else:
                print("histogram_statistics 对象没有 mode 方法")

            if mode_value > 40:
                baoguang -= baoguang_step
                sensor.set_auto_exposure(False,baoguang)#设置感光度  这里至关重要
                print("亮度减小")

            elif mode_value < 30:
                baoguang += baoguang_step
                sensor.set_auto_exposure(False,baoguang)#设置感光度  这里至关重要
                print("亮度增大")
            else:
                auto_exposure_first = False
    #print("调节已结束")