import pygame as PY
import random
import pygame.draw as Ciz
import pygame.display as Goruntule
import pygame.event as Olay
import pygame.surfarray as DiziEkran
import pygame.font as YaziTipi
#Ekrenın ve oyunun genişliğini,yuksekligini tanımlama
EkranGenisligi = 400
EkranYuksekligi = 500
OyunYuksekligi = 400

#Raketlerin genislik yukseklik ve tamponunu tanımlama
RaketGenisligi = 15
RaketYuksekligi = 60
RaketAraligi = 15

# Topun genisligini ve yuksekligini tnaımla
TopGenisligi = 20
TopYuksekligi = 20

#Top ve Raketlerin hızlarını belirleme
RaketHareketHizi = 3
TopXEksendeHizi = 2
TopYEksendeHizi = 2

#Oyun ekranı ve raketleri için RGB renkler
RGBBeyazRenk = (255,255,255)
RGBSiyahRenk = (0,0,0)

#Skorların ekranda gözüken yazı tipi
YaziFontu = YaziTipi.match_font('arial')

OyunEkrani = Goruntule.set_mode((EkranGenisligi,EkranYuksekligi))

#Ekrana Raket çizdirme Fonksiyonu
def RaketOlustur(RaketTipi, RaketYEkseni):
    
    #hangi raketin cizilmesi gerektigini kontrol etmek için if komutu yap ve ona göre sag ve solda raketleri çizdir
    if RaketTipi == "Ajan":
        Raket = PY.Rect(RaketAraligi, RaketYEkseni, RaketGenisligi, RaketYuksekligi)
    elif RaketTipi == "Normal":
        Raket = PY.Rect(EkranGenisligi - RaketAraligi - RaketGenisligi, RaketYEkseni, RaketGenisligi, RaketYuksekligi)
        
    Ciz.rect(OyunEkrani, RGBBeyazRenk, Raket)
 
#Topun ekranda görüntelenmesi için çizen fonksiyon
def TopOlustur(TopXEkseni, TopYEkseni):
    
    Top = PY.Rect(TopXEkseni, TopYEkseni, TopGenisligi, TopYuksekligi)
    
    Ciz.rect(OyunEkrani, RGBBeyazRenk, Top)

#Ekranda raketlerin topu yakalayıp yakalayamadıklarını ekran gösteren fonksiyon
def SkorYazdir(Ekran,Yazi,switch):
    FontOlustur = PY.font.Font(YaziFontu,40)
    YaziIcerik = FontOlustur.render(Yazi,True,RGBBeyazRenk)
    YaziAlani = YaziIcerik.get_rect()
    if switch == 0:    
        YaziAlani.midtop = (EkranGenisligi/4,OyunYuksekligi + (EkranYuksekligi-OyunYuksekligi)/2)
    else:
        YaziAlani.midtop = (EkranGenisligi/2 + EkranGenisligi/4,OyunYuksekligi + (EkranYuksekligi-OyunYuksekligi)/2)
    Ekran.blit(YaziIcerik, YaziAlani)
    
    
#Raketlerin konumu guncelleme
def RaketGuncelle(RaketTipi, Aksiyon , RaketYEkseni, TopXEkseni):
    DeltaZaman = 7.5 
   
    #ajan raket için aldığı aksiyonlara göre konumunu güncelle
    if RaketTipi == "Ajan":
        if Aksiyon == 1:
            RaketYEkseni = RaketYEkseni - RaketHareketHizi*DeltaZaman
        if Aksiyon == 2:
            RaketYEkseni = RaketYEkseni + RaketHareketHizi*DeltaZaman
            
        if RaketYEkseni < 0:
            RaketYEkseni = 0
        if RaketYEkseni > OyunYuksekligi - RaketYuksekligi:
            RaketYEkseni = OyunYuksekligi - RaketYuksekligi
    #normal raket için topun takibini sağlayacak sekilde konum guncelle
    elif RaketTipi == "Normal":
        if RaketYEkseni + RaketYuksekligi/2 < TopXEkseni + TopYuksekligi/2:
            RaketYEkseni = RaketYEkseni + RaketHareketHizi*DeltaZaman
        if RaketYEkseni + RaketYuksekligi/2 > TopXEkseni + TopYuksekligi/2:
            RaketYEkseni = RaketYEkseni - RaketHareketHizi*DeltaZaman   
            
        if RaketYEkseni < 0:
            RaketYEkseni = 0
        if RaketYEkseni > OyunYuksekligi - RaketYuksekligi:
            RaketYEkseni = OyunYuksekligi - RaketYuksekligi
    return RaketYEkseni

