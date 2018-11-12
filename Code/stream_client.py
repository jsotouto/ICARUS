import io
import socket
import struct
import time
import picamera

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.10', 9190))
connection = s.makefile('wb')

try:
	with picamera.PiCamera() as camera:
		camera.resolution = (320,240)
		camera.framerate = 10
		time.sleep(2)
		start = time.time()
		stream = io.BytesIO()

		for foo in camera.capture_continuous(stream, format='jpeg', use_video_port = True):
			connection.write(struct.pack('<L', stream.tell()))
			connection.flush()
			stream.seek(0)
			connection.write(stream.read())
			if time.time() - start > 600:
				break
			stream.seek(0)
			stream.truncate()
	connection.write(struct.pack('<L', 0))
finally:
	connection.close()
	s.close()

