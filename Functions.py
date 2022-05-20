import imageio
from skimage.transform import resize
from os import listdir, mkdir
import numpy as np
import colorsys
import keras

import cv2

en = 224
boy = 224
kanal = 1

if(kanal==1):
    renkliDeger = "gri"
elif(kanal==3):
    renkliDeger = "renkli"

resimlerDiziniOrjinal = "Resimler_Orjinal"
resimlerDiziniOnIslenmis = "Resimler_OnIslenmis"

etiketler = listdir(resimlerDiziniOrjinal)
etiketler.sort()
etiketSayisi = len(etiketler)
liste1 = [0 for i in range(etiketSayisi)]
yeniliste = [liste1, etiketler]

enbuyuketiket = []
enbuyukdeger = []
enbuyukler = [enbuyukdeger, enbuyuketiket]

def kanal_ayarla(resim):
    """
    _, _, kanalSayisi = resim.shape
    if(kanalSayisi > 3):
        rgb2hsv = np.vectorize(colorsys.rgb_to_hsv)
        h,s,v = rgb2hsv(resim[:,:,0], resim[:,:,1], resim[:,:,2])
        h *= h
        hsv2rgb= np.vectorize(colorsys.hsv_to_rgb)
        resim = hsv2rgb(h,s,v)
        resim = np.array(resim).transpose((1,2,0))
        resim.flatten();
    """

    if len(resim.shape) > 2 and resim.shape[2] == 4:
        resim = cv2.cvtColor(resim, cv2.COLOR_BGRA2BGR)
    resim = resize(resim, (boy, en, kanal))
    return resim

def resmi_kaydet(path, etiket, deger):
    if(deger=="gri"):
        resim = imageio.imread(path, as_gray=True)
        resim.flatten();
        resim = resize(resim, (boy, en, kanal))
        imageio.imwrite(resimlerDiziniOnIslenmis + '/' + etiket, resim)
    elif(deger=="renkli"):
        resim = imageio.imread(path, as_gray=False)
        resim = kanal_ayarla(resim)
        imageio.imwrite(resimlerDiziniOnIslenmis + '/' + etiket, resim)

def resmi_al(path, deger):
    if(deger=="gri"):
        resim = imageio.imread(path, as_gray=True)
        resim.flatten();
        resim = resize(resim, (boy, en, kanal))
        return resim
    elif(deger=="renkli"):
        resim = imageio.imread(path, as_gray=False)
        resim = kanal_ayarla(resim)
        return resim

def kontrol(image, model):
    print("[INFO] loading network...")
    model.predict(image, batch_size=1)
    prob = model.predict_proba(image)

    etiketler.sort()
    for i in range(etiketSayisi):
        liste1[i] = '{:.4f}'.format(prob[0][i])

    for a in range(0,etiketSayisi):
        for i in range(a+1,etiketSayisi):
             if ((i)!=etiketSayisi) and (yeniliste[0][a]<yeniliste[0][(i)]):
                c=yeniliste[0][a]
                yeniliste[0][a]=yeniliste[0][i]
                yeniliste[0][i]=c
                c1=yeniliste[1][a]
                yeniliste[1][a]=yeniliste[1][i]
                yeniliste[1][i]=c1
                
    """
    etiketAdi = yeniliste[1][0]
    if(etiketAdi[0:2] == 'AA'):
        if(yeniliste[0][0]>'0.60'):
            enbuyuketiket.append(yeniliste[1][0])
            enbuyukdeger.append(yeniliste[0][0])
    """
         
    print (yeniliste)
    return yeniliste