import random
import numpy as np
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D
from collections import deque


AksiyonSayisi = 3
ResimYuksekligi = 40
ResimGenisligi = 40
ResimSiniri = 4

Gozlem = 2500
GamaDegeri = 0.975
BatchBoyutu = 64

DeneyimTekrariKapasite = 2000


class Ajan:

    def __init__(self,HazirModel=""):
        if(HazirModel == ""):
            self.Model = self.ModelOlustur()
        else:
            self.Model = keras.models.load_model(HazirModel)
        self.DeneyimTekrari = deque()
        self.AdimSayisi = 0
        self.EpsilonDegeri = 1.0
    
    def ModelOlustur(self):
        Model = Sequential()
        
        Model.add(Conv2D(32, kernel_size=4, strides = (2,2), 
                         input_shape = (ResimYuksekligi,ResimGenisligi,ResimSiniri),padding = "same"))
        Model.add(Activation("relu"))
        Model.add(Conv2D(64,kernel_size=4,strides=(2,2),padding="same"))
        Model.add(Activation("relu"))
        Model.add(Conv2D(64,kernel_size=3,strides=(1,1),padding="same"))
        Model.add(Activation("relu"))
        Model.add(Flatten())
        Model.add(Dense(512))
        Model.add(Activation("relu"))
        Model.add(Dense(units= AksiyonSayisi, activation="linear"))
        
        Model.compile(loss = "mse", optimizer="adam")
        
        return Model
    
    def EnIyiAksiyonuBul(self, GoruntuGirdileri):
        if random.random() < self.EpsilonDegeri or self.AdimSayisi < Gozlem:
            return random.randint(0,AksiyonSayisi - 1)
        else:
            qvalue = self.Model.predict(GoruntuGirdileri)
            bestA = np.argmax(qvalue)
            return bestA
    
    def Depolama(self, Durum):
        self.DeneyimTekrari.append(Durum)
        if len(self.DeneyimTekrari) > DeneyimTekrariKapasite:
            self.DeneyimTekrari.popleft()
        
        self.AdimSayisi += 1 
        
        self.EpsilonDegeri = 1.0
        if self.AdimSayisi > Gozlem:
            self.EpsilonDegeri = 0.75
            if self.AdimSayisi > 7000:
                self.EpsilonDegeri = 0.5
            if self.AdimSayisi > 14000:
                self.EpsilonDegeri = 0.25
            if self.AdimSayisi > 30000:
                self.EpsilonDegeri = 0.15
            if self.AdimSayisi > 45000:
                self.EpsilonDegeri = 0.1
            if self.AdimSayisi > 70000:
                self.EpsilonDegeri = 0.05
                
    def EgitimSureci(self):
        if self.AdimSayisi > DeneyimTekrariKapasite:
            Ornekler = random.sample(self.DeneyimTekrari, BatchBoyutu)
            OrnekUzunlugu = len(Ornekler)
            
            Girdiler = np.zeros((BatchBoyutu,ResimYuksekligi,ResimGenisligi,ResimSiniri))
            Hedefler = np.zeros((Girdiler.shape[0],AksiyonSayisi))
            
            for i in range(OrnekUzunlugu):
                Durum = Ornekler[i][0]
                Aksiyon = Ornekler[i][1]
                Odul = Ornekler[i][2]
                GelecekDurum = Ornekler[i][3]
                
                Girdiler[i:i + 1] = Durum
                Hedefler[i]  = self.Model.predict(Durum)
                
                if GelecekDurum is None:
                    Hedefler[i,Aksiyon] = Odul
                else:
                    Hedefler[i,Aksiyon] = Odul + GamaDegeri*np.max(self.Model.predict(GelecekDurum))
                
            self.Model.fit(Girdiler, Hedefler ,batch_size= BatchBoyutu, epochs=1, verbose=0)
        if self.AdimSayisi % 10000 == 0:
            self.ModelKaydet(self.AdimSayisi)

    def ModelKaydet(self,Adim):
        self.Model.save("agent{e}.h5".format(e=Adim))
