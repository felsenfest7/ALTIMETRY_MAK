from netCDF4 import Dataset as dt
import xarray as xr
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import geopy.distance
import juliandate as jd
from datetime import datetime
import math as m
import scipy as sc
import geopy.distance

#-----------------------------------------------------------------------------------------------------------------------
def read_xt(data, ist_enlem, ist_boylam, delta):
    """
           --> XTRACK verilerinin okunması için oluşturulmuş fonksiyon.

           input: data olarak xtrack verisi, ist_enlem ve ist_boylam ise istasyonun koordinatlarıdır
           oytput: dataframe
    """

    # Dataset xarray kütüphanesi ile açılır
    dataset = xr.open_dataset(data, decode_times=False)
    # Ardından dataframe'e dönüştürülür
    df = dataset.to_dataframe()
    # Ardından yeni bir dataframe oluşturulur ve multiindex yapıdaki veri resetlenerek single index yapılır
    df2 = df.reset_index()

    #En yakın ölçme noktalarının bulunması
    if df2["lat"].mean() < ist_enlem:
        df2 = df2[(df2.lat > (ist_enlem - delta)) & (df2.lat < (ist_enlem))]
    elif df2["lat"].mean() > ist_enlem:
        df2 = df2[(df2.lat > (ist_enlem)) & (df2.lat < (ist_enlem + delta))]

    #NaN değerlerin elimine edilmesi --> julian date çevirimleri yaparken sıkıntıya sebebiyet veriuor çünkü
    df2 = df2.dropna(0)

    # Jülyen tarihlerini grogaryan tarihine çevirme
    ##XTRACK verileri "days since 1950-1-1" olarak tanımlanmakta ve bu tarih 2433282.50000 Jülyen tarihine gelmekte (MÖ 4713'e göre)
    # Elimdeki julian günlerini bu date ile toplarsam aslında epok kaydırma yapmış olurum, bu sayede BC 4713'e göre tarih bulurum.
    # Ardından yeni epokları gregoryana çevirebilirim
    jday4713 = [i + 2433282.50000 for i in df2["time"]]
    df2.insert(loc=21, column="jday4713", value=jday4713)

    # Calendar date'e çevirme
    cdate = [jd.to_gregorian(i) for i in df2["jday4713"]]
    df2.insert(loc=22, column="cdate", value=cdate)

    # Datetime'a çevirme
    cdate_2 = []

    for i in cdate:
        dt_obj = datetime(*i)
        x = dt_obj.strftime("%Y-%m-%d")
        cdate_2.append(x)
    df2.insert(loc=23, column="cdate_t", value=cdate_2)

    # Pandasta çalışması için şu komut girilmeli
    df2["cdate_t"] = pd.to_datetime(df2["cdate_t"])

    # İlk olarak SSH değerleri ham veride hesaplanacak
    df2["ssh"] = df2["mssh"] + df2["sla"]

    df3 = df2[["points_numbers", "cdate_t", "lat", "lon", "ssh", "mssh"]]
    df3.reset_index(drop = True, inplace = True)

    return df3
#-----------------------------------------------------------------------------------------------------------------------
def aylık_xt(df):
    """
        --> Günlük verilerden aylık veriler oluşturma
        input: df
        output: df
    """
    df = df.sort_values(by="cdate_t", ascending=True)
    df.set_index("cdate_t", inplace=True)
    df_aylık = df.resample("MS").mean()
    return df_aylık
