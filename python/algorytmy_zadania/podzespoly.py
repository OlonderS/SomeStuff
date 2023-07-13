import os
import socket
import sys
import platform
from tkinter import *
text=''
def write(napis):
    global text
    text=str(napis)
    field.set(text)
    
if __name__=="__main__":
    gui = Tk()
    gui.configure(background="light blue")
    gui.title("Toolkit")
    gui.geometry("400x250")
    
    button_opt = {'fill': constants.BOTH, 'padx': 15, 'pady': 5}
    field = StringVar()
    expression = Entry(gui, textvariable=field)
    expression.pack(fill = constants.BOTH, padx=15, pady=10)
    
    btn1=Button(gui, text='Name:', command=lambda:write("Name: " + socket.gethostname())).pack(**button_opt)
    btn2=Button(gui, text='System platform:', command=lambda: write("System Platform: "+sys.platform)).pack(**button_opt)
    btn3=Button(gui, text='Version:', command=lambda: write("Version: " +platform.version())).pack(**button_opt)
    btn4=Button(gui, text='Machine:', command=lambda: write("Machine: " +platform.machine())).pack(**button_opt)
    btn5=Button(gui, text='Processor:', command=lambda: write("Processor: " +platform.processor())).pack(**button_opt)
    btn6=Button(gui, text='Number of CPUs:', command=lambda: write("Number of CPUs: " +str(os.cpu_count()))).pack(**button_opt)
    
    gui.mainloop()
