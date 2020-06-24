import socketserver
import socket
import os
import time
import threading

class FileServer(threading.Thread):
    def __init__(self, host , port):
        threading.Thread.__init__(self)
        self.ADDR = (host, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.first = r'.'
        os.chdir(self.first)                                     # first是初始路径 在linux系统中反斜杠需要修改

    def tcp_connect(self, conn, addr):
        print(' Connected by: ', addr)
        
        while True:
            data = conn.recv(1024)
            data = data.decode()
            if data == 'quit':
                print('Disconnected from {0}'.format(addr))
                break
            order = data.split(' ')[0]                             # 获取相应命令
            self.recv_func(order, data, conn)
                
        conn.close()

    # 保存上传文件
    def Recv(self, message, conn):

        name = message.split()[1]                              # 获取文件名
        fileName = name
        with open(fileName, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if data == 'EOF'.encode():
                    f.close()
                    break
                f.write(data)

    def Send(self, message, conn):
        name = message.split()[1]                               # 获取第二个参数(文件名)
        fileName = name

        try:
            with open(fileName, 'rb') as f:    
                while True:
                    a = f.read(1024)
                    if not a:
                        break
                    conn.send(a)
            time.sleep(0.1)                                          # 延时确保文件发送完整
            conn.send('EOF'.encode())
        except Exception:
            print(fileName)
            print("No such file, please check the file name")

    # 判断输入的命令并执行对应的函数
    def recv_func(self, order, message, conn):
        if order == 'Upload':
            return self.Recv(message, conn)
        elif order == 'Download':
            return self.Send(message, conn)

    #运行客户端
    def run(self):
        print('File Service Start...')
        self.s.bind(self.ADDR)
        self.s.listen(5)
        while True:
            conn, addr = self.s.accept()
            t = threading.Thread(target=self.tcp_connect, args=(conn, addr))
            t.start()
        self.s.close()


if __name__ == "__main__":
    
    host = "127.0.0.1"
    port = 23456
    FileServer = FileServer(host,port)
    FileServer.start()