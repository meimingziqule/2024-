# 画圆
# 如果第一个参数是scaler，那么此方法应传递x y和半径。否则，它需要一个(x,y,半径)元组
img.draw_circle(x, y, radius, color=(r, g, b), thickness=2, fill=False)

# 画十字       
# 如果第一个参数是scaler，则此方法需要传递x和y。否则，它需要传递一个（x，y）元组。
img.draw_cross(x, y, color=(r, g, b), size=10, thickness=2)

# 画线段
# 画线函数img.draw_line((x0, y0, x1, y1), color=White)
img.draw_line((i, 0, i, img.height()-1), color = int(c))

#画矩形
#传递一个(x,y,w,h)元组
img.draw_rectangle(x, y, w, h, color=(r, g, b), thickness=2, fill=False)

#写字符串        
img.draw_string(x,y,"Hello World!",color=(r, g, b),scale=2)