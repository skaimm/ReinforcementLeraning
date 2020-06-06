import PongAjan
import PongOyunu
import numpy as np
from skimage.color import rgb2gray as Grilestir
from skimage.transform import resize as YenidenBoyutlandir
from skimage.exposure import rescale_intensity as YogunlukAyarla

import warnings
warnings.filterwarnings("ignore")

EgitimDonguSayisi = 400000

ResimYuksekligi = 40
ResimGenisligi = 40
ResimSiniri = 4

def GoruntuHazirlama( Goruntu ):
    
    GriGoruntu = Grilestir(Goruntu)
    
    KirpilanGoruntu = GriGoruntu[0:400,0:400]
    
    HazirGoruntu = YenidenBoyutlandir(KirpilanGoruntu,(ResimYuksekligi,ResimGenisligi))
    
    HazirGoruntu = YogunlukAyarla(HazirGoruntu, out_range = (0,255))
    
    HazirGoruntu = HazirGoruntu / 128
    
    return HazirGoruntu


def Egitim():
    
    EgitimGecmisDepolama = []
    
    Cevre = PongOyunu.PongOyunu()
    
    Cevre.EkrandaGoruntuOlustur()
    
    Ajan = PongAjan.Ajan()
    
    RandomAksiyon = 0
    
    [BaslangicSkoru, BaslangicEkranGoruntusu] = Cevre.HareketEttir(RandomAksiyon)
    BaslangicOyunGoruntusu = GoruntuHazirlama(BaslangicEkranGoruntusu)
    
    GoruntuYigini = np.stack((BaslangicOyunGoruntusu,BaslangicOyunGoruntusu,BaslangicOyunGoruntusu,BaslangicOyunGoruntusu),axis = 2)
    
    GoruntuYigini = GoruntuYigini.reshape(1, GoruntuYigini.shape[0],GoruntuYigini.shape[1],GoruntuYigini.shape[2])
    
    for i in range(EgitimDonguSayisi):
        
        RandomAksiyon = Ajan.EnIyiAksiyonuBul(GoruntuYigini)
        [Skor, YeniEkranGoruntusu] = Cevre.HareketEttir(RandomAksiyon)
        
        YeniOyunGoruntusu = GoruntuHazirlama(YeniEkranGoruntusu)
        
        YeniOyunGoruntusu = YeniOyunGoruntusu.reshape(1,YeniOyunGoruntusu.shape[0],YeniOyunGoruntusu.shape[1],1)
        
        GelecekGoruntuYigini = np.append(YeniOyunGoruntusu, GoruntuYigini[:,:,:,:3], axis = 3)
        
        Ajan.Depolama((GoruntuYigini,RandomAksiyon,Skor,GelecekGoruntuYigini))
        
        Ajan.EgitimSureci()
        
        GoruntuYigini = GelecekGoruntuYigini
        
        if i % 100 == 0:
            print("Egitim Süresi: ",i, " Oyun Skoru: ",Cevre.OyunSkor)
            EgitimGecmisDepolama.append(Cevre.OyunSkor)

#Egitimi başlat
Egitim()  
