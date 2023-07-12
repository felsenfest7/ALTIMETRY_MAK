import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
from numpy.linalg import inv
from matplotlib.ticker import FormatStrFormatter
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MonthLocator, YearLocator
import sys
import scipy as sc
import datetime
pd.options.mode.chained_assignment = None  # default='warn'
np.set_printoptions(threshold=sys.maxsize)
#-----------------------------------------------------------------------------------------------------------------------
def read_tudes(path):
    """
        --> Path girdi olarak girer ve ilgili mareograf istasyonu dosyası okunur.
        --> Burada ana amaç detrend ve IQR analizleri öncesinde verilerin düzenlenerek hazır hale getirilmesi.
        --> BU KOD HEM 15 HEM DE 60 DAKİKALIK VERİLER İÇİN KULLANILABİLİR.
    """
    # Verinin df ile okunması
    df = pd.read_csv(path, sep=",")

    # Bu veride gerekli olan columnları almak için
    df2 = df[["Tarih", "Deniz Seviyesi", "Deniz Seviyesi Kalite Kodu"]]
    df2.rename(columns={"Deniz Seviyesi": "Deniz_Seviyesi", "Deniz Seviyesi Kalite Kodu": "Kalite"}, inplace=True)

    # Deniz Seviyesi Kalite Kodu 0 veya 1 olabiliyor. Eğer 0'sa kalitesiz, 1'se kaliteli veri demek.
    # Kalitesiz verileri ondan dolayı elimine etcem.
    # Kalitesiz verilerde zaten SSH verileri NaN biçiminde geliyor.
    condition = df2[df2["Kalite"] == 0].index
    df2.drop(condition, inplace=True)
    df2.drop(columns=["Kalite"], inplace=True)  # Artık bunla işim kalmadı

    return df2
#-----------------------------------------------------------------------------------------------------------------------
def tudes15dk_birlestir(frames):
    """
            --> 15 dk'lık verilerin okunması için fonksiyon.
            --> 15 dk'lık veriler birleştirilir bu sayede.

            input : list
            output: df
        """
    # Verileri birleştirip indexi sıfırladı
    result = pd.concat(frames)
    result.drop_duplicates(inplace = True)
    result.reset_index(inplace=True, drop=True)

    # Verilerin tarih bilgilerinin düzeltilmesi ve IQR hesabının yapılarak birleştirilmiş 15dklık verilerin elde edilmesi
    result['Tarih'] = pd.to_datetime(result['Tarih'], format='%d.%m.%Y %H:%M:%S')  # Datetime object oluşturdum
    result.rename(columns={'Tarih': 'cdate_t'}, inplace=True)
    result.rename(columns={'Deniz_Seviyesi': 'ssh'}, inplace=True)

    return result
