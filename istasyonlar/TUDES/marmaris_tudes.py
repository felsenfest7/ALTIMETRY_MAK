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
path1 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MARMARİS/MARMARİS_15DK/27_6_2009-27_6_2014.txt" #15dk
path2 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MARMARİS/MARMARİS_15DK/27_6_2014-27_6_2019.txt" #15dk
path3 = "/home/furkan/deus/ALTIMETRY/processler/TUDES/TUDES_İSTASYONLAR/MARMARİS/MARMARİS_15DK/27_6_2019-13_11_2019.txt" #15dk

#Dataframelerin oluşturulması
df1 = ft.read_tudes(path1)
df2 = ft.read_tudes(path2)
df3 = ft.read_tudes(path3)

#15 dakikalık verilerin birleştirilmesi
frames_15dk = [df1, df2, df3]
df_15dk_merged = ft.tudes15dk_birlestir(frames_15dk)    #15 DAKİKA HAM VERİ

#15 dakikalık verilere IQR uygulanması
df_15dk_merged_iqr = ft.tudes15dk_iqr(df_15dk_merged)   #0 olan DETREND değerlerinin alınacağı yer
                                                        #1 olan IQR SONRASI SSH değerlerinin alınacağı ve diğer fonklara sokulacak df

#15 dakikalık verilerin saatlik hale getirilmesi
df_15_saatlik = ft.tudes15_saatlik(df_15dk_merged_iqr[1])

#Saatlik verilere IQR uygulanması
df_saatlik_iqr = ft.tudes60dk_iqr(df_15_saatlik)       #0 olan DETREND değerlerinin alınacağı yer
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
grafikler = pf.plot_digerleri_tudes(df_15dk_merged_iqr[0], df_15dk_merged_iqr[1], df_saatlik_iqr[0], df_saatlik_iqr[1], df_gunluk_iqr[0], df_gunluk_iqr[1], df_aylik_iqr[0], df_aylik_iqr[1], "Marmaris")
df_ekksa_grafik = pf.plot_ekksa_tudes(df_ekksa[1], "Marmaris", df_ekksa[2], df_ekksa[3], 2018, 8, 1, 0.29)

print(df_ekksa[0])










