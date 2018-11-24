import cv2
import socket
import time
import os
import numpy as np
import keyboard

## Declaration of Getch ##

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

    
getch = _Getch()


## Collecting Data ##

class CollectTrainingData(object):

    def __init__(self):
        # socket for getting image
        self.server_socket = socket.socket()
        self.server_socket.bind(('192.168.1.19', 9190)) #PC IP
        self.server_socket.listen(0)
        print('Ready to connect')
        # accept connection
        self.connection = self.server_socket.accept()[0].makefile('rb')

        # socket for controlling car
        self.client_socket = socket.socket()
<<<<<<< HEAD
        self.client_socket.connect(('192.168.0.7', 9200))
=======
        self.client_socket.connect(('192.168.1.7', 9200)) #PI IP
>>>>>>> a3c2d441cdf5213252558d13d307e721b2521c75
        print('Connected')
        
        # create labels
        self.k = np.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = np.zeros((1, 4), 'float')
        
        self.collect_image()

    def collect_image(self):
        saved_frame = 0
        total_frame = 0
        
        print('Start collecting images')
        
        e1 = cv2.getTickCount()
        image_array = np.zeros((1, 120, 320))
        label_array = np.zeros((1, 4), 'float')

        stream_bytes = ' '
        frame = 1        

        while 1:
            stream_bytes += self.connection.read(1024)
            first = stream_bytes.find('\xff\xd8')
            last = stream_bytes.find('\xff\xd9')
#            keyin = 'q'
            if first != -1 and last != -1:
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                # image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)[1]

                # select lower half of the image
                roi = image[120:240, :]

                # save streamed images
                # cv2.imwrite('training_images/frame{:>05}.jpg'.format(frame), image)

                # cv2.imshow('roi_image', roi)
                cv2.imshow('image', image)

                # reshape the roi image into one row array
                temp_array = roi.reshape(1, 120, 320).astype(np.float32)

                frame += 1
                total_frame += 1

                # get input from human driver
                print('Press key')
                keyin = getch()
                #if keyboard.is_pressed('w'):
                if keyin == 'w':
                    print('Forward')
                    #keyin = 'w'
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, self.k[2]))
                    saved_frame += 1
                elif keyin == 'a':
                    print('Left')
                    #keyin = 'a'
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, self.k[0]))
                    saved_frame += 1
                elif keyin == 's':
                    print('Backward')
                    #keyin = 's'
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, self.k[3]))
                    saved_frame += 1
                elif keyin == 'd':
                    print('Right')
                    #keyin = 'd'
                    image_array = np.vstack((image_array, temp_array))
                    label_array = np.vstack((label_array, self.k[1]))
                    saved_frame += 1
                elif keyin == 'q':
                    print('Stop')
                    #keyin = 'q'
                elif keyin == 'z':
                    print('Quit')
                    #keyin = 'z'
                    break
                if keyin not in ['w', 'a', 's', 'd', 'q', 'z']:
                    continue
                self.client_socket.send(keyin)
                
            # save training images and labels
            train = image_array[1:, :]
            train_labels = label_array[1:, :]
#            print train
#            print train_labels

            # save training data as a numpy file
            file_name = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)
            try:
                np.savez(directory + '/' + file_name + '.npz', train=train, train_labels=train_labels)
            except IOError as e:
                print(e)

        e2 = cv2.getTickCount()
        # calculate streaming duration
        time0 = (e2 - e1) / cv2.getTickFrequency()
        print ('Streaming duration:', time0)

        print(train.shape)
        print(train_labels.shape)
        print ('Total frame:', total_frame)
        print ('Saved frame:', saved_frame)
        print ('Dropped frame', total_frame - saved_frame)

if __name__ == '__main__':
    CollectTrainingData()
