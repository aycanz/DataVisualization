
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#random olarak veri seti oluşturuyorum
np.random.seed(0)
var1 = np.random.choice([10,20, 25, 26, 28, 29, 30, 32, 33, 37, 56], size=100)
var2 = np.random.choice([12,20, 25, 26, 28, 29, 30, 32, 48, 37, 56], size=100)
var3 = np.random.choice([20, 25, 26, 28, 29, 30, 32, 33, 37, 56], size=100)

dt = pd.DataFrame({'Değişken1': var1, 'Değişken2': var2, 'Değişken3': var3})

# Veri setini csv olarak kaydediyorum veriseti yerine dt olarak adlandırdım dosyayı
#print(dt)
dt.to_csv('veriseti.csv', index=False)

# Veri setini okuyorum
dt = pd.read_csv('veriseti.csv')

# Veriyi tek bir liste haline getirdim sıralayabilmek için
data = dt.values.flatten()

#veri uzunluğu bulan fonksiyon
def uzunlukbul(dizi):
    count = 0
    for _ in dizi:
        count += 1
    return count
#toplama yapan fonksiyon
def topla(dizi):
    total = 0
    for num in dizi:
        total += num
    return total
#enbuyuk degeri bulan fonksiton
def enbuyuk(arr):
    current_max = arr[0]  # Başlangıçta ilk elemanı en büyük olarak kabul ediyoruz
    for item in arr:
        if item > current_max:
            current_max = item
    return current_max

# datayı sıralıyorum
def bubble_sort(arr):
    n = uzunlukbul(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

siralanmisData = bubble_sort(data)

# Q1 ve Q3'ü hesaplıyorum
n = uzunlukbul(siralanmisData)
q1index = int(n * 0.25)
q3index = int(n * 0.75)
Q1 = siralanmisData[q1index]
Q3 = siralanmisData[q3index]

# IQR hesaplıyorum
IQR = Q3 - Q1

# Alt ve üst sınırlarını hesapladım
altLimit = Q1 - 1.5 * IQR
ustLimit = Q3 + 1.5 * IQR

# Aykırı değerleri belirliyorum
outliers = dt[(dt < altLimit) | (dt > ustLimit)] #her bir hücre için True veya False değerleri içeren bir DataFrame elde edilir
print("Aykırı Değerlerin Olduğu Satırlar:")
print(outliers)

#matplotlib kütüphanesiyle kutumu çizdiriyorum
plt.figure(figsize=(10, 6))
sns.boxplot(data=dt, orient='h', fliersize=5, linewidth=1)
plt.show()

# Merkezi eğilim ölçümleri için fonksiyonlar
def aritmetik_ortalama(veri):
    return topla(veri) / uzunlukbul(veri)

def ortanca(veri):
    siralanmisData  = bubble_sort(veri)
    n = uzunlukbul(siralanmisData )
    if n % 2 == 1:
        return siralanmisData [n // 2]
    else:
        return (siralanmisData [n // 2 - 1] + siralanmisData [n // 2]) / 2

def tepe_deger(veri):
    frekanslar = {}
    for i in veri:
        if i in frekanslar:
            frekanslar[i] += 1
        else:
            frekanslar[i] = 1
    enyuksekfrekans = max(frekanslar.values())
    return [i for i in frekanslar if frekanslar[i] == enyuksekfrekans][0]

# Merkezi dağılım ölçümleri
def deger_araligi(veri):
    current_max = veri[0]
    current_min = veri[0]
    for j in veri:
        if j > current_max:
            current_max = j
        if j < current_min:
            current_min = j
    return current_max - current_min

def ortalama_mutlak_sapma(veri):
    ortalama = aritmetik_ortalama(veri)
    return topla(abs(x - ortalama) for x in veri) / uzunlukbul(veri)#abs mutlak değer döndürüyor

def varyans(veri):
    ortalama = aritmetik_ortalama(veri)
    return topla((x - ortalama) ** 2 for x in veri) / (uzunlukbul(veri) - 1)

def standart_sapma(veri):
    return varyans(veri) ** 0.5

def degisim_katsayisi(veri):
    ortalama = aritmetik_ortalama(veri)
    std_sapma = standart_sapma(veri)
    return std_sapma / ortalama

def ceyrekler_acikligi(veri):
    siralanmisData = bubble_sort(veri)
    n = uzunlukbul(siralanmisData)
    q1index = int(n * 0.25)
    q3index = int(n * 0.75)
    q1 = siralanmisData[q1index]
    q3 = siralanmisData[q3index]
    return q3 - q1

# Her bir değişken için hesaplamaları yap
sonuclar = []
for column in dt.columns:
    veri = dt[column]
    sonuc = {
        'Degisken': column,
        'Aritmetik Ortalama': aritmetik_ortalama(veri),
        'Ortanca (Medyan)': ortanca(veri),
        'Tepe Deger (Mod)': tepe_deger(veri),
        'Deger Araligi': deger_araligi(veri),
        'Ortalama Mutlak Sapma': ortalama_mutlak_sapma(veri),
        'Varyans': varyans(veri),
        'Standart Sapma': standart_sapma(veri),
        'Degisim Katsayisi': degisim_katsayisi(veri),
        'Ceyrekler Acikligi': ceyrekler_acikligi(veri)
    }
    sonuclar.append(sonuc)

# Sonuçları ekrana yazdırdım
for sonuc in sonuclar:
    print(sonuc)

# Sonuçları dosyaya yazdırdım
with open('sonuc.txt', 'w') as dosya:
    for sonuc in sonuclar:
        dosya.write(str(sonuc) + '\n')

