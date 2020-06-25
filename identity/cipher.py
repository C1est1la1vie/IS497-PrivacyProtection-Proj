from Crypto.Cipher import AES
import os

def add_16(par):
    par = par.encode('utf-8')
    while len(par) % 16 != 0:
        par += b'\x00'
    return par

def enc_pic(key,path):
    key = add_16(key)
    iv = "0000000000000000"
    iv = bytes(iv, encoding="utf8")
    input_file = open(path,'rb')
    input_data = input_file.read()
    input_file.close()
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
    enc_data = cfb_cipher.encrypt(input_data)

    enc_file = open(path+".enc", "wb")
    enc_file.write(enc_data)
    enc_file.close()
    os.remove(path)

def dec_pic(key,path):
    key = add_16(key)
    enc_file2 = open(path,'rb')
    enc_data2 = enc_file2.read()
    enc_file2.close()

    iv = "0000000000000000"
    iv = bytes(iv, encoding="utf8")

    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    plain_data = cfb_decipher.decrypt(enc_data2)

    output_file = open(path.rstrip(".enc"), "wb")
    output_file.write(plain_data)
    output_file.close()
    os.remove(path)

if __name__ == '__main__':
    dec_pic("test123",r"C:\Users\Administrator\Desktop\安全大作业\security\identity\recognizer\trainingData.yml.enc")

