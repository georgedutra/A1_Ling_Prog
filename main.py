import os
import sys

sys.path.insert(0, os.path.abspath('./modules'))

import pandas as pd
import group_1
import group_2
import group_3

try:
    df_tnbh = pd.read_csv('TNBH_Data.csv',index_col=[0,1])
except FileNotFoundError:
    print("The file 'TNBH_Data.csv' for the 2 group was not found.")

df = group_1.handled_df()
df_albums = group_1.handled_df("Albums")

print("Group Question 1")
print("================")

print("Generating pdf file with bar charts for each album to answer the question:")
print("'which songs are longest and which are shortest per album?")
group_1.song_duration_album(df_albums)
print("Done!")
print("============================================================")

print("Generating pdf file with bar charts for each album to answer the question:")
print("'which songs are the most and least popular per album?")
group_1.song_popularity_album(df_albums)
print("Done!")
print("============================================================")

print("Generating pdf file with a bar chart with the 4-longest and 4-shortest popular song of all times")
group_1.song_duration_all_times(df,4)
print("Done!")
print("============================================================")

print("Generating pdf file with bar charts for each album to answer the question:")
print("'which songs are the most and least popular per album?") 
group_1.song_popularity_all_times(df,4)
print("Done!")
print("============================================================")

print("Generating pdf file with a scatterplot to visualize any")
print("correlations between the popularity and the duration of the musics.")
group_1.scatterplot(df)
print("Done!")
print("============================================================")

print("The last question, about the awards of the group's albums can't be answered properly,")
print("because, as the group is of indie/rock music, they didn't received important awards.")
print("We searched for the position of their songs in the charts of Billboard, but they are not in the top 10")
print("of the main chart, being the maximum position 14. If we analyse the secondaries charts,")
print("they reached a peak position of 13 with the song 'Wipped Out' in the Billboard top 200,")
print("and peak position of 1 with 'Sweater Weather' in the Hot Rock & Alternative Songs.")
print("============================================================")

print("\n"*2)

print("Group Question 2")
print("================")
print("Question 1:")
group_2.question_1(df_tnbh)

print("Question 2:")
group_2.question_2(df_tnbh)

print("Question 3:")
group_2.question_3(df_tnbh)

print("Question 4:")
group_2.question_4(df_tnbh)

print("Question 5:")
group_2.question_5(df_tnbh)

print("Question 6:")
group_2.question_6(df_tnbh)

print("\n"*2)

print("Group Question 3")
print("================")
print("Question 1:")
group_3.question_1(df_albums)

print("Question 2:")
group_3.question_2(df_tnbh)

print("Question 3:")
group_3.question_3(df_albums)