#-----------------------------------------------------------------------------------------------------------------------
def tudes15dk_iqr(df):
    """
        --> 15dklık verilere IQR uygulanması için kullanılır.
        --> İki farklı df döndürecek.
    """
    # Detrend hesabı
    detrended = sc.signal.detrend(df["ssh"], type="linear")
    detrended_df = pd.DataFrame(detrended, columns=["detrended_15lik"])

    # Detrend series'ı ile df'in birleştirilmesi
    df_merged = pd.concat([df, detrended_df], axis=1)  # IQR ÖNCESİ DF BU, ÇİZDİRİLECEK DETREBD GRAFİĞİ BU OLACAK   #BUNA 0 DEDİM

    # IQR analizi
    Q1 = df_merged["detrended_15lik"].quantile(0.25)
    Q3 = df_merged["detrended_15lik"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df_merged.query('(@Q1 - 1.5 * @IQR) <= detrended_15lik <= (@Q3 + 1.5 * @IQR)')  # IQR SONRASI DF BU, BU DA IQR OLARAK ÇİZDİRİLECEK (SSH VE DETREND)  #BUNA 1 DEDİM
    filtered.drop(columns = ["detrended_15lik"], inplace = True)

    return df_merged, filtered
#-----------------------------------------------------------------------------------------------------------------------
def tudes15_saatlik(df):
    """
        --> 15 dakikalık verilerden saatlik veriler üretmek için.
    """
    # 15dklık verilerden saatlik veriler elde edilmesi
    df = df.resample('H', on='cdate_t', closed='right').mean().reset_index()
    return df
#-----------------------------------------------------------------------------------------------------------------------
def tudes_15_60_birlestir(df1, df2):
    """
        --> 15 ve 60dk'lık verilerin birleştirilmesi için.

        input : list
        output: df
    """
    frames = [df1, df2]
    result = pd.concat(frames)
    result.reset_index(inplace=True, drop=True)
    result.drop_duplicates(subset=['cdate_t'], inplace=True)
    result.reset_index(inplace=True, drop=True)
    return result
#-----------------------------------------------------------------------------------------------------------------------
def tudes60dk_iqr(df):
    """
        --> Saatlik verilere IQR uygulanması için kullanılır.
        --> İki farklı df döndürecek.
    """
    df.dropna(0, inplace = True)
    df.reset_index(inplace = True, drop = True)

    # Detrend hesabı
    detrended = sc.signal.detrend(df["ssh"], type="linear")
    detrended_df = pd.DataFrame(detrended, columns=["detrended_saatlik"])

    # Detrend series'ı ile df'in birleştirilmesi
    df_merged = pd.concat([df, detrended_df], axis=1)  # IQR ÖNCESİ DF BU, ÇİZDİRİLECEK DETREBD GRAFİĞİ BU OLACAK   #BUNA 0 DEDİM

    # IQR analizi
    Q1 = df_merged["detrended_saatlik"].quantile(0.25)
    Q3 = df_merged["detrended_saatlik"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df_merged.query('(@Q1 - 1.5 * @IQR) <= detrended_saatlik <= (@Q3 + 1.5 * @IQR)')  # IQR SONRASI DF BU, BU DA IQR OLARAK ÇİZDİRİLECEK (SSH VE DETREND)  #BUNA 1 DEDİM
    filtered.drop(columns = ["detrended_saatlik"], inplace = True)

    return df_merged, filtered
#-----------------------------------------------------------------------------------------------------------------------
def tudes_gunluk(df):
    # Günlük verilerin oluşturulması
    df = df.groupby(pd.Grouper(freq='D', key='cdate_t')).mean()
    df.reset_index(inplace = True)
    df.dropna(0, inplace = True)
    df.reset_index(inplace = True, drop = True)
    return df
#-----------------------------------------------------------------------------------------------------------------------
def tudes_gunluk_iqr(df):
    """
            --> Günlük verilere IQR uygulanması için kullanılır.
            --> İki farklı df döndürecek.
        """
    # Detrend hesabı
    detrended = sc.signal.detrend(df["ssh"], type="linear")
    detrended_df = pd.DataFrame(detrended, columns=["detrended_gunluk"])

    # Detrend series'ı ile df'in birleştirilmesi
    df_merged = pd.concat([df, detrended_df], axis=1)  # IQR ÖNCESİ DF BU, ÇİZDİRİLECEK DETREBD GRAFİĞİ BU OLACAK   #BUNA 0 DEDİM

    # IQR analizi
    Q1 = df_merged["detrended_gunluk"].quantile(0.25)
    Q3 = df_merged["detrended_gunluk"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df_merged.query('(@Q1 - 1.5 * @IQR) <= detrended_gunluk <= (@Q3 + 1.5 * @IQR)')  # IQR SONRASI DF BU, BU DA IQR OLARAK ÇİZDİRİLECEK (SSH VE DETREND)  #BUNA 1 DEDİM
    filtered.drop(columns=["detrended_gunluk"], inplace=True)

    return df_merged, filtered
#-----------------------------------------------------------------------------------------------------------------------
def tudes_aylik(df):
    # Aylık verilerin oluşturulması
    df = df.resample("MS", on="cdate_t").mean()  # Tarih bilgisi yine indexte
    df.reset_index(inplace=True)  # Indexten aldım
    return df
#-----------------------------------------------------------------------------------------------------------------------
def tudes_aylik_iqr(df):
    """
            --> Günlük verilere IQR uygulanması için kullanılır.
            --> İki farklı df döndürecek.
        """
    df.dropna(0, inplace=True)
    df.reset_index(inplace=True, drop=True)

    # Detrend hesabı
    detrended = sc.signal.detrend(df["ssh"], type="linear")
    detrended_df = pd.DataFrame(detrended, columns=["detrended_aylik"])

    # Detrend series'ı ile df'in birleştirilmesi
    df_merged = pd.concat([df, detrended_df],
                          axis=1)  # IQR ÖNCESİ DF BU, ÇİZDİRİLECEK DETREBD GRAFİĞİ BU OLACAK   #BUNA 0 DEDİM

    # IQR analizi
    Q1 = df_merged["detrended_aylik"].quantile(0.25)
    Q3 = df_merged["detrended_aylik"].quantile(0.75)

    IQR = Q3 - Q1

    filtered = df_merged.query('(@Q1 - 1.5 * @IQR) <= detrended_aylik <= (@Q3 + 1.5 * @IQR)')  # IQR SONRASI DF BU, BU DA IQR OLARAK ÇİZDİRİLECEK (SSH VE DETREND)  #BUNA 1 DEDİM
    filtered.drop(columns=["detrended_aylik"], inplace=True)

    return df_merged, filtered
#-----------------------------------------------------------------------------------------------------------------------
def tudes60dk_duzenle(df):
    """
        --> 60dklık veriyi düzenler.
    """
    # Verilerin tarih bilgilerinin düzeltilmesi ve IQR hesabının yapılarak birleştirilmiş 15dklık verilerin elde edilmesi
    df['Tarih'] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y %H:%M:%S')  # Datetime object oluşturdum
    df.rename(columns={'Tarih': 'cdate_t'}, inplace=True)
    df.rename(columns={'Deniz_Seviyesi': 'ssh'}, inplace=True)

    return df
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
def pre_ekksa_tudes(df):
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
    df3.set_index("date", inplace=True)

    # Ağırlık column'unun oluşturulması
    df3["weight"] = 1

    df3.reset_index(inplace=True)
    df3.rename_axis("ay", inplace=True)

    return df3










