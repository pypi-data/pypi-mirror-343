def topla(a, b): return a + b
def cikar(a, b): return a - b
def carp(a, b): return a * b

def bol(a, b):
    if b == 0: raise ValueError("Bir sayı sıfıra bölünemez!")
    return a / b

def tam_sayi_bolme(a, b):
    if b == 0: raise ValueError("Bir sayı sıfıra bölünemez!")
    return a // b

def kalan(a, b):
    if b == 0: raise ValueError("Sıfıra bölümün kalanı tanımsızdır!")
    return a % b

def us_alma(taban, kuvvet):
    if kuvvet < 0: raise ValueError("Negatif üsler bu basit fonksiyonda desteklenmemektedir.")
    sonuc = 1
    for _ in range(kuvvet): sonuc *= taban
    return sonuc

def kare(sayi): return us_alma(sayi, 2)
def kup(sayi): return us_alma(sayi, 3)

def faktoriyel(n):
    if n < 0: raise ValueError("Negatif sayıların faktöriyeli yoktur!")
    sonuc = 1
    for i in range(1, n + 1): sonuc *= i
    return sonuc

def mutlak_deger(sayi): return -sayi if sayi < 0 else sayi

def isaret(sayi):
    if sayi > 0: return 1
    elif sayi < 0: return -1
    else: return 0

def ebob(a, b):
    while b: a, b = b, a % b
    return a

def ekok(a, b): return abs(a * b) // ebob(a, b)

