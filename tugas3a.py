# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 09:50:05 2025

@author: IPT
"""
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import random
import math
import numpy as np
import tracemalloc

def merge_sort(arr):
    """
    Fungsi utama Merge Sort yang rekursif.
    """
    # === BASIS REKURSI (Base Case) ===
    # Jika list memiliki 0 atau 1 elemen, list tersebut sudah terurut.
    if len(arr) <= 1:
        return arr

    # === LANGKAH REKURSI (Recursive Step) ===
    
    # 1. Divide (Bagi)
    # Temukan titik tengah list
    tengah = len(arr) // 2
    
    # Bagi list menjadi dua bagian: kiri dan kanan
    # (Slicing list seperti ini membuat salinan baru)
    kiri = arr[:tengah]
    kanan = arr[tengah:]

    # 2. Conquer (Taklukkan)
    # Panggil merge_sort secara rekursif untuk kedua bagian
    kiri_terurut = merge_sort(kiri)
    kanan_terurut = merge_sort(kanan)

    # 3. Combine (Gabungkan)
    # Gabungkan kedua bagian yang sudah terurut
    return merge(kiri_terurut, kanan_terurut)


def merge(kiri, kanan):
    """
    Fungsi untuk menggabungkan dua list (kiri dan kanan) 
    yang sudah terurut.
    """
    hasil = []
    indeks_kiri = 0
    indeks_kanan = 0

    # Loop selama kedua list masih memiliki elemen untuk dibandingkan
    while indeks_kiri < len(kiri) and indeks_kanan < len(kanan):
        # Bandingkan elemen pertama dari kedua list
        if kiri[indeks_kiri] < kanan[indeks_kanan]:
            hasil.append(kiri[indeks_kiri])
            indeks_kiri += 1
        else:
            hasil.append(kanan[indeks_kanan])
            indeks_kanan += 1

    # Setelah satu list habis, tambahkan sisa elemen dari list yang lain
    # (Hanya salah satu dari dua baris 'extend' ini yang akan berjalan)
    hasil.extend(kiri[indeks_kiri:])
    hasil.extend(kanan[indeks_kanan:])

    return hasil

n=10**4
tracemalloc.start()
list_angka = np.random.randint(0, 1000,n)
list_terurut = merge_sort(list_angka)
current, peak = tracemalloc.get_traced_memory()
# tracemalloc.get_traced_memory() returns bytes,
# so we divide by 10**6 to get megabytes (MB)
print(f"Current memory usage: {current / 10**6:.2f} MB")
print(f"Peak memory usage:    {peak / 10**6:.2f} MB")
# Stop tracking
tracemalloc.stop()