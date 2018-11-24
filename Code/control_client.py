# -*- coding: utf-8 -*-
#!/usr/bin/env python

import socket
import wiringpi2 as wiringpi
#import AlphaBot
#Ab = AlphaBot.AlphaBot()
#Ab.stop()

#--- declaration of motor status---

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWORD = 2
LEFT = 1
RIGHT = 2

# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0



# 실제 핀 정의
#PWM PIN
ENA = 25
ENB = 30

#GPIO PIN
IN1 = 24
IN2 = 23
IN3 = 22
IN4 = 21


# 핀 설정 함수
def setPinConfig(EN, INA, INB):
    wiringpi.pinMode(EN, OUTPUT)
    wiringpi.pinMode(INA, OUTPUT)
    wiringpi.pinMode(INB, OUTPUT)
    wiringpi.softPwmCreate(EN, 0, 255)

# 모터 제어 함수
def setMotorContorl(PWM, INA, INB, speed, stat):
    #모터 속도 제어 PWM
    wiringpi.softPwmWrite(PWM, speed)

    #앞으로
    if stat == FORWARD:
        wiringpi.digitalWrite(INA, HIGH)
        wiringpi.digitalWrite(INB, LOW)
    #뒤로
    elif stat == BACKWORD:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, HIGH)
    #정지
    elif stat == STOP:
        wiringpi.digitalWrite(INA, LOW)
        wiringpi.digitalWrite(INB, LOW)

# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed, stat):
    if ch == CH1:
        setMotorContorl(ENA, IN1, IN2, speed, stat)
    else:
        setMotorContorl(ENB, IN3, IN4, speed, stat)

#GPIO 라이브러리 설정
wiringpi.wiringPiSetup()

#모터 핀 설정
setPinConfig(ENA, IN1, IN2)
setPinConfig(ENB, IN3, IN4)

#---

HOST = '192.168.0.5' #PI IP
PORT = 9200
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
#s.connect((HOST, PORT))
conn, addr = s.accept()
print ('Connected')

while 1:
	data = conn.recv(1024)
	if not data: break
	# decode_str = data.decode()

	if 'w' == data:
		print ('forward')
		setMotor(CH1, 100, FORWARD)

	elif 's' == data:
		print ('backward')
		setMotor(CH1, 100, BACKWORD)

	elif 'a' == data:
		print ('left')
		setMotor(CH2, 100, LEFT)

	elif 'd' == data:
		print ('right')
		setMotor(CH2, 100, RIGHT)


	elif 'q' == data:
		print ('stop')
		setMotor(CH1, 100, STOP)
		setMotor(CH2, 100, STOP)

	else:
		continue

	if data == 'z':
		print('quit')
		break
	# conn.sendall(data)
conn.close()


