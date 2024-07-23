lcd.init(freq=15000000)

while(True):
    img = sensor.snapshot()
    lcd.display(img)