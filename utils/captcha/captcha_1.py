# coding: utf-8

import random
import string
from captcha.image import ImageCaptcha

def gene_captcha():
    words = string.ascii_letters + string.digits
    image = ImageCaptcha(fonts=['Courgette-Regular.ttf', 'LHANDW.TTF', 'Lobster-Regular.ttf', 'verdana.ttf'])
    k = random.sample(words, 4)
    data = image.generate(k)
    image.write(k, 'C:\\Code\\eru_bbs\\static\\imgs\\captcha.png')


if __name__ == '__main__':
    gene_captcha()