#-----------------------------------------------------------------------------------------------------------------------
def iqr_gunluk_xt(df):
    """
        --> Günlük verileri kullanarak hem detrend hem de IQR analizi yapmayı sağlıyor.
        --> İki input döndürecek. İlkinin kullanılma amacı öncül detrend ve ssh değerlerinin alınması. Diğeri ise post detrend ve ssh değerlerinin alınmasında kullnaılıyor.

        input: df
        output: df
    """

    #Şu gereksiz column yukarıdaki fonksiyonda gitmemiş (copy  etseydim giderdi büyük ihtimal)
    df.drop(["points_numbers"], axis = 1, inplace = True)

    #Detrend hesabı
    detrended = sc.signal.detrend(df["ssh"], type = "linear")
    detrended_df = pd.DataFrame(detrended, columns = ["detrended_gunluk"])

    #Detrend series'ı ile df'in birleştirilmesi
    df_merged = pd.concat([df, detrended_df], axis = 1)     #IQR ÖNCESİ DF BU, ÇİZDİRİLECEK DETREBD GRAFİĞİ BU OLACAK   #BUNA 0 DEDİM

    #IQR analizi
    Q1 = df_merged["detrended_gunluk"].quantile(0.25)
    Q3 = df_merged["detrended_gunluk"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df_merged.query('(@Q1 - 1.5 * @IQR) <= detrended_gunluk <= (@Q3 + 1.5 * @IQR)')      #IQR SONRASI DF BU, BU DA IQR OLARAK ÇİZDİRİLECEK (SSH VE DETREND)  #BUNA 1 DEDİM

    return df_merged, filtered
#-----------------------------------------------------------------------------------------------------------------------
def iqr_aylik_xt(df):
    """
        --> Aylık verileri kullanarak hem detrend hem de IQR analizi yapmayı sağlıyor.
        --> İki input döndürecek. İlkinin kullanılma amacı öncül detrend ve ssh değerlerinin alınması. Diğeri ise post detrend ve ssh değerlerinin alınmasında kullnaılıyor.

        input: df
        output: df
        """
    #Aylık verilerin üretilmesi ve hataya sebebiyet verdiği için NaN'ların çıkarılması
    df_aylık = aylık_xt(df)
    df_aylık.dropna(axis = 0, inplace = True)

    # Detrend hesabı
    detrended = sc.signal.detrend(df_aylık["ssh"], type="linear")
    detrended_df = pd.DataFrame(detrended, columns=["detrended_aylik"])

    # Detrend series'ı ile df'in birleştirilmesi
    df_aylık.reset_index(inplace = True)    #birleşmeleri için gerekli
    df_merged = pd.concat([df_aylık, detrended_df], axis=1)  # IQR ÖNCESİ DF BU, ÇİZDİRİLECEK DETREBD GRAFİĞİ BU OLACAK   #BUNA 0 DEDİM

    # IQR analizi
    Q1 = df_merged["detrended_aylik"].quantile(0.25)
    Q3 = df_merged["detrended_aylik"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df_merged.query('(@Q1 - 1.5 * @IQR) <= detrended_aylik <= (@Q3 + 1.5 * @IQR)')  # IQR SONRASI DF BU, BU DA IQR OLARAK ÇİZDİRİLECEK (SSH VE DETREND)  #BUNA 1 DEDİM

    #Tekrardan dates interpolation
    df_merged = aylık_xt(df_merged)
    filtered = aylık_xt(filtered)

    return df_merged, filtered
#-----------------------------------------------------------------------------------------------------------------------
def pre_ekksa(df, station_date, end_date):
    """
        --> İçine atılan df'in columnlarının yalnızca bir kısmının kullanılması için oluşturulan dataframe.
        --> Ekstra bir hesap yaparak yeni bir columnda oluşturmayı hedeflemiştir.
        --> EKKSA öncesi kullanılmakta.
        --> Station date: istasyon kurulum tarihi, end_date = son tarih(random 2023 şu an)

        input: df
        output: df
        """
    #Index resetlenerek belirli bir dataframe oluşturulur
    df2 = df.reset_index()
    df3 = df2[["cdate_t", "ssh"]].copy()    #BU da o dataframe

    # YYYY.MM biriminde hesaplamaya yapabilmek için yapılan hesaplamalar
    new_date = []
    for i in df3["cdate_t"]:
        new_date.append(i.year + ((i.month - 0.5) / 12))

    # Elde edilen değerlerin virgülden sonra çok hanesi olduğu için formatlanması gerekmekte
    formatting = ["%.4f" % i for i in new_date]

    # Elde edilen listenin df'e eklenmesi
    df3["date"] = formatting

    #Zamansal olarak kısıtlanma
    df3 = df3[df3["cdate_t"] >= station_date]
    df3 = df3[df3["cdate_t"] <= end_date]
    df3.set_index("date", inplace=True)

    # Ağırlık column'unun oluşturulması
    df3["weight"] = 1

    df3.reset_index(inplace=True)
    df3.rename_axis("ay", inplace=True)

    return df3
#-----------------------------------------------------------------------------------------------------------------------
def dates_interpolation(df):
    """
        --> Aylara göre interpolasyon yapar.
        --> Sadece tarihler için geçerlidir.

        input: df
        output: df
    """
    df['cdate_t'] = pd.to_datetime(df['cdate_t'])

    df = (df.set_index('cdate_t')
          .reindex(pd.date_range(df['cdate_t'].min(), df['cdate_t'].max(), freq='MS'))
          .rename_axis(['cdate_t'])
          .fillna(np.nan)   #0 dı bu
          .reset_index())

    return df
#-----------------------------------------------------------------------------------------------------------------------
def mesafe_hesapla(ist_lat, ist_lon, alt_lat, alt_lon):
    """
        --> Mareograf istasyonu ile ölçme noktasının konum bilgilerini kullanarak mesafe hesabı yapar.
        --> Haversine formülü kullanıldı (küre üzerinde lat-lon ile mesafe hesabı).
        --> İst_lat ve ist_lon; mareograf istasyonunun enlem ve boylamı.
        --> Alt_lat ve alt_lon; altimetri ölçme noktasının enlem ve boylamı.
    """

    ist_coords = (ist_lat, ist_lon)
    alt_coords = (alt_lat, alt_lon)

    distance = geopy.distance.geodesic(ist_coords, alt_coords).km
    distance = round(distance, 3)

    print(f"Altimetri ölçme noktasının enlemi {alt_lat}, boylamı {alt_lon} ve istasyon ile aralarındaki mesafe {distance} km.")
#-----------------------------------------------------------------------------------------------------------------------
def read_bozuk_xt(data, ist_enlem, delta, station_name, mode):
    """
        --> BAZI VERİLERDE DATETİME OBJELERİ ÇEVRİLİRKEN HATA VERİYOR VE BU HATAYI DÜZELTEMİYORUM.
        --> BUNDAN DOLAYI İLGİLİ VERİLER İÇİN "BOZUK" KOD ADINDAKİ FONKSİYONLAR KULLANILMALI.
        --> AYRICA BELLİ BİR KISIMDA EXCELDE ELLE DÜZELTME GETİRMEK ZORUNDAYIM.
        --> data = verinin (nc) pathi
    """
    #Verinin okunması, dataframe'e aktarılması ve indeksinin resetlenmesi
    datam = xr.open_dataset(data, decode_times = False)
    df = datam.to_dataframe()
    df2 = df.reset_index()

    #Yeni verisetinde verileri almak
    df3 = df2.loc[:, ["points_numbers", "lat", "lon", "mssh", "sla", "time"]]

    #En yakın ölçme noktalarının bulunması
    if df3["lat"].mean() < ist_enlem:
        df3 = df3[(df3.lat > (ist_enlem - delta)) & (df3.lat < (ist_enlem))]
    elif df3["lat"].mean() > ist_enlem:
        df3 = df3[(df3.lat > (ist_enlem)) & (df3.lat < (ist_enlem + delta))]

    #NaN değerlerin droplanması
    df3 = df3.dropna(0)

    #SSH hesaplanması ve diğer column'un hesaplanması
    df3["ssh"] = df3["mssh"] + df3["sla"]
    df3 = df3.drop(columns=["sla"])

    # 1950 tarihli JD BC 4713'e kaymalı
    df3["BC4713"] = df3["time"] + 2433282.50000
    df3["x"] = [jd.to_gregorian(i) for i in df3["BC4713"]]

    # Excele atmadan önce bir takım işlemler
    df3["xx"] = [list(i) for i in df3["x"]]
    df3["Zaman"] = [i[0:3] for i in df3["xx"]]

    #Gereksiz columnları droplayalım
    df3.drop(columns=["time", "BC4713", "x", "xx"], inplace = True)

    #Excele atalım
    station_name2 = station_name.lower()
    path = f"/home/furkan/deus/ALTIMETRY_2/SONUÇLAR/{station_name}/{station_name2}_{mode}_bozuk.xlsx"
    #table = df3.to_excel(path)

    # EXCELDE ELLE NASIL AYIKLAMA YAPILACAK ?
        # --> CTRL+H İLE İLK OLARAK BRACKETLARI KALDIR ([ İLE ])
        # --> ARDINDAN İLGİLİ COLUMN'U SEÇ. DATA --> TEXT TO COLUMNS'A TIKLA MENUBARDAN
        #     BURADAN EN AŞAĞIDA TABLO HALİNDE GÖZÜKEN RESME TIKLA VE FIELD BÖLÜMÜNDEN İLGİLİ AYARI SEÇ (YMD BENDE)
        # --> SONRA İLGİLİ COLUMN'U SEÇ SAĞ TIK YAPIP FORMAT CELLS'TEN YYYY-MM-DD FORMATINA ÇEVİR
        # https://ask.libreoffice.org/t/convert-text-mm-dd-yyyy-hhss-to-date-time-yyyy-mm-dd-hh-mm/47514/2

        # DİĞER BOZUK VERİLER ELLE İMHA EDİLECKE















