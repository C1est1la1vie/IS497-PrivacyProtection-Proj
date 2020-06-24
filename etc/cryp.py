import pandas as pd
from zipfile import ZipFile
import os, sys, time, base64, pyAesCrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

sys.path.append("./etc/")

class core():
    def detemppwd(password):
        datapwd = password.split("b'")[1]
        password = datapwd.split("'")[1]
        password = datapwd.encode(encoding)
        keysalt = base64.urlsafe_b64encode(key+key)
        cipher_suite = Fernet(keysalt)
        password = cipher_suite.decrypt(password)
        password = password.decode('utf-8')
        return password

    def timeout(timestart):
        timedone = time.time()
        elapsed = float(timedone) - float(timestart)
        if elapsed >= secout:
            core.dialog_exit()
            self.close()
            core.exit_now('','')
        else:
            return None
        return None


    def hash_password(password):
        keysalt = base64.urlsafe_b64encode(key+key)
        bpass = bytes(password, encoding)
        cipher_suite = Fernet(keysalt)
        encoded_text = cipher_suite.encrypt(bpass)
        return encoded_text

    def sessioncheck():
        try:
            f = open(sessiontmp,"r")
            session = f.read()
            result = [x.strip() for x in session.split('\n')]
            otoken = result[0]
            timestart =  result[1]
            core.timeout(timestart)
            f.close()
            return True
        except:
            core.exit_now('','')
            return False
        return None

    def exit_now(token,timestart):
        try:
            df.drop(df.index, inplace=True)
        except:
            timestart=''
        try:
            os.remove(filetemp)
        except:
            token=''
        try:
            os.remove(sessiontmp)
        except:
            pass
        try:
            os.system('exit')
        except:
            pass
        return(sys.exit(1))


    def now():
        now = time.localtime()
        year = now[0]
        month = now[1]
        day = now[2]
        return (now,year,month,day)


    def verify_password(datapass,password):
        keysalt = base64.urlsafe_b64encode(key+key)
        bpass = bytes(password, encoding)
        cipher_suite = Fernet(keysalt)
        datapwd = datapass.split("b'")[1]
        datapass = datapwd.split("'")[1]
        datapass = datapwd.encode(encoding)
        dtext = cipher_suite.decrypt(datapass)
        dtext = dtext.decode(encoding)
        return password == dtext


    def decrypt(password):
        bpass = bytes(password, encoding)
        kdf = PBKDF2HMAC(
             algorithm=hashes.SHA256(),
             length=23,
             salt=key,
             iterations=100000,
             backend=default_backend()
        )
        keyencrypt = base64.urlsafe_b64encode(kdf.derive(bpass))
        keyfile = keyencrypt.decode(encoding)
        return keyfile
    

    def session():
        token = base64.urlsafe_b64encode(os.urandom(60))
        timestart = time.time()
        f=open(sessiontmp,"w+")
        f.write(str(token))
        f.write('\n')
        f.write(str(timestart))
        f.close()
        return(token,timestart)

secout = 360
encoding = "UTF-8"
filename = '.aes'
filetemp = '.temp'
sessiontmp = '.session'
bufferSize = 64 * 180024
key = b'\xde\xeb\xec5\xb1\x07XW\x03\x92U\x0f\xbb\xac\xf4\x03'