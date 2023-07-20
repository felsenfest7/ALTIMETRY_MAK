import xarray as xr
from netCDF4 import Dataset as dt
import pandas as pd
import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy as sci
import re
#-----------------------------------------------------------------------------------------
def read_cls(path, lon1, lon2, lat1, lat2):
    """
        --> CLS MSS versini okumak için yapıldı
        input: path -> verinin pathi
               lat1, lat2, lon1, lon2 -> verinin sınırlandırılması için koordinat
    """
    #Verinin açılması ve sadece mss verisinin alınması
    dataset = xr.open_dataset(path, decode_times=False)
    dataset2 = dataset["mss"]
    df = dataset2.to_dataframe()

    #Verinin sınırlandırılması
    idx = pd.IndexSlice
    df2 = df.loc[idx[lon1:lon2, lat1:lat2], :]

    return df2
#-----------------------------------------------------------------------------------------
def find_closest_cls(df, lat_min, lon_min, lat_max, lon_max, sta, sta_lat, sta_lon, xt_lat, xt_lon):

    #Verinin bir düzenlenmesi
    df.reset_index(inplace = True)
    df.rename(columns = {"NbLongitudes" : "longitude", "NbLatitudes": "latitude"}, inplace = True)

    #Plot çizdirilmesi
    margin = 0.02
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(lon_min - margin, lon_max + margin)
    ax.set_ylim(lat_min - margin, lat_max + margin)
    ax.scatter(df.longitude, df.latitude)

    #Mesafe hesabının yapılması
    d_lat = df.latitude - sta_lat
    d_lon = df.longitude - sta_lon
    r2_requested = d_lat ** 2 + d_lon ** 2
    i_j_loc = np.where(r2_requested == np.min(r2_requested))

    #İstasyona göre en yakın noktanın koordinatları
    nearest_point = df.iloc[i_j_loc]

    #Bunların çizdirilmesi
    ax.scatter(sta_lon, sta_lat, color='green')
    ax.text(sta_lon, sta_lat, f'{sta}')
    ax.scatter(nearest_point.longitude, nearest_point.latitude, color='red')
    ax.text(nearest_point.longitude, nearest_point.latitude, 'nearest')

    #XT noktasına göre en yakın grid noktası
    d_lat_2 = df.latitude - xt_lat
    d_lon_2 = df.longitude - xt_lon
    r2_requested_2 = d_lat_2 ** 2 + d_lon_2 ** 2
    i_j_loc_2 = np.where(r2_requested_2 == np.min(r2_requested_2))

    # İstasyona göre en yakın noktanın koordinatları
    nearest_point_xt = df.iloc[i_j_loc_2]

    # Bunların çizdirilmesi
    ax.scatter(xt_lon, xt_lat, color='black')
    ax.text(xt_lon, xt_lat, 'XT')
    ax.scatter(nearest_point_xt.longitude, nearest_point_xt.latitude, color='red')
    ax.text(nearest_point_xt.longitude, nearest_point_xt.latitude, 'nearest xt')

    print(nearest_point_xt)

    plt.show()
#-----------------------------------------------------------------------------------------
def read_combined_mss(path, lon1, lon2, lat1, lat2):
    """
            --> Combined SIO/CLS/DTU MSS versini okumak için yapıldı
            input: path -> verinin pathi
                   lat1, lat2, lon1, lon2 -> verinin sınırlandırılması için koordinat
        """
    # Verinin açılması ve sadece mss verisinin alınması
    dataset = xr.open_dataset(path, decode_times=False)
    dataset2 = dataset["mssh"]
    df = dataset2.to_dataframe()

    # Verinin sınırlandırılması
    idx = pd.IndexSlice
    df2 = df.loc[idx[lat1:lat2, lon1:lon2], :]

    return df2
#-----------------------------------------------------------------------------------------
def find_closest_combined_mss(df, lat_min, lon_min, lat_max, lon_max, sta, sta_lat, sta_lon, xt_lat, xt_lon):
    """
        --> Combined MSS verisinde en yakın grid noktasının bulunmasında kullanılır.
    :param df:      Veri grubu
    :param lat_min: minimum lat sınırı
    :param lon_min: minimum lon sınırı
    :param lat_max: maksimum lat sınırı
    :param lon_max: maksimum lon sınırı
    :param sta:     istasyon ismi
    :param sta_lat: istasyon enlemi
    :param sta_lon: istasyon boylamı
    :param xt_lat:  xtrack noktası enlemi
    :param xt_lon:  xtrack noktası boylamı
    :return:
    """
    # Verinin bir düzenlenmesi
    df.reset_index(inplace=True)

    # Plot çizdirilmesi
    margin = 0.02
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(lon_min - margin, lon_max + margin)
    ax.set_ylim(lat_min - margin, lat_max + margin)
    ax.scatter(df.longitude, df.latitude)

    # Mesafe hesabının yapılması
    d_lat = df.latitude - sta_lat
    d_lon = df.longitude - sta_lon
    r2_requested = d_lat ** 2 + d_lon ** 2
    i_j_loc = np.where(r2_requested == np.min(r2_requested))

    # İstasyona göre en yakın noktanın koordinatları
    nearest_point = df.iloc[i_j_loc]

    # Bunların çizdirilmesi
    ax.scatter(sta_lon, sta_lat, color='green', label = "Mareograf İstasyonu")
    ax.text(sta_lon, sta_lat, f'{sta}', fontsize  = 12)
    ax.scatter(nearest_point.longitude, nearest_point.latitude, color='red', label = "Mareograf İstasyonuna Yakın MSS Noktası")
    ax.text(nearest_point.longitude, nearest_point.latitude, 'Yakın İstasyon', fontsize  = 12)

    # XT noktasına göre en yakın grid noktası
    d_lat_2 = df.latitude - xt_lat
    d_lon_2 = df.longitude - xt_lon
    r2_requested_2 = d_lat_2 ** 2 + d_lon_2 ** 2
    i_j_loc_2 = np.where(r2_requested_2 == np.min(r2_requested_2))

    # İstasyona göre en yakın noktanın koordinatları
    nearest_point_xt = df.iloc[i_j_loc_2]

    # Bunların çizdirilmesi
    ax.scatter(xt_lon, xt_lat, color='black', label = "XT Noktası")
    ax.text(xt_lon, xt_lat, 'XT', fontsize  = 12)
    ax.scatter(nearest_point_xt.longitude, nearest_point_xt.latitude, color='red', label = "XT Noktasına Yakın MSS Noktası")
    ax.text(nearest_point_xt.longitude, nearest_point_xt.latitude, 'Yakın XT', fontsize  = 12)

    print(nearest_point)
    print(nearest_point_xt)

    ax.set_xlabel("Boylam")
    ax.set_ylabel("Enlem")
    ax.xaxis.label.set_size(15)
    ax.yaxis.label.set_size(15)
    plt.title(f"{sta} Durum", fontsize = 15)
    plt.legend(loc = "upper right")
    plt.show()

















