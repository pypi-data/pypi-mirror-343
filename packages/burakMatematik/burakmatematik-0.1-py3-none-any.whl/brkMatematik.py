# BurakMatematik.py

def topla(a, b):
    return a + b

def cikar(a, b):
    return a - b

def carp(a, b):
    return a * b

def bol(a, b):
    if b == 0:
        raise ValueError("Bir sayı sıfıra bölünemez!")
    return a / b

def faktoriyel(n):
    if n < 0:
        raise ValueError("Negatif sayıların faktöriyeli yoktur!")
    sonuc = 1
    for i in range(1, n + 1):
        sonuc *= i
    return sonuc

def asal_mi(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def ebob(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def ekok(a, b):
    return abs(a * b) // ebob(a, b)
