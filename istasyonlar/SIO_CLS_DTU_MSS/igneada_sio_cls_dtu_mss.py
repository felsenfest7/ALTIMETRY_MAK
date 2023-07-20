import pandas as pd
import numpy as np
import sys
sys.path.insert(1, "/home/furkan/PycharmProjects/pythonProject/venv/ALTIMETRY_MAK/functions")

import functions_global_mss as fgm

desired_width=320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns',500)
pd.set_option('display.max_rows',100000)

path = "/home/furkan/deus/ALTIMETRY_2/DATA/SIO_CLS_DTU15_MSS/MSS_Combine_SIO_CNES15_DTU15.nc"
df = fgm.read_combined_mss(path, 25, 42.5, 35, 42.5)
deus = fgm.find_closest_combined_mss(df, 41.84, 28.01, 41.89, 28.21, "IADA", 41.88890424, 28.02351594, 41.8409454197531, 28.2003938024691)
