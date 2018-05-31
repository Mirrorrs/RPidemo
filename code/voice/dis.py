# coding = utf-8
import time
import RPi.GPIO as GPIO

"""这个demo用于距离的测定"""

GPIO.setwarnings(False)
trig = 13
echo = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(trig,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

# 返回距离
def dis_d():
    time.sleep(0.3)
    GPIO.output(trig,GPIO.HIGH)
    time.sleep(0.015)
    GPIO.output(trig,GPIO.LOW)
    start = 0
    end = 0
    usage = 0
    while not GPIO.input(echo):
        start = time.time()
    while GPIO.input(echo):
        end = time.time()
    usage = end - start

    return usage*17000

def main():
    try:
        while True:
            print(dis_d())
            time.sleep(2)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    main()


