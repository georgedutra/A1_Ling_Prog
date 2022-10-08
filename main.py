import os
import sys

sys.path.insert(0, os.path.abspath('./modulos'))

import pandas as pd
import group_2


df_tnbh = pd.read_csv("TNBH_Data.csv", index_col=[0,1])

print("Group Question 2")
print("================")
print("Question 1:")
group_2.question_1(df_tnbh)

print("Question 2:")
group_2.question_2(df_tnbh)

print("Question 3:")
group_2.question_3(df_tnbh)