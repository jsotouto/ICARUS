#!/usr/bin/env python

import socket
# import wiringpi
import AlphaBot
Ab = AlphaBot.AlphaBot()
Ab.stop()

HOST = '192.168.0.5'
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
		Ab.stop()
		Ab.forward()

	elif 's' == data:
		print ('backward')
		Ab.stop()
		Ab.backward()

	elif 'a' == data:
		print ('left')
		Ab.stop()
		Ab.left()

	elif 'd' == data:
		print ('right')
		Ab.stop()
		Ab.right()

	elif 'q' == data:
		print ('stop')
		Ab.stop()
	
	else:
		continue

	if data == 'z':
		print('quit')
		break
	# conn.sendall(data)
conn.close()


