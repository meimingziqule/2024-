#矩形识别变量与标志位
rect_flag  = 1
rect_points = []
rect_points_flag = 1
rect_point_num = 0
still_send_flag =0


#颠倒识别到的矩形四个顶点坐标顺序
def change_condi(corners_list):
    corners = [0,0,0,0]
    corners[0] = corners_list[-1]
    corners[1] = corners_list[-2]
    corners[2] = corners_list[-3]
    corners[3] = corners_list[-4]
    if corners is not None:
        return corners
#打印颠倒后的矩形四个顶点坐标，并返回矩形矩形顶点
def find_rect_corners(rect,img):
    for r in rect:
        #img.draw_rectangle(r.rect(), color = (255, 0, 0))
        corners = change_condi(r.corners())
        for p in corners:  # 颠倒点的顺序
            img.draw_cross(p[0], p[1], 5, color = (0, 255, 0))
        print(corners)#打印顶点[(x1,y1),................]
    return corners

#线段分割函数
def divide_line_segment(point1, point2, n):
    """
    将两个点连成的线段平分成n份，并返回包含这些点的数组。

    参数:
    point1 (tuple): 第一个点的坐标 (x1, y1)
    point2 (tuple): 第二个点的坐标 (x2, y2)
    n (int): 要平分的份数

    返回:
    list: 包含所有点的数组，例如[(x1, y1), (x2, y2), ...]CC
    """
    if n < 1:
        raise ValueError("n必须大于等于1")

    x1, y1 = point1
    x2, y2 = point2

    points = []
    for i in range(n + 1):
        x = x1 + (x2 - x1) * i / n
        y = y1 + (y2 - y1) * i / n
        points.append((x, y))

    return points

#矩形分割函数
def divide_polygon_segments(points, n):#如[(0.0, 0.0), (10.0, 1.2), (20.0, 2.4), (30.0, 3.6), (40.0, 4.8), (50.0, 6.0), (50.0, 6.0), (48.0, 10.8)]  
    """
    将一个四边形的每条边平分成n份，并将所有结果拼接成一个新的列表。

    参数:
    points (list): 包含四个点的列表，例如[(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    n (int): 要平分的份数

    返回:
    list: 包含所有点的数组，例如[(x1, y1), (x2, y2), ..., (x4, y4), ...]
    """
    if len(points) != 4:
        raise ValueError("points列表必须包含四个点")

    result = []
    for i in range(4):
        segment_points = divide_line_segment(points[i], points[(i + 1) % 4], n)
        result.extend(segment_points)

    return result
#缩放矩形框
def scale_rect_points(rect_points, scale_factor):
    x_coords = [point[0] for point in rect_points]
    y_coords = [point[1] for point in rect_points]
    center_x = sum(x_coords) / len(rect_points)
    center_y = sum(y_coords) / len(rect_points)
    scaled_points = []
    for point in rect_points:
        x = center_x + (point[0] - center_x) / scale_factor
        y = center_y + (point[1] - center_y) / scale_factor
        x = round(x, 1)
        y = round(y, 1)
        scaled_points.append((x, y))
    return scaled_points
#去重
def remove_duplicates_preserve_order(input_list):
    seen = set()
    unique_list = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            unique_list.append(item)
    return unique_list

while(True):
    #找到矩形后不再继续找
    if rect_flag == 1:
        rect = img.find_rects(threshold=17000)
        if rect:
            corners = find_rect_corners(rect, img)
            if corners:
                rect_flag = 0
        else:
            print("没找到矩形")
    else:
        print("corner:", corners)
        img.draw_rectangle(rect[0].rect(), color=(255, 255, 255))
    print("rect_points_flag",rect_points_flag)

    #识别一次矩形
    if rect_points_flag == 1:
        if rect:
            rect_points = divide_polygon_segments(corners, 2)
            rect_points_transform = scale_rect_points(rect_points, 1.06)#缩放矩形框
            rect_points_transform = remove_duplicates_preserve_order(rect_points_transform)#去除重复元素
            rect_points_flag = 0
            print("rect_point:", rect_points)

    #如果接收到了坐标发送信号且矩形识别完成    

    if data=='B' and rect_points_flag == 0:
        still_send_flag = 1
         
    #发送下一坐标点    
    elif data == 'A' and rect_points_flag == 0:
        rect_point_num += 1
        data = 0
    else:
        pass
        #print('等待接收数据')

    if still_send_flag ==1:    #持续发送坐标
        if rect_points is not None:
            send_data = '#0'+'X'+str(rect_points[rect_point_num][0])+'Y'+str(rect_points[rect_point_num][1])+'x'+str(red_blob.cx())+'y'+str(red_blob.cy())+';'
            print(send_data)
            #uart.write(send_data)    