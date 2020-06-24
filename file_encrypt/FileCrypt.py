import base64
import os
from Crypto.Cipher import AES
import file_encrypt.visual_crypto_FileCrypt
import file_encrypt.qr_coder_FileCrypt
import cv2 as cv
from PIL import Image
from file_encrypt.FileClient import *
import chardet

WorkPath = os.getcwd()
WorkPath = WorkPath+'\\file_encrypt'

class AES_128():

    def __init__(self):

        Download("127.0.0.1",23456,"cph.png")
        os.chdir(WorkPath)
        self.vc2qr("./sct.png", "./cph.png")
        os.remove("./cph.png")
        self.key = self.qr2str("./out.png")  # 密钥长度必须为16、24或32位，分别对应AES-128、AES-192和AES-256
        os.remove("./out.png")
        self.aes = AES.new(str.encode(self.key), AES.MODE_ECB)
        self.buffer = ""

    def qr2str(self,qr_path):
        qDecoder = file_encrypt.qr_coder_FileCrypt.qrDecoder()
        imgarr = cv.imread(qr_path)
        string = qDecoder.dec_str(qDecoder.process(imgarr))
        return string
    
    def vc2qr(self,img_sct, img_cph):
        cryptCoder = file_encrypt.visual_crypto_FileCrypt.cryptCoder(path_dir='./')
        img = Image.open(img_cph)
        cryptCoder.get_msg(img)
        # Generate secret and cipher image
        img_sct = Image.open(img_sct)
        img_cph = Image.open(img_cph)
        #
        img_out = cryptCoder.get_out(img_sct, img_cph)
        img_out.save("./out.png")
        return img_out
    # 补足字符串长度为16的倍数
    def add_to_16(self,s):
        #print(s)
        while len(s) % 16 != 0:
            s += b'\0'
        return s  # 返回bytes
 
    def encrypt(self,DirPath,Filename):
        os.chdir(DirPath)
        with open (Filename,"rb") as r:
            #try : 
            a = r.read()
            encrypted_text = base64.encodebytes(self.aes.encrypt(self.add_to_16(a)))
            self.buffer = encrypted_text
            
        r.close()
        if self.buffer != "":
            with open (Filename,"wb") as r:
                r.write(self.buffer)
                self.buffer = ""
            r.close()
    def decrypt(self,DirPath,Filename):
        os.chdir(DirPath)
        with open (Filename,"rb") as r:
            #try:
            decrypted_text = self.aes.decrypt(base64.decodebytes(r.read())).rstrip(b'\0')
            #print(decrypted_text)
            self.buffer = decrypted_text

        r.close()
        if self.buffer != "":
            with open (Filename,"wb") as r:
                r.write(self.buffer)
                self.buffer = ""
            r.close()