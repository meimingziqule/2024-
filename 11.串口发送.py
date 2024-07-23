uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

while(True):
    uart.write(data)