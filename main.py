import ctypes
import os
import sys
import threading
import tkinter as tk
import customtkinter

from tkinter import ttk, Frame

from user_interface import UI
from offset_rewriter import read_joystick
from rw_config import read_config

class vars:       
    def __init__(self):
        self.axis = [0, 0, 0, 0, 0, 0]
        self.new_axis = [0, 0, 0, 0, 0, 0]
        self.config = read_config() 
        self.joy_id = self.config['usages']['joy_id']
        self.msg = ''
        self.ReadInput = True
        self.KeepMain = True
        
def main():
    s1 = vars()

    thread1 = threading.Thread(target=read_joystick, args=(s1, ))
    thread1.start()
    
    thread2 = threading.Thread(target=UI, args=(s1, ))
    thread2.daemon = True
    thread2.start()
    thread2.join()
    
if __name__ == "__main__":
    myappid = 'Suundumused.Joy Offset.Joy Offset.1' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    main()