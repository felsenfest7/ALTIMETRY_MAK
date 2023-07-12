import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_MAK/functions")
import functions_tudes as ft
import plot_functions as pf
import harmonik_analiz_mak as haa
#--------------------------------------------------
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',10000)
#--------------------------------------------------
#15 ve 60dklık verilerin birleştirilerek kullanılması gerekiliyor. Çünkü veriler arası zaman farklılıkları var.
#Bunları tespit ederken ben elimle txt filedan düzelttim ve ona göre verileri düzenleyerek buraya aktardım.
path1 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ERDEK/ERDEK_60DK/16_04_1999-31_12_2003.txt" #60dk
path2 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ERDEK/ERDEK_15DK/27_06_2001-21_12_2005.txt" #15dk
path3 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ERDEK/ERDEK_15DK/21_12_2005-21_12_2010.txt" #15dk
path4 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ERDEK/ERDEK_15DK/21_12_2010-21_12_2015.txt" #15dk
path5 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/ERDEK/ERDEK_15DK/21_12_2015-13_11_2019.txt" #15dk

#Dataframelerin oluşturulması
df1 = ft.read_tudes(path1)
df2 = ft.read_tudes(path2)
df3 = ft.read_tudes(path3)
df4 = ft.read_tudes(path4)
df5 = ft.read_tudes(path5)

#15 dakikalık verilerin birleştirilmesi
frames_15dk = [df2, df3, df4, df5]
df_15dk_merged = ft.tudes15dk_birlestir(frames_15dk)    #15 DAKİKA HAM VERİ

#60 dakikalık verininde aynı formata getirilmesi
df_60dk = ft.tudes60dk_duzenle(df1)

#15 dakikalık verilere IQR uygulanması
df_15dk_merged_iqr = ft.tudes15dk_iqr(df_15dk_merged)   #0 olan DETREND değerlerinin alınacağı yer
                                                        #1 olan IQR SONRASI SSH değerlerinin alınacağı ve diğer fonklara sokulacak df

#15 dakikalık verilerin saatlik hale getirilmesi
df_15_saatlik = ft.tudes15_saatlik(df_15dk_merged_iqr[1])

#Ardından 15 ve 60 dakikalık verilerin birleştirilmesi
df_saatlik = ft.tudes_15_60_birlestir(df_60dk, df_15_saatlik)   #SAATLİK HAM VERİ

#Saatlik verilere IQR uygulanması
df_saatlik_iqr = ft.tudes60dk_iqr(df_saatlik)       #0 olan DETREND değerlerinin alınacağı yer
                                                    #1 olan IQR SONRASI SSH değerlerinin alınacağı ve diğer fonklara sokulacak df

#Günlük verilerin oluşturulması
df_gunluk = ft.tudes_gunluk(df_saatlik_iqr[1])          #GÜNLÜK HAM VERİ

#Günlük verilere IQR uygulanması
df_gunluk_iqr = ft.tudes_gunluk_iqr(df_gunluk)      #0 olan DETREND değerlerinin alınacağı yer
                                                    #1 olan IQR SONRASI SSH değerlerinin alınacağı ve diğer fonklara sokulacak df

#Aylık verilerin üretilmesi
df_aylik = ft.tudes_aylik(df_gunluk_iqr[1])         #AYLIK HAM VERİ

#Aylık verilere IQR uygulanması
df_aylik_iqr = ft.tudes_aylik_iqr(df_aylik)         #0 olan DETREND değerlerinin alınacağı yer
                                                    #1 olan IQR SONRASI SSH değerlerinin alınacağı ve diğer fonklara sokulacak df

#Bazı aylar artık gözükmüyor (veri yoktu onlarda), onları şimdi Nan yapmak gerek
df_aylik_son = ft.dates_interpolation(df_aylik_iqr[1])      #BU SPEKTRAL ANALİZE GİDECEK

#EKKSA öncesi hazırlık
df_pre_ekksa = ft.pre_ekksa_tudes(df_aylik_son)

#Harmonik analiz
df_ekksa = haa.harmonik_analiz(df_pre_ekksa)

#Grafiklerin çizdirilmesi
grafikler = pf.plot_digerleri_tudes(df_15dk_merged_iqr[0], df_15dk_merged_iqr[1], df_saatlik_iqr[0], df_saatlik_iqr[1], df_gunluk_iqr[0], df_gunluk_iqr[1], df_aylik_iqr[0], df_aylik_iqr[1], "Erdek")
df_ekksa_grafik = pf.plot_ekksa_tudes(df_ekksa[1], "Erdek", df_ekksa[2], df_ekksa[3], 2018, 5, 1, 0.57)

print(df_ekksa[0])










