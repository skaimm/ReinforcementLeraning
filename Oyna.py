import PongOyunu
import numpy as np
from skimage.exposure import rescale_intensity as YogunlukAyarla
from skimage.color import rgb2gray as Grilestir
from skimage.transform import resize as YenidenBoyutlandir
import keras

ResimYuksekligi = 40
ResimGenisligi = 40


def GoruntuHazirlama( Goruntu ):
    
    GriGoruntu = Grilestir(Goruntu)
    
    KirpilanGoruntu = GriGoruntu[0:400,0:400]
    
    HazirGoruntu = YenidenBoyutlandir(KirpilanGoruntu,(ResimYuksekligi,ResimGenisligi))
    
    HazirGoruntu = YogunlukAyarla(HazirGoruntu, out_range = (0,255))
    
    HazirGoruntu = HazirGoruntu / 128
    
    return HazirGoruntu

Ajan = keras.models.load_model('agent200000.h5')
Cevre = PongOyunu.PongOyunu()
Cevre.EkrandaGoruntuOlustur()
RandomAksiyon = 0

[BaslangicSkoru, BaslangicEkranGoruntusu] = Cevre.HareketEttir(RandomAksiyon)
BaslangicOyunGoruntusu = GoruntuHazirlama(BaslangicEkranGoruntusu)
GoruntuYigini = np.stack((BaslangicOyunGoruntusu,BaslangicOyunGoruntusu,BaslangicOyunGoruntusu,BaslangicOyunGoruntusu),axis = 2)
GoruntuYigini = GoruntuYigini.reshape(1, GoruntuYigini.shape[0],GoruntuYigini.shape[1],GoruntuYigini.shape[2])



while True:
    Qdegeri = Ajan.predict(GoruntuYigini)
    RandomAksiyon = np.argmax(Qdegeri)
    [Skor, YeniEkranGoruntusu] = Cevre.HareketEttir(RandomAksiyon)
        
    YeniOyunGoruntusu = GoruntuHazirlama(YeniEkranGoruntusu)
        
    YeniOyunGoruntusu = YeniOyunGoruntusu.reshape(1,YeniOyunGoruntusu.shape[0],YeniOyunGoruntusu.shape[1],1)
    [ReturnScore, NewScreenImage] = Cevre.HareketEttir(RandomAksiyon)
    NewGameImage = GoruntuHazirlama(NewScreenImage)
    NewGameImage = NewGameImage.reshape(1,NewGameImage.shape[0],NewGameImage.shape[1],1)
    GelecekGoruntuYigini = np.append(YeniOyunGoruntusu, GoruntuYigini[:,:,:,:3], axis = 3)
    GoruntuYigini = GelecekGoruntuYigini
    
    
