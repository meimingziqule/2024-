import sensor, image, lcd, time, math
import KPU as kpu
import gc, sys
from machine import UART, Timer
from fpioa_manager import fm

fm.register(18, fm.fpioa.UART1_TX, force=True)
fm.register(19, fm.fpioa.UART1_RX, force=True)
uart = UART(UART.UART1, 115200, 8, 1, 0, timeout=1000, read_buf_len=4096)

uart.write("#0b"+str(most_commom_value)+';')
