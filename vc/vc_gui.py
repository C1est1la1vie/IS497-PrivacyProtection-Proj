import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets

from . import qr_coder
from . import visual_crypto


def show_visual_crypt(obj):
    obj.text_str = QtWidgets.QLineEdit('String')
    obj.main_layout.addWidget(obj.text_str, 3, 5, 1, 4)
    obj.labl_str = QtWidgets.QLabel('')
    obj.main_layout.addWidget(obj.labl_str, 7, 5, 2, 4)
    obj.labl_str.setAlignment(QtCore.Qt.AlignCenter)

    obj.button_qrenc = QtWidgets.QPushButton(qtawesome.icon('fa.qrcode', color='black'), "编码字符串")
    obj.button_qrenc.setObjectName('encStr')
    obj.main_layout.addWidget(obj.button_qrenc, 6, 3, 1, 2)
    obj.button_qrenc.clicked.connect(lambda: qrenc(obj))

    obj.button_vcenc = QtWidgets.QPushButton(qtawesome.icon('fa.lock', color='black'), "加密二维码")
    obj.button_vcenc.setObjectName('encImg')
    obj.main_layout.addWidget(obj.button_vcenc, 6, 5, 1, 2)
    obj.button_vcenc.clicked.connect(lambda: vcenc(obj))

    obj.button_vcdec = QtWidgets.QPushButton(qtawesome.icon('fa.unlock', color='black'), "解密二维码")
    obj.button_vcdec.setObjectName('decImg')
    obj.main_layout.addWidget(obj.button_vcdec, 6, 7, 1, 2)
    obj.button_vcdec.clicked.connect(lambda: vcdec(obj))

    obj.button_qrdec = QtWidgets.QPushButton(qtawesome.icon('fa.crosshairs', color='black'), "解码字符串")
    obj.button_qrdec.setObjectName('decStr')
    obj.main_layout.addWidget(obj.button_qrdec, 6, 9, 1, 2)
    obj.button_qrdec.clicked.connect(lambda: qrdec(obj))


def qrenc(obj):
    encoder = qr_coder.qrEncoder()
    img = encoder.enc_str(obj.text_str.text())
    img.show()
    img.save("./temp/msg.png")


def vcenc(obj):
    from PIL import Image
    obj.cryptCoder = visual_crypto.cryptCoder(path_dir='./temp/')
    img = Image.open("./temp/msg.png")
    obj.cryptCoder.get_msg(img)
    img_sct = obj.cryptCoder.get_sct()
    img_cph = obj.cryptCoder.get_cph()
    img_sct.show()
    img_cph.show()
    img_sct.save("./temp/sct.png")
    img_cph.save("./temp/cph.png")


def vcdec(obj):
    img_out = obj.cryptCoder.get_out()
    img_out.show()
    img_out.save("./temp/out.png")


def qrdec(obj):
    import cv2 as cv
    decoder = qr_coder.qrDecoder()
    imgarr = cv.imread("./temp/out.png")
    codeinfo = decoder.dec_str(decoder.process(imgarr))
    obj.labl_str = QtWidgets.QLabel(codeinfo)
    obj.main_layout.addWidget(obj.labl_str, 7, 5, 2, 4)
    obj.labl_str.setAlignment(QtCore.Qt.AlignCenter)
    # obj.labl_str.setText(str(codeinfo))
