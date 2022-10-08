import os
import sys

sys.path.insert(0, os.path.abspath('./modulos'))

import pandas as pd
import group_2


df_tnbh = pd.read_csv("TNBH_Data.csv", index_col=[0,1])

print(df_tnbh.keys())

