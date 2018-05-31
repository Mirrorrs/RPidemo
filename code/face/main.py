# coding=utf-8
import os,sys,threading,time
import dis as Watcher
sys.path.append('/home/pi/files/IoT/voice')
sys.path.append('/home/pi/files/IoT/demo')
import Light
import led as Led
import RPi.GPIO as GPIO
from baidu_face import *

"""刷脸的主程序"""

Led.off_red()

# light to show working
def status_light():
    Led.green()

# watch the distance
def watch_dis():
    result_dic = {}
    count = 0
    path = '/home/pi/files/IoT/face/storage/test.jpg'
    while True:
        try:
            distance = Watcher.dis_d()
            count += 1
            if count < 2000:
                with open('/home/pi/files/IoT/face/data.txt','a+') as f:
                    f.write(str(count) + " ")
                    f.close()
            else:
                with open('/home/pi/files/IoT/face/data.txt','w+') as f:
                    f.write('0 ')
                    f.close()
            if distance < 60:
                time.sleep(0.5)
                if Watcher.dis_d() < 60:
                    Led.red()
                    command = 'raspistill -t 2000 -o ' + path + ' -q 5'
                    os.system(command)
                    Led.blink2()
                    result_dic = iden_myface(path)

                    try:
                        if int(float(result_dic['score'])) > 85:
                            print(result_dic['uid'] + ',please come in!')
                            Light.on(Light.pin1)
                    except:
                        print('Nothing.')

                    time.sleep(3)
                    Led.off_red()
        except:
            continue

# 两个线程
threads = []
t1 = threading.Thread(target = status_light)
threads.append(t1)
t2 = threading.Thread(target = watch_dis)
threads.append(t2)

if __name__ == '__main__':
    try:
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
    except KeyboardInterrupt:
        GPIO.cleanup()
