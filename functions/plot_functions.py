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
def plot_digerleri_xt(df1, df2, df3, df4, title):
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

    fig.suptitle(f"{title} XTRACK Grafikleri", fontsize=15)
    fig.supxlabel("Tarih (Yıl)", fontsize=15)
    fig.supylabel("Deniz Seviyesi Yükseklikleri (m)", fontsize=15)
    plt.subplots_adjust(hspace = 0.5)
    plt.tight_layout()
    plt.show()
#-----------------------------------------------------------------------------------------------------------------------
def plot_ekksa_xt(df, title, mss, trend, year, month, day, h):
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
    plt.title(f"{title} XTRACK SSH Grafiği")
    plt.show()












