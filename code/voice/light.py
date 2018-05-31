# coding = utf-8
import os,sys,threading
sys.path.append('/home/pi/files/IoT/demo')
import Light
import cloud as Listener
import dis as Watcher
import led as Led
import RPi.GPIO as GPIO

"""声控灯的主程序"""

# 首先关闭所有的led
Led.off_red()

#　绿色的呼吸灯代表工作中，需要点亮
def status_light():
    Led.green()

# 主程序，在距离达到一定数值时，激活系统等待语音输入
def watch_dis():
    path = '/home/pi/files/IoT/voice/'
    count = 0
    while True:
        try:
            distance = Watcher.dis_d()
			# 将最后２０００个距离写入文件，方便调试            
			count += 1
            if count < 2000:
                with open('/home/pi/files/IoT/voice/data.txt','a+') as f:
                    f.write(str(count) + " ")
                    f.close()
            else:
                with open('/home/pi/files/IoT/voice/data.txt','w+') as f:
                    f.write('0 ')
                    f.close()
                    count = 0
			# 设定为１５ｃｍ
            if distance < 15:
                Led.red()
				# 录制一段音频
                os.system('arecord -D "plughw:1,0" -d 2 -f S16_LE /home/pi/files/IoT/voice/test.wav')
            
                words = Listener.use_cloud('/home/pi/files/IoT/voice/test.wav')
                if '关' in words:
                    Light.off_all()
                elif '开' in words:
                    Light.on_all()
				
				# 当识别不成功时，ｌｅｄ闪烁警告                
				else:
                    Led.blink1()
                Led.off_red()
        except:
            continue

# 设定两个线程，一个用于ｌｅｄ，另一个用于语音检测
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
