import sensor, image, time, pyb, math, lcd
from pyb import UART, LED, Pin, Timer

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

buffer = ""

#接收“#b;”的数据帧
def receive_data():
    global buffer
    if uart.any():
        char = uart.read(1).decode()
        if char == '#':
            buffer = ""
        elif char == ';':
            if buffer:
                data = buffer
                buffer = ""
                return data
        else:
            buffer += char
    else:
        time.sleep_ms(1)

while True:
    data = receive_data()
    if data == 'B':
        still_send_flag = 1
        LED(3).on()
    