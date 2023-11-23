import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt

df = pd.read_csv('./spotify.csv', encoding='latin-1')

#Limpieza de datos
#print(df.corr(method='kendall', numeric_only=True))
print(df['in_shazam_charts'][13])
for i in range(0, len(df)):
    print(i)
    int(df['in_shazam_charts'][i])