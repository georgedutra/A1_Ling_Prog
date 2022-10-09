# A1_Ling_Prog - The Neighbourhood Data Anlysis

Project for the Programming Language discipline at EMAP FGV.

In this project we made a scrapper to collect data from Spotify API and Letras about The Neighbourhood group, anda made some analysis about this data.

An explanation about what we tought when answering each group of questions:

Group 1:

To answer questions 1 to 4, we chose to go mainly with bar graphs, as they are simple but very effective for comparing quantitative variables. We choose not to print anything on the terminal for these questions because the graph speaks for itself.
In particular for question 1 and 2, we choose to not make charts for albums that contained less than 3 musics because most of them are singles that belong to other albums.

To answer question 5 we printed in the terminal explaining about the non-existence of major awards won by the band. We also made a little research about the Billboard history of the band.

To answer question 6 we first calculated the Pearson's correlation coefficient and then made a scatter plot.  We also added a brief explanation about what conclusions we could make with both the coefficient and the chart together.

Group 2:

To answer questions 1 to 4 we simply concatenated all lyrics or names in a single string, and made a counter for each word frequency in the string.

To answer questions 5 and 6, we verified if an album's or music's names appears in the lyrics, and if it happens in at least half the albums or half the musics, we print a message saying it's a common ocurrence.
 
Group 3:

To answer questions 1 and 3, we choose to check which album had the bigger duration average and popularity, average respectively.

To answer question 2 we looked to se if there was any correlation between a song being explicit and it's popularity. 

The documentation can be found at: https://georgedutra.github.io/A1_Ling_Prog/index.html.

To install the requirements:
```
    pip install requirements.txt
```

Our results examples can be found in the images folder, and to see the written results, please run the main.py file in the A1_Ling_Prog folder:

```
    python3 main.py
```
