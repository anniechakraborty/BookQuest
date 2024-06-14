import pandas as pd
import numpy as np

df_books = pd.read_csv('asset/books.csv')

print(df_books)
no_of_rows = df_books.shape[0]
print(no_of_rows)
