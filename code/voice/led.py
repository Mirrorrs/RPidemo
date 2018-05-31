# coding = utf-8
import RPi.GPIO as GPIO
import time

"""这个demo定义了一些led灯的工作方式, 
用于之后的调用"""

GPIO.setwarnings(False)
pins = [16,18]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pins,GPIO.OUT)

# 绿色的呼吸灯
def green():
    GPIO.output(pins[1],GPIO.LOW)
    pwm = GPIO.PWM(pins[0],50)
    pwm.start(0)
    while True:
        for i in range(0,101,10):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.1)
        for i in range(100,-1,-10):
            pwm.ChangeDutyCycle(i)
            time.sleep(0.1)
    pwm.stop()

# 红色灯的开启
def red():
    GPIO.output(pins[1],GPIO.HIGH)

# led闪烁五次
def blink1():
    for i in range(0,5):
        GPIO.output(pins[1],GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(pins[1],GPIO.LOW)
        time.sleep(0.05)

# 另一种闪烁方式
def blink2():
    for i in range(0,5):
        GPIO.output(pins[1],GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(pins[1],GPIO.HIGH)
        time.sleep(0.05)

# 关闭红色led
def off_red():
    GPIO.output(pins[1],GPIO.LOW)

if __name__ == '__main__':
    try:
        color = input()
        if color == 'red':
            red()
        elif color == 'green':
            green()
        elif color == 'b':
            blink1()
        elif color == 'b2':
            blink2()
    except KeyboardInterrupt:
        GPIO.cleanup()
