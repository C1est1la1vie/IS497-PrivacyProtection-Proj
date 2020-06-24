# by nyLiao, 2020

from cv2 import blur, threshold, QRCodeDetector, bitwise_not, THRESH_BINARY_INV
from PIL import Image


class qrEncoder(object):
    def __init__(self):
        super(qrEncoder, self).__init__()

    def _pil2pil(self, img):
        import io
        buffered = io.BytesIO()
        img.save(buffered)
        return Image.open(buffered)

    def enc_str(self, s):
        import qrcode
        img = self._pil2pil(qrcode.make(s))
        return img


class qrDecoder(object):
    def __init__(self):
        super(qrDecoder, self).__init__()

    def process(self, imgarr):
        imgarr_blr = blur(imgarr, ksize=(3, 3))
        _, dst = threshold(imgarr_blr, 150, 255, THRESH_BINARY_INV)
        return dst

    def dec_str(self, imgarr):
        qrcoder = QRCodeDetector()
        codeinfo, points, straight_qrcode = qrcoder.detectAndDecode(imgarr)
        if codeinfo == '':
            imgarr = bitwise_not(imgarr)
            codeinfo, points, straight_qrcode = qrcoder.detectAndDecode(imgarr)
        return codeinfo