def asal_mi(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def sonraki_asal(n):
    sayi = n + 1
    while not asal_mi(sayi): sayi += 1
    return sayi

def önceki_asal(n):
    if n <= 2: raise ValueError("2'den küçük sayılar için önceki asal sayı tanımsızdır.")
    sayi = n - 1
    while not asal_mi(sayi): sayi -= 1
    return sayi

def asal_carpanlar(n):
    carpanlar = []
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            carpanlar.append(d)
            temp //= d
        d += 1
    if temp > 1: carpanlar.append(temp)
    return carpanlar

def tam_bölenler(n): return [i for i in range(1, abs(n) + 1) if n % i == 0]

def toplam_kareler(n): return sum(kare(i) for i in range(1, n + 1))
def toplam_kup(n): return sum(kup(i) for i in range(1, n + 1))

def aritmetik_ortalama(liste):
    if not liste: raise ValueError("Boş liste için ortalama hesaplanamaz.")
    return sum(liste) / len(liste)

def geometrik_ortalama(liste):
    if not liste: raise ValueError("Boş liste için ortalama hesaplanamaz.")
    carpim = 1
    for sayi in liste:
        if sayi < 0: raise ValueError("Negatif sayılarla geometrik ortalama hesaplanamaz.")
        carpim *= sayi
    return us_alma(carpim, 1 / len(liste))

def harmonik_ortalama(liste):
    if not liste: raise ValueError("Boş liste için ortalama hesaplanamaz.")
    toplam = 0
    for sayi in liste:
        if sayi == 0: raise ValueError("Sıfır içeren liste için harmonik ortalama hesaplanamaz.")
        toplam += 1 / sayi
    return len(liste) / toplam

def maksimum(liste):
    if not liste: raise ValueError("Boş listenin maksimumu bulunamaz.")
    return max(liste)

def minimum(liste):
    if not liste: raise ValueError("Boş listenin minimumu bulunamaz.")
    return min(liste)

def dizi_toplami(baslangic, bitis, artis=1): return sum(range(baslangic, bitis + 1, artis))

def karekok_yaklasik(sayi, iterasyon=10):
    if sayi < 0: raise ValueError("Negatif sayının karekökü reel sayılarda yoktur.")
    if sayi == 0: return 0
    tahmin = sayi / 2
    for _ in range(iterasyon): tahmin = 0.5 * (tahmin + sayi / tahmin)
    return tahmin

def logaritma_2_tabaninda_yaklasik(sayi, iterasyon=20):
    if sayi <= 0: raise ValueError("Pozitif sayı girin.")
    sonuc = 0
    while sayi >= 2:
        sayi /= 2
        sonuc += 1
    x = sayi - 1
    terim = x
    toplam = terim
    for n in range(2, iterasyon + 1):
        terim *= -x * (n - 1) / n
        toplam += terim
    return sonuc + toplam / (2 ** 0.693)  # ln(2) yaklaşık değeri ile düzeltme

def fibonacci_sayisi(n):
    if n < 0: raise ValueError("Negatif indis geçersiz.")
    elif n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_dizisi(n): return [fibonacci_sayisi(i) for i in range(n)]

def kombinasyon(n, k):
    if k < 0 or k > n: raise ValueError("Geçersiz girdi.")
    if k == 0 or k == n: return 1
    if k > n // 2: k = n - k
    sonuc = 1
    for i in range(k):
        sonuc = sonuc * (n - i) // (i + 1)
    return sonuc

def permütasyon(n, k):
    if k < 0 or k > n: raise ValueError("Geçersiz girdi.")
    sonuc = 1
    for i in range(k): sonuc *= (n - i)
    return sonuc

def toplam_basamak(sayi): return sum(int(basamak) for basamak in str(abs(sayi)))
def basamak_sayisi(sayi): return len(str(abs(sayi)))
def sayi_ters_cevir(sayi): return int(str(abs(sayi))[::-1]) * (-1 if sayi < 0 else 1)
def palindrom_mu(sayi): return sayi == sayi_ters_cevir(sayi)

def ortanca(liste):
    sirali_liste = sorted(liste)
    n = len(sirali_liste)
    if n % 2 == 1:
        return sirali_liste[n // 2]
    else:
        return (sirali_liste[n // 2 - 1] + sirali_liste[n // 2]) / 2

def varyans(liste):
    n = len(liste)
    if n < 2: raise ValueError("Varyans için en az iki elemanlı bir liste gerekir.")
    ortalama = aritmetik_ortalama(liste)
    kare_farklar_toplami = sum((x - ortalama) ** 2 for x in liste)
    return kare_farklar_toplami / (n - 1)  # Örneklem varyansı

def standart_sapma(liste): return karekok_yaklasik(varyans(liste))

def en_buyuk_ortak_bolen_coklu(sayilar):
    if not sayilar: raise ValueError("Boş liste için EBOB tanımsızdır.")
    ebob_deger = sayilar[0]
    for i in range(1, len(sayilar)): ebob_deger = ebob(ebob_deger, sayilar[i])
    return ebob_deger

def en_kucuk_ortak_kat_coklu(sayilar):
    if not sayilar: raise ValueError("Boş liste için EKOK tanımsızdır.")
    ekok_deger = sayilar[0]
    for i in range(1, len(sayilar)): ekok_deger = ekok(ekok_deger, sayilar[i])
    return ekok_deger

def kuvvet_var_mi(sayi, kuvvet):
    if sayi == 0: return kuvvet == 0
    if kuvvet == 0: return sayi == 1 or sayi == -1
    if kuvvet < 0: return False  # Sadece pozitif tam sayı kuvvetleri kontrol eder
    temp = 1
    while abs(temp) < abs(sayi): temp *= kuvvet
    return temp == sayi

def tam_kare_mi(sayi):
    if sayi < 0: return False
    if sayi == 0: return True
    kok = int(karekok_yaklasik(sayi))
    return kok * kok == sayi

def tam_kup_mu(sayi):
    if sayi == 0: return True
    isaret = 1 if sayi > 0 else -1
    mutlak_sayi = abs(sayi)
    kok = round(mutlak_sayi ** (1/3))
    return isaret * kok * kok * kok == sayi

def basamaklarin_kupleri_toplami(sayi): return sum(kup(int(basamak)) for basamak in str(abs(sayi)))
def armstrong_sayisi_mi(sayi): return toplam_basamak_uslu(sayi, basamak_sayisi(sayi)) == abs(sayi)

def toplam_basamak_uslu(sayi, us): return sum(int(basamak)**us for basamak in str(abs(sayi)))

def mukemmel_sayi_mi(sayi):
    if sayi <= 1: return False
    return sum(i for i in range(1, sayi) if sayi % i == 0) == sayi

def dost_sayilar_mi(sayi1, sayi2):
    if sayi1 <= 1 or sayi2 <= 1 or sayi1 == sayi2: return False
    def bolenler_toplami(n): return sum(i for i in range(1, n) if n % i == 0)
    return bolenler_toplami(sayi1) == sayi2 and bolenler_toplami(sayi2) == sayi1

def basamaklarin_carpimi(sayi):
    carpim = 1
    sayi = abs(sayi)
    if sayi == 0: return 0
    while sayi > 0:
        carpim *= sayi % 10
        sayi //= 10
    return carpim

def euler_totient(n):
    if n == 1: return 1
    sonuc = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0: n //= p
            sonuc -= sonuc // p
        p += 1
    if n > 1: sonuc -= sonuc // n
    return sonuc

def pi_sayisi_yaklasik(terim=1000):
    sonuc = 0
    isaret = 1
    for i in range(terim):
        sonuc += isaret / (2 * i + 1)
        isaret *= -1
    return 4 * sonuc

def faktoriyel_hesapla(n):
    if n < 0: raise ValueError("Negatif sayının faktöriyeli olmaz.")
    elif n == 0: return 1
    else:
        sonuc = 1
        for i in range(1, n + 1): sonuc *= i
        return sonuc

def us_alma_pozitif(taban, kuvvet):
    if kuvvet < 0: raise ValueError("Negatif kuvvet desteklenmiyor.")
    sonuc = 1
    for _ in range(kuvvet): sonuc *= taban
    return sonuc

def sinüs_yaklasik(x, terim=15):
    sonuc = 0
    isaret = 1
    for n in range(terim):
        pay = us_alma_pozitif(x, 2 * n + 1)
        payda = faktoriyel_hesapla(2 * n + 1)
        sonuc += isaret * pay / payda
        isaret *= -1
    return sonuc

def kosinüs_yaklasik(x, terim=15):
    sonuc = 0
    isaret = 1
    for n in range(terim):
        pay = us_alma_pozitif(x, 2 * n)
        payda = faktoriyel_hesapla(2 * n)
        sonuc += isaret * pay / payda
        isaret *= -1
    return sonuc

def tanjant_yaklasik(x, terim=10):
    pay = sinüs_yaklasik(x, terim)
    payda = kosinüs_yaklasik(x, terim)
    if abs(payda) < 1e-9: return float('inf') if pay > 0 else float('-inf')
    return pay / payda

def arcsinüs_yaklasik(x, terim=15):
    if not -1 <= x <= 1: raise ValueError("arcsinüs için girdi [-1, 1] aralığında olmalıdır.")
    sonuc = x
    for n in range(1, terim):
        pay_ust = faktoriyel(2 * n - 1)
        pay_alt = faktoriyel(2 * n)
        payda = 2 * n + 1
        sonuc += (pay_ust / pay_alt) * (us_alma_pozitif(x, 2 * n + 1) / payda)
    return sonuc

def arkkosinüs_yaklasik(x, terim=15):
    pi_yarisi = pi_sayisi_yaklasik(terim * 2) / 2
    return pi_yarisi - arcsinüs_yaklasik(x, terim)

def arktanjant_yaklasik(x, terim=15):
    sonuc = 0
    isaret = 1
    for n in range(terim):
        sonuc += isaret * (us_alma_pozitif(x, 2 * n + 1) / (2 * n + 1))
        isaret *= -1
    return sonuc

def derece_radyan(derece): return derece * pi_sayisi_yaklasik(50) / 180
def radyan_derece(radyan): return radyan * 180 / pi_sayisi_yaklasik(50)

def faktoriyel_cift(n):
    if n < 0: raise ValueError("Negatif girdi!")
    if n == 0 or n == 1: return 1
    sonuc = 1
    for i in range(n, 0, -2): sonuc *= i
    return sonuc

def faktoriyel_tek(n):
    if n < 0: raise ValueError("Negatif girdi!")
    if n == 0: return 1
    sonuc = 1
    for i in range(n, 0, -2): sonuc *= i
    return sonuc