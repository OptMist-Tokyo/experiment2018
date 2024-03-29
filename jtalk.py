#!/usr/bin/env python
# -*- encoding:utf8  -*-
#coding: utf-8

from __future__ import unicode_literals
import subprocess
from datetime import datetime

from multiprocessing import Process

import RPi.GPIO as GPIO
import time
import  pygame.mixer
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import codecs
import subprocess
import linecache
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

nagare = 0.005
hayakuti = 1.2

gyosu = 18

def discharge():
    pin = 26
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
    time.sleep(0.5)

def charge_time():
    pin = 26
    t1 = time.time()
    GPIO.setup(pin, GPIO.IN)
    while (not GPIO.input(pin)) and time.time() - t1 < 0.11:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        time.sleep(0.001)
        GPIO.setup(pin, GPIO.IN)
        time.sleep(0.001)
    t2 = time.time()
    return (t2 - t1)*10


def analog_read():
    discharge()
    return charge_time()


def ledisplay(m, n):
    m = 9 - m
    n += 10
    GPIO.output(m, GPIO.HIGH)
    GPIO.output(n, GPIO.LOW)
    time.sleep(0.0001)
    GPIO.output(m, GPIO.LOW)
    GPIO.output(n, GPIO.HIGH)


def represent(n, a):
    for i in range(16):
        a.append (0)
    for i in range(n+16):
        t1=time.time()
        while time.time() < t1+nagare:
            for j in range(8):
                for k in range(
                    16):
                    if  (a[i+k]>> j)  % 2 == 1:
                        ledisplay(j, k)
                    else:
                        time.sleep(0.000001)

def inv_represent(n, a):
    for i in range(16):
        a.append (0)
    for l in range(n+16):
        i = n + 15 - l
        t1=time.time()
        while time.time() < t1+nagare:
            for j in range(8):
                for k in range(16):
                    if  (a[i+k]>> j)  % 2 == 1:
                        ledisplay(j, k)
                    else:
                        time.sleep(0.000001)

#def jtalk(t):
    

def nihongo(a):
    str_flow = []

    for i in range(16):
        str_flow.append(0)

    # フォントの指定。引数は順に「フォントのパス」「フォントのサイズ」「エンコード」
    # メソッド名からも分かるようにTure Typeのフォントを指定する
    font = ImageFont.truetype('./misaki_gothic.ttf',
                              10, encoding='unic')
    input_str=a
    str_size = len(input_str)
    image = Image.new('RGBA', (str_size*10, 8))
    draw = ImageDraw.Draw(image)

    # 日本語の文字を入れてみる
    # 引数は順に「(文字列の左上のx座標, 文字列の左上のy座標)」「フォントの指定」「文字色」
    draw.text((0, 0), u'%s'%input_str, font = font, fill='#000000')

    image.save('hello.png', 'PNG')
    img = Image.open("hello.png")
    img_size=img.size
    img.show()
    img_np = np.array(img)
    for i in range(8):
        for j in range(str_size*10):
            if(img_np[i,j,3]>=70):
                img_np[i,j,3]=1
            else:
                img_np[i,j,3]=0
    #print(img_np)
    output = img_np[:,:,3]
    for j in range(str_size*10):
        tmp = 0
        for i in range(8):
            tmp += (2**i) * output[i, j]
        str_flow.append(tmp)
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed=['-r', str(hayakuti)]
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(a.encode('utf-8'))
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    jobs=[Process(target=represent, args=(str_size*10, str_flow)),
          Process(target=subprocess.Popen, args=(aplay, ))
        ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    #subprocess.Popen(aplay)
    time.sleep(0.5)
    b = a[::-1]
    d = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    d.stdin.write(b.encode('utf-8'))
    d.stdin.close()
    d.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    jobs=[Process(target=inv_represent, args=(str_size*10, str_flow)),
          Process(target=subprocess.Popen, args=(aplay, ))
        ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

def zannen():
    a = u'ざんねーん　これは回文ではありません'
    str_flow = []

    for i in range(16):
        str_flow.append(0)

    # フォントの指定。引数は順に「フォントのパス」「フォントのサイズ」「エンコード」
    # メソッド名からも分かるようにTure Typeのフォントを指定する
    font = ImageFont.truetype('./misaki_gothic.ttf',
                              10, encoding='unic')
    input_str=u'ざんねーん　これは回文ではありません'
    str_size = len(input_str)
    image = Image.new('RGBA', (str_size*10, 8))
    draw = ImageDraw.Draw(image)

    # 日本語の文字を入れてみる
    # 引数は順に「(文字列の左上のx座標, 文字列の左上のy座標)」「フォントの指定」「文字色」
    draw.text((0, 0), u'%s'%input_str, font = font, fill='#000000')

    image.save('hello.png', 'PNG')
    img = Image.open("hello.png")
    img_size=img.size
    img.show()
    img_np = np.array(img)
    for i in range(8):
        for j in range(str_size*10):
            if(img_np[i,j,3]>=70):
                img_np[i,j,3]=1
            else:
                img_np[i,j,3]=0
    #print(img_np)
    output = img_np[:,:,3]
    for j in range(str_size*10):
        tmp = 0
        for i in range(8):
            tmp += (2**i) * output[i, j]
        str_flow.append(tmp)
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed=['-r', str(hayakuti)]
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(a.encode('utf-8'))
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    jobs=[Process(target=represent, args=(str_size*10, str_flow)),
          Process(target=subprocess.Popen, args=(aplay, ))
        ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    #subprocess.Popen(aplay)

if __name__ == '__main__':
    for i in range(24):
        GPIO.setup(2+i, GPIO.OUT)
        if i < 8:
            GPIO.output(2+i, GPIO.LOW)
        else:
            GPIO.output(2+i, GPIO.HIGH)

    f = codecs.open('kaibun', 'r', 'utf-8')
    st = []

    for i in range(gyosu):
        input_str = f.readline()
        input_str = input_str[:-1]
        st.append(input_str)

    try:
        while True:
            #print(analog_read())
            if(analog_read() > 0.1):
                j = random.randrange(gyosu)
                nihongo(st[j])
                if(j > 15):
                    zannen()
            time.sleep(0.5)
        
    except KeyboardInterrupt:
        pass



    GPIO.cleanup()