#Raketlerin konumu guncelleme
def TopGuncelle(AjanRaketYEkseni, NormalRaketYEkseni, TopXEkseni, TopYEkseni, TopXYonu, TopYYonu):
    
    dft = 7.5
    
    TopXEkseni = TopXEkseni + TopXYonu*TopXEksendeHizi*dft
    TopYEkseni = TopYEkseni + TopYYonu*TopYEksendeHizi*dft
    
    YasamCezasi = -0.05
    # agent
    if (TopXEkseni <= (RaketAraligi + RaketGenisligi + TopGenisligi/2)) and ((TopYEkseni + TopYuksekligi -1) >= AjanRaketYEkseni) and ((TopYEkseni-1) <= (AjanRaketYEkseni + RaketYuksekligi)) and (TopXYonu == -1):
        TopXYonu = 1 
        
        YasamCezasi = 10
        
    elif (TopXEkseni <= TopGenisligi/2):
        
        TopXYonu = 1
        
        YasamCezasi = -10 
        
        return [YasamCezasi, TopXEkseni ,TopYEkseni ,TopXYonu, TopYYonu]
    
    if (TopXEkseni >= (EkranGenisligi - RaketGenisligi - RaketAraligi - TopGenisligi)) and ((TopYEkseni + TopYuksekligi)>= NormalRaketYEkseni) and (TopYEkseni <= (NormalRaketYEkseni + RaketYuksekligi)) and (TopXYonu == 1):
        
        TopXYonu = -1
    
    elif(TopXEkseni >= EkranGenisligi - TopGenisligi):
        
        TopXYonu = -1
        YasamCezasi = 0.05
        return [YasamCezasi, TopXEkseni,TopYEkseni, TopXYonu, TopYYonu]
    
    if TopYEkseni <= 0:
        
        TopYEkseni = 0
        
        TopYYonu = 1
        
    elif TopYEkseni >= OyunYuksekligi - TopYuksekligi:
        
        TopYEkseni = OyunYuksekligi - TopYuksekligi
        
        TopYYonu = -1
        
    return [YasamCezasi, TopXEkseni,TopYEkseni,TopXYonu,TopYYonu]
    
    
class PongOyunu:
    
    def __init__(self):
        PY.init()
        Goruntule.set_caption("Pong Oyunu")
        
        self.AjanRaketYEkseni = OyunYuksekligi/2 - RaketYuksekligi/2
        self.NormalRaketYEkseni = OyunYuksekligi/2 - RaketYuksekligi/2
        
        self.AjanSkor = 0
        self.NormalSkor = 0
        self.OyunSkor = 0.0
        
        self.TopXYonu = random.sample([-1,1],1)[0]
        self.TopYYonu = random.sample([-1,1],1)[0]
        
        self.TopXEkseni = EkranGenisligi/2
        self.TopYEkseni = random.randint(0,9)*(EkranYuksekligi - TopYuksekligi)/9
        
        
    def EkrandaGoruntuOlustur(self):
        
        Olay.pump()
        
        OyunEkrani.fill(RGBSiyahRenk)
        
        RaketOlustur("Ajan", self.AjanRaketYEkseni)
        RaketOlustur("Normal",self.NormalRaketYEkseni)
        
        TopOlustur(self.TopXEkseni, self.TopYEkseni)
        
        Goruntule.flip()
    
    def HareketEttir(self, Aksiyon):
        
        Olay.pump()
        
        Skor = 0
        
        OyunEkrani.fill(RGBSiyahRenk)
        
        self.AjanRaketYEkseni = RaketGuncelle("Ajan", Aksiyon, self.AjanRaketYEkseni, self.TopYEkseni)
        RaketOlustur("Ajan", self.AjanRaketYEkseni)

        self.NormalRaketYEkseni = RaketGuncelle("Normal", Aksiyon, self.NormalRaketYEkseni, self.TopYEkseni)
        RaketOlustur("Normal", self.NormalRaketYEkseni)
        
        [Skor, self.TopXEkseni, self.TopYEkseni, self.TopXYonu, self.TopYYonu] = TopGuncelle(self.AjanRaketYEkseni, self.NormalRaketYEkseni, self.TopXEkseni, self.TopYEkseni, self.TopXYonu, self.TopYYonu)
        
        TopOlustur(self.TopXEkseni, self.TopYEkseni)
        
        if Skor == 0.05:
            self.AjanSkor +=1
        if Skor == -10:
            self.NormalSkor +=1
            
        if ( Skor > 0.5 or Skor < -0.5):
            self.OyunSkor = self.OyunSkor*0.9 + 0.1*Skor 
            
        EkranGoruntusu = DiziEkran.array3d(Goruntule.get_surface())
        SkorYazdir(OyunEkrani,str(self.AjanSkor),0)
        SkorYazdir(OyunEkrani,str(self.NormalSkor),1)
        Goruntule.flip()
        
        return [Skor, EkranGoruntusu]
