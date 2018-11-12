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
#        self.server_socket = socket.socket()
#        self.server_socket.bind(('192.168.0.10', 9190))
#        self.server_socket.listen(0)
#        print('Ready to connect')
        
        # accept connection
#        self.connection, self.address = self.server_socket.accept()
#        print('Connected')

        # socket for controlling car
        self.client_socket = socket.socket()
        self.client_socket.connect(('192.168.0.5', 9200))

        
        self.collect_image()

    def collect_image(self):

        
        print('Start collecting images')
        
 
        stream_bytes = ' '
        frame = 1        

        while 1:

                # get input from human driver
                print('Press key')
                keyin = getch()
                if keyin == 'w':
                    print('Forward')
                    
                elif keyin == 'a':
                    print('Left')
                    
                elif keyin == 's':
                    print('Backward')
                    
                elif keyin == 'f':
                    print('Right')
                
                elif keyin == 'q':
                    print('Stop')
                elif keyin == 'z':
                    print('Quit')
                    break
                if keyin not in ['w', 'a', 's', 'd', 'q', 'z']:
                    continue
                self.client_socket.send(keyin)
                


if __name__ == '__main__':
    CollectTrainingData()
