from math import log2

# Veri seti
veri = [
    ["Yüksek", "Yüksek", "İşveren", "Kötü"],
    ["Yüksek", "Yüksek", "Ücretli", "Kötü"],
    ["Yüksek", "Düşük" , "Ücretli", "Kötü"],
    ["Düşük" , "Düşük" , "Ücretli", "İyi" ],
    ["Düşük" , "Düşük" , "İşveren", "Kötü"],
    ["Düşük" , "Yüksek", "İşveren", "İyi" ],
    ["Düşük" , "Yüksek", "Ücretli", "İyi" ],
    ["Düşük" , "Düşük" , "Ücretli", "İyi" ],
    ["Düşük" , "Düşük" , "İşveren", "Kötü"],
    ["Düşük" , "Yüksek", "İşveren", "İyi" ],
]

# sutun adlari
sutun_adlari = ["Borç", "Gelir", "Statü", "Risk"]

# Entropi hesaplama 
def entropi_hesapla(degerler):
    toplam = len(degerler)
    if toplam == 0:
        return 0

    sayilar = {}
    for deger in degerler:
        if deger not in sayilar:
            sayilar[deger] = 1
        else:
            sayilar[deger] += 1

    entropi = 0
    for sayi in sayilar.values():
        olasilik = sayi / toplam
        entropi -= olasilik * log2(olasilik)

    return entropi

# Bilgi kazancı hesaplama
def kazanc_hesapla(veri, ozellik_indeksi, hedef_indeksi):
    print("---------------------Kazanc hesapla başla---------------------\n")
    hedef_degerleri = [satir[hedef_indeksi] for satir in veri] #قيم الهدف لحساب الاحصاء 
    print("Hedef degerleri:",hedef_degerleri)
    hedef_entropisi = entropi_hesapla(hedef_degerleri) #قيمة الاحصاء للهدف
    print("hedef entropisi:",hedef_entropisi)

    ozellik_degerleri = [satir[ozellik_indeksi] for satir in veri] #sicaklık قيم
    print("özellik degerleri:",ozellik_degerleri)
    benzersiz_ozellik_degerleri = set(ozellik_degerleri)# كم قيمة متواجدة في العمود من دون تكرار
    print("benzersiz", benzersiz_ozellik_degerleri)

    ozellik_entropisi = 0 # حساب قيمة الاحصاء لكل عمود بداية
    for deger in benzersiz_ozellik_degerleri:
        alt_kume = [satir[hedef_indeksi] for satir in veri if satir[ozellik_indeksi] == deger]
        print(f"alt küme degerleri  {deger} için :",alt_kume)
        alt_kume_entropisi = entropi_hesapla(alt_kume)
        print(f"alt küme degerleri  {deger} için entropi :",entropi_hesapla(alt_kume))
        agirlik = len(alt_kume) / len(veri) #olasılık deger / tum degerler 
        ozellik_entropisi += agirlik * alt_kume_entropisi
        print("özellik entropisi :" ,ozellik_entropisi)

    # Kazancı hesapla
    kazanc = hedef_entropisi - ozellik_entropisi
    print("kazanç :" ,kazanc)
    print("---------------------Kazanc hesapla bitiş---------------------\n")
    return kazanc

# Karar agacinı olustur
def karar_agaci_olustur(veri, sutun_adlari):
    print("---------------------karar ağacı oluştur---------------------\n")
    hedef_indeksi = len(sutun_adlari) - 1 # ما هو عمود الهدف 
    print("hedef index :",hedef_indeksi)
    def agac_olustur(veri, sutun_adlari):
        print("---------------------ağacı oluşturuluyor---------------------\n")
        hedef_degerleri = [satir[hedef_indeksi] for satir in veri] # جميع قيم الهدف الموجودة في عمود الهدف
        print("hedef degerleri:",hedef_degerleri)

        # Tüm hedef degerleri aynı ise, bu bir yaprak düğümüdür
        if len(set(hedef_degerleri)) == 1: 
            return hedef_degerleri[0]

        # En iyi bölme ozelliğini bul
        kazanclar = [kazanc_hesapla(veri, i, hedef_indeksi) for i in range(len(sutun_adlari) - 1)]
        print("kazançlar :",kazanclar)
        en_iyi_ozellik_indeksi = kazanclar.index(max(kazanclar))
        print("en iyi özellik index :",en_iyi_ozellik_indeksi)

        en_iyi_ozellik_adi = sutun_adlari[en_iyi_ozellik_indeksi]
        print("en iyi özellik adı :",en_iyi_ozellik_adi)
        agac = {en_iyi_ozellik_adi: {}}
        print(agac)

        # En iyi ozellikten türetilen alt veri kumelerini olustur
        benzersiz_ozellik_degerleri = set([satir[en_iyi_ozellik_indeksi] for satir in veri])
        print("benzersiz özellik degerleri :",benzersiz_ozellik_degerleri)
        for deger in benzersiz_ozellik_degerleri:
            
            alt_kume = [satir for satir in veri if satir[en_iyi_ozellik_indeksi] == deger]
            print("alt küme :",alt_kume)
        
            alt_agac = agac_olustur(alt_kume, sutun_adlari)
            print("alt agaç :",alt_agac)
            
            agac[en_iyi_ozellik_adi][deger] = alt_agac
        print("agaç son :",agac)
        
        print("---------------------ağacı oluşturuldu---------------------\n")
        return agac
    
    return "agaç oluştur :",agac_olustur(veri, sutun_adlari),print("---------------------karar ağacı oluşturulmuş---------------------\n")

# Karar ağaçını oluştur
karar_agaci = karar_agaci_olustur(veri, sutun_adlari)
print("---------------------------------------------------------------")
