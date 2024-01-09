import sys
import time
from RPLCD.i2c import CharLCD

def show(ml):

    lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
    try:
        lcd.backlight_enabled = True
        print('按下 Ctrl-C 可停止程式')
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string("{}".format(time.strftime("%m/%d %H:%M:%S")))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("OutPut:"+str(ml)+"ml")
        time.sleep(5)
        lcd.backlight_enabled = False
    except KeyboardInterrupt:
        print('關閉程式')
    finally:
        lcd.clear()

