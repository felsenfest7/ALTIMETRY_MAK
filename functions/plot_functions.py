import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib
from netCDF4 import Dataset as dt
import glob
import xarray as xr
import pandas as pd
import cartopy as ca
import os
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, MonthLocator, YearLocator
import statsmodels
import matplotlib.dates as dates
from sklearn.metrics import mean_squared_error
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.ticker import FormatStrFormatter
from dateutil.relativedelta import relativedelta
import math as m
import geopy.distance
#-----------------------------------------------------------------------------------------------------------------------
def plot_digerleri_xt(df1, df2, df3, df4, title, mode):
    """
        --> XTRACK verilerine ait verilerin grafikleri çizdirildi.
        --> df1: günlük ham veriler ve detrend değerleri buradan alınacak
            df2: IQR sonrası günlük ham veriler ve detrend değerleri buradan alınacak
            df3: aylık ham veriler ve detrend değerleri buradan alınacak
            df4: IQR sonrası aylık ham veriler ve detrend değeleri buradan alınacak
            df5: EKKSA sonrası çizdirilecek SSH_ilk ve SSH_model değerleri buradan alınacak
            mss: EKKSA sonrası elde edilen MSS değeri
            trend: EKKSA sonrası elde edilen trend değeri
            title: başlık
    """

    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff1, dff2, dff3, dff4 = df1, df2, df3, df4

    dff3.reset_index(inplace = True)
    dff4.reset_index(inplace = True)

    # Nan değerlerinin alınmaması
    dff1 = dff1[dff1["ssh"].notna()]
    dff1 = dff1[dff1["detrended_gunluk"].notna()]

    dff2 = dff2[dff2["ssh"].notna()]
    dff2 = dff2[dff2["detrended_gunluk"].notna()]

    dff3 = dff3[dff3["ssh"].notna()]
    dff3 = dff3[dff3["detrended_aylik"].notna()]

    dff4 = dff4[dff4["ssh"].notna()]
    dff4 = dff4[dff4["detrended_aylik"].notna()]

    #Plotların çizdirilmesi
    fig = plt.figure(figsize = (12,10))
    ax1 = fig.add_subplot(421)
    ax2 = fig.add_subplot(422)
    ax3 = fig.add_subplot(423)
    ax4 = fig.add_subplot(424)
    ax5 = fig.add_subplot(425)
    ax6 = fig.add_subplot(426)
    ax7 = fig.add_subplot(427)
    ax8 = fig.add_subplot(428)

    ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax3.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax4.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax5.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax6.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax7.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax8.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax1.xaxis.set_major_locator(MonthLocator(interval=24))
    ax2.xaxis.set_major_locator(MonthLocator(interval=24))
    ax3.xaxis.set_major_locator(MonthLocator(interval=24))
    ax4.xaxis.set_major_locator(MonthLocator(interval=24))
    ax5.xaxis.set_major_locator(MonthLocator(interval=24))
    ax6.xaxis.set_major_locator(MonthLocator(interval=24))
    ax7.xaxis.set_major_locator(MonthLocator(interval=24))
    ax8.xaxis.set_major_locator(MonthLocator(interval=24))

    ax1.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax2.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax3.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax4.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax5.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax6.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax7.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax8.fmt_xdata = DateFormatter('% Y-% m-% d')

    ax1.plot_date(dff1["cdate_t"], dff1["ssh"], "#0d88e6", label="SSH")
    ax2.plot_date(dff1["cdate_t"], dff1["detrended_gunluk"], "#FA5F55", label="Detrended")
    ax3.plot_date(dff2["cdate_t"], dff2["ssh"], "#0d88e6", label="SSH")
    ax4.plot_date(dff2["cdate_t"], dff2["detrended_gunluk"], "#FA5F55", label="Detrended")
    ax5.plot_date(dff3["cdate_t"], dff3["ssh"], "#0d88e6", label="SSH ")
    ax6.plot_date(dff3["cdate_t"], dff3["detrended_aylik"], "#FA5F55", label="Detrended")
    ax7.plot_date(dff4["cdate_t"], dff4["ssh"], "#0d88e6", label="SSH")
    ax8.plot_date(dff4["cdate_t"], dff4["detrended_aylik"], "#FA5F55", label="Detrended")

    ax1.set_title(f"{title} Ham Günlük Altimetri Verileri", fontsize = 12)
    ax2.set_title(f"{title} Ham Günlük Altimetri Verilerinin Detrend Değerleri", fontsize=12)
    ax3.set_title(f"{title} IQR Sonrası Günlük Altimetri Verileri", fontsize=12)
    ax4.set_title(f"{title} IQR Sonrası Günlük Altimetri Verilerinin Detrend Değerleri", fontsize=12)
    ax5.set_title(f"{title} Aylık Altimetri Verileri", fontsize=12)
    ax6.set_title(f"{title} Aylık Altimetri Verilerinin Detrend Değerleri", fontsize=12)
    ax7.set_title(f"{title} IQR Sonrası Aylık Altimetri Verileri", fontsize=12)
    ax8.set_title(f"{title} IQR Sonrası Aylık Altimetri Verilerinin Detrend Değerleri", fontsize=12)

    ax1.legend(loc="upper right")
    ax2.legend(loc="upper right")
    ax3.legend(loc="upper right")
    ax4.legend(loc="upper right")
    ax5.legend(loc="upper right")
    ax6.legend(loc="upper right")
    ax7.legend(loc="upper right")
    ax8.legend(loc="upper right")

    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    ax5.grid()
    ax6.grid()
    ax7.grid()
    ax8.grid()

    fig.suptitle(f"{title} XTRACK {mode} SSH Model Grafikleri", fontsize=15)
    fig.supxlabel("Tarih (Yıl)", fontsize=15)
    fig.supylabel("Deniz Seviyesi Yükseklikleri (m)", fontsize=15)
    plt.subplots_adjust(hspace = 0.5)
    plt.tight_layout()
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def plot_ekksa_xt(df, title, mss, trend, year, month, day, h, mode):
    """
        --> Dengelenmiş SSH değerlerinin çizdirilmesi için.
        --> Year, month, day ve h değerleri plota trend değerleri yazdırılırken yazdırılacağı yeri belirtir.
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = df

    # Nan değerlerinin alınmaması
    dff = dff[dff["SSH_ilk"].notna()]
    dff = dff[dff["SSH_model"].notna()]

    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["cdate_t"], dff["SSH_ilk"], "#FFBF00", label="SSH Ölçü")
    ax.plot_date(dff["cdate_t"], dff["SSH_model"], "#0d88e6", label="SSH Model")

    ax.axhline(y = mss, c = "red", label = "MSS")
    plt.text(datetime.date(year, month, day), h, trend, fontsize=10)

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=12))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="upper left")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.title(f"{title} XTRACK {mode} SSH Modeli")
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def plot_digerleri_tudes(df1, df2, df3, df4, df5, df6, df7, df8, title):
    """
        --> TUDES verilerine ait verilerin grafikleri çizdirildi.
        --> df1: 15 dk ham veriler ve detrend değerleri buradan alınacak
            df2: IQR sonrası 15 dk ham veriler buradan alınacak
            df3: saatlik ham veriler ve detrend değerleri buradan alınacak
            df4: IQR sonrası saatlik ham veriler buradan alınacak
            df5: günlük ham veriler ve detrend değerleri buradan alınacak
            df6: IQR sonrası günlük ham veriler buradan alınacak
            df7: aylık ham veriler ve detrend değerleri buradan alınacak
            df8: IQR sonrası aylık ham veriler buradan alınacak
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff1, dff2, dff3, dff4, dff5, dff6, dff7, dff8 = df1, df2, df3, df4, df5, df6, df7, df8

    # Nan değerlerinin alınmaması
    dff1 = dff1[dff1["ssh"].notna()]
    dff1 = dff1[dff1["detrended_15lik"].notna()]

    dff2 = dff2[dff2["ssh"].notna()]

    dff3 = dff3[dff3["ssh"].notna()]
    dff3 = dff3[dff3["detrended_saatlik"].notna()]

    dff4 = dff4[dff4["ssh"].notna()]

    dff5 = dff5[dff5["ssh"].notna()]
    dff5 = dff5[dff5["detrended_gunluk"].notna()]

    dff6 = dff6[dff6["ssh"].notna()]

    dff7 = dff7[dff7["ssh"].notna()]
    dff7 = dff7[dff7["detrended_aylik"].notna()]

    dff8 = dff8[dff8["ssh"].notna()]

    # Plotların çizdirilmesi
    fig, ax = plt.subplots(4, 3, figsize=(12, 10))

    ax[0, 0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[0, 1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[0, 2].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[1, 0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[1, 1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[1, 2].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[2, 0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[2, 1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[2, 2].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[3, 0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[3, 1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax[3, 2].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

    ax[0, 0].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[0, 1].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[0, 2].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[1, 0].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[1, 1].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[1, 2].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[2, 0].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[2, 1].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[2, 2].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[3, 0].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[3, 1].xaxis.set_major_locator(MonthLocator(interval=24))
    ax[3, 2].xaxis.set_major_locator(MonthLocator(interval=24))

    ax[0, 0].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[0, 1].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[0, 2].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[1, 0].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[1, 1].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[1, 2].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[2, 0].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[2, 1].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[2, 2].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[3, 0].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[3, 1].fmt_xdata = DateFormatter('% Y-% m-% d')
    ax[3, 2].fmt_xdata = DateFormatter('% Y-% m-% d')

    #Plotların çizdirilmesi
    ax[0, 0].plot_date(dff1["cdate_t"], dff1["ssh"], "#24b7db", label="SL")
    ax[0, 1].plot_date(dff1["cdate_t"], dff1["detrended_15lik"], "#FA5F55", label="Detrended")
    ax[0, 2].plot_date(dff2["cdate_t"], dff2["ssh"], "#0d88e6", label="SL")

    ax[1, 0].plot_date(dff3["cdate_t"], dff3["ssh"], "#24b7db", label="SL")
    ax[1, 1].plot_date(dff3["cdate_t"], dff3["detrended_saatlik"], "#FA5F55", label="Detrended")
    ax[1, 2].plot_date(dff4["cdate_t"], dff4["ssh"], "#0d88e6", label="SL")

    ax[2, 0].plot_date(dff5["cdate_t"], dff5["ssh"], "#24b7db", label="SL")
    ax[2, 1].plot_date(dff5["cdate_t"], dff5["detrended_gunluk"], "#FA5F55", label="Detrended")
    ax[2, 2].plot_date(dff6["cdate_t"], dff6["ssh"], "#0d88e6", label="SL")

    ax[3, 0].plot_date(dff7["cdate_t"], dff7["ssh"], "#24b7db", label="SL")
    ax[3, 1].plot_date(dff7["cdate_t"], dff7["detrended_aylik"], "#FA5F55", label="Detrended")
    ax[3, 2].plot_date(dff8["cdate_t"], dff8["ssh"], "#0d88e6", label="SL")

    #Başlıklar
    ax[0, 0].set_title("15 Dakikalık Mareograf İstasyonu Verileri", fontsize=12)
    ax[0, 1].set_title("15 Dakikalık Mareograf İstasyonu Verilerinin Detrendleri", fontsize=12)
    ax[0, 2].set_title("IQR Sonrası 15 Dakikalık Mareograf İstasyonu Verileri", fontsize=12)

    ax[1, 0].set_title("Saatlik Mareograf İstasyonu Verileri", fontsize=12)
    ax[1, 1].set_title("Saatlik Mareograf İstasyonu Verilerinin Detrendleri", fontsize=12)
    ax[1, 2].set_title("IQR Sonrası Saatlik Mareograf İstasyonu Verileri", fontsize=12)

    ax[2, 0].set_title("Günlük Mareograf İstasyonu Verileri", fontsize=12)
    ax[2, 1].set_title("Günlük Mareograf İstasyonu Verilerinin Detrendleri", fontsize=12)
    ax[2, 2].set_title("IQR Sonrası Günlük Mareograf İstasyonu Verileri", fontsize=12)

    ax[3, 0].set_title("Aylık Mareograf İstasyonu Verileri", fontsize=12)
    ax[3, 1].set_title("Aylık Mareograf İstasyonu Verilerinin Detrendleri", fontsize=12)
    ax[3, 2].set_title("IQR Sonrası Aylık Mareograf İstasyonu Verileri", fontsize=12)

    ax[0, 0].legend(loc="upper right")
    ax[0, 1].legend(loc="upper right")
    ax[0, 2].legend(loc="upper right")
    ax[1, 0].legend(loc="upper right")
    ax[1, 1].legend(loc="upper right")
    ax[1, 2].legend(loc="upper right")
    ax[2, 0].legend(loc="upper right")
    ax[2, 1].legend(loc="upper right")
    ax[2, 2].legend(loc="upper right")
    ax[3, 0].legend(loc="upper right")
    ax[3, 1].legend(loc="upper right")
    ax[3, 2].legend(loc="upper right")

    ax[0, 0].grid()
    ax[0, 1].grid()
    ax[0, 2].grid()
    ax[1, 0].grid()
    ax[1, 1].grid()
    ax[1, 2].grid()
    ax[2, 0].grid()
    ax[2, 1].grid()
    ax[2, 2].grid()
    ax[3, 0].grid()
    ax[3, 1].grid()
    ax[3, 2].grid()

    fig.suptitle(f"{title} Mareograf İstasyonu SL Model Grafikleri", fontsize=15)
    fig.supxlabel("Tarih (Yıl)", fontsize=15)
    fig.supylabel("Deniz Seviyesi Yükseklikleri (m)", fontsize=15)
    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout()
    plt.show()
# -----------------------------------------------------------------------------------------------------------------------
def plot_ekksa_tudes(df, title, mss, trend, year, month, day, h):
    """
        --> Dengelenmiş SSH değerlerinin çizdirilmesi için.
        --> Year, month, day ve h değerleri plota trend değerleri yazdırılırken yazdırılacağı yeri belirtir.
    """
    # df çizdirilirken sorun verdiği için dff diye yeni bir dataframe e kopyalanır
    dff = df

    # Nan değerlerinin alınmaması
    dff = dff[dff["SSH_ilk"].notna()]
    dff = dff[dff["SSH_model"].notna()]

    # Plotun çizdirilmesi
    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.plot_date(dff["cdate_t"], dff["SSH_ilk"], "#FFBF00", label="SL Ölçü")
    ax.plot_date(dff["cdate_t"], dff["SSH_model"], "#0d88e6", label="SL Model")

    ax.axhline(y = mss, c = "red", label = "MSL")
    plt.text(datetime.date(year, month, day), h, trend, fontsize=10)

    # Year-Month bilgileri için MonthLocator kullanılmalı
    ax.xaxis.set_major_locator(MonthLocator(interval=12))
    # Burada ise verinin veri tipinin formatı girilmeli
    ax.fmt_xdata = DateFormatter('% Y-% m-% d')
    ax.set_xlabel("Tarih (Yıl-Ay)", fontsize=13)
    ax.set_ylabel("Ortalama Aylık Deniz Seviyesi Yüksekliği (m)", fontsize=13)
    ax.legend(loc="upper left")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.title(f"{title} Mareograf İstasyonu SL Modeli")
    plt.show()
