import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'
desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',30)
pd.set_option('display.max_rows',4000)
#-----------------------------------------------------------------------------------------------------------------------
#Dosyanın konumu
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_MAK/functions")

import harmonik_analiz_mak as haa
import functions_xt as fxt
import plot_functions as pf
#-----------------------------------------------------------------------------------------------------------------------
#Datanın konumu ve okunması
data = "/home/furkan/deus/ALTIMETRY_2/DATA/XTRACK_DATA/MEDSEA/ctoh.sla.ref.TP+J1+J2+J3.medsea.170.nc"
dataset = fxt.read_xt(data, 36.813829885245906, 28.57312370765027, 0.20)

#Ardından kıyıya uzak ve yakın iki XTRACK altimetri ölçme noktasının belirlenmesi
dataset1 = dataset[dataset["points_numbers"] == 110]     #kıyıya yakın olan
dataset2 = dataset[dataset["points_numbers"] == 111]     #kıyıya uzak olan

#Kıyıya yakın olan ölçme noktasına ait işlemler
dataset1.reset_index(drop=True, inplace = True)     #bir tane veriseti 0 harcinde sayı ile başlıyor ve sorun veriyor, bunu çözmek için bunu kullandım
dataset1_gunluk = fxt.iqr_gunluk_xt(dataset1)
dataset1_aylık = fxt.iqr_aylik_xt(dataset1_gunluk[1])   #1'in anlamı filtered olan df
dataset1_pre_ekksa = fxt.pre_ekksa(dataset1_aylık[1], "2009-06-01", "2023-11-01")
dataset1_ekksa = haa.harmonik_analiz(dataset1_pre_ekksa)
df1, df2, df3, df4, df5 = dataset1_gunluk[0], dataset1_gunluk[1], dataset1_aylık[0], dataset1_aylık[1], dataset1_ekksa[1]
dataset1_grafikler = pf.plot_digerleri_xt(df1, df2, df3, df4, "Marmaris (Yakın)", "LRM")
dataset1_ekksa_grafik = pf.plot_ekksa_xt(df5, "Marmaris (Yakın)", dataset1_ekksa[2], dataset1_ekksa[3], 2021, 2, 1, 23.725, "LRM")

#Kıyıya uzak olan ölçme noktasına ait işlemler
dataset2.reset_index(drop=True, inplace = True)     #bir tane veriseti 0 harcinde sayı ile başlıyor ve sorun veriyor, bunu çözmek için bunu kullandım
dataset2_gunluk = fxt.iqr_gunluk_xt(dataset2)
dataset2_aylık = fxt.iqr_aylik_xt(dataset2_gunluk[1])   #1'in anlamı filtered olan df
dataset2_pre_ekksa = fxt.pre_ekksa(dataset2_aylık[1], "2009-06-01", "2023-11-01")
dataset2_ekksa = haa.harmonik_analiz(dataset2_pre_ekksa)
df6, df7, df8, df9, df10 = dataset2_gunluk[0], dataset2_gunluk[1], dataset2_aylık[0], dataset2_aylık[1], dataset2_ekksa[1]
dataset2_grafikler = pf.plot_digerleri_xt(df6, df7, df8, df9, "Marmaris (Uzak)", "LRM")
dataset2_ekksa_grafik = pf.plot_ekksa_xt(df10, "Marmaris (Uzak)", dataset2_ekksa[2], dataset2_ekksa[3], 2021, 2, 1, 24.585, "LRM")

#Mesafeler ve koordinatlar
dataset1_distance = fxt.mesafe_hesapla(36.83811118, 28.38501334, dataset1.lat.mean(), dataset1.lon.mean())
dataset2_distance = fxt.mesafe_hesapla(36.83811118, 28.38501334, dataset2.lat.mean(), dataset2.lon.mean())


print(dataset1_ekksa[0], dataset2_ekksa[0])















