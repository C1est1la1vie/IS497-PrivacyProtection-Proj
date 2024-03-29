import time
import socket
import os
import sys 

host = "127.0.0.1"
port = 23456

def Upload(host,post,fileName):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    message = 'Upload ' + fileName
    file = '.\\file_encrypt\\'+fileName
    s.send(message.encode())
    try:
        with open(file, 'rb') as f:
            while True:
                a = f.read(1024)
                if not a:
                    break
                s.send(a)
            time.sleep(0.1)  # 延时确保文件发送完整
            s.send('EOF'.encode())
    except Exception:
        print("No such file founded")
    finally:
        s.close()

def Download(host,port,fileName):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
            #更新文件列表
    message = 'Download '+ fileName
    file = ".\\file_encrypt\\"+fileName
    s.send(message.encode())
    #File = s.recv(1024).decode()
    with open(file, 'wb') as f:
        while True:
            data = s.recv(1024)
            if data == 'EOF'.encode():
                break
            f.write(data)
    s.close()
