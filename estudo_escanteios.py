#%%

import pandas as pd
import warnings
warnings.filterwarnings('ignore')
# %%
df = pd.read_excel('https://github.com/futpythontrader/YouTube/blob/main/Brasil_S%C3%A9rie_A.xlsx?raw=true')
# %%
df = df[['League','League','Season','Home','Away','HT_Corner_Kicks_H','HT_Corner_Kicks_A','FT_Corner_Kicks_H','FT_Corner_Kicks_A']]
df
# %%
df = df.reset_index()
# df = df[df.League == "BRAZIL - SERIE A"]
df = df[df.Season == 2021]
df
# %%
df = df[['Season','Home','Away','HT_Corner_Kicks_H','HT_Corner_Kicks_A','FT_Corner_Kicks_H','FT_Corner_Kicks_A']]
df.columns = ['Temporada','Home','Away','HT_Cantos_H','HT_Cantos_A','FT_Cantos_H','FT_Cantos_A']
df.dropna(inplace = True)
# Ajustando o Índice
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(['Nº'])
df = df.rename(index=lambda x: x + 1)
df
# %%
df_HT = df[['Home','Away','HT_Cantos_H','HT_Cantos_A']]
df_HT['HT_Cantos_Total'] = df_HT['HT_Cantos_H'] + df_HT['HT_Cantos_A']  

# Média
df_HT['Media_Cantos_Marcados_Home'] = df_HT.groupby('Home')['HT_Cantos_H'].rolling(window=5, min_periods=1).mean().reset_index(0,drop=True)
df_HT['Media_Cantos_Sofridos_Home'] = df_HT.groupby('Home')['HT_Cantos_A'].rolling(window=5, min_periods=1).mean().reset_index(0,drop=True)
df_HT['Media_Cantos_Total_Home'] = df_HT.groupby('Home')['HT_Cantos_Total'].rolling(window=5, min_periods=1).mean().reset_index(0,drop=True)

# Desvio Padrão
df_HT['DesvP_Cantos_Marcados_Home'] = df_HT.groupby('Home')['HT_Cantos_H'].rolling(window=5, min_periods=1).std().reset_index(0,drop=True)
df_HT['DesvP_Cantos_Sofridos_Home'] = df_HT.groupby('Home')['HT_Cantos_A'].rolling(window=5, min_periods=1).std().reset_index(0,drop=True)
df_HT['DesvP_Cantos_Total_Home'] = df_HT.groupby('Home')['HT_Cantos_Total'].rolling(window=5, min_periods=1).std().reset_index(0,drop=True)

# Coeficiente de Variação
df_HT['CV_Cantos_Marcados_Home'] = df_HT['DesvP_Cantos_Marcados_Home'] / df_HT['Media_Cantos_Marcados_Home']
df_HT['CV_Cantos_Sofridos_Home'] = df_HT['DesvP_Cantos_Sofridos_Home'] / df_HT['Media_Cantos_Sofridos_Home']
df_HT['CV_Cantos_Total_Home'] = df_HT['DesvP_Cantos_Total_Home'] / df_HT['Media_Cantos_Total_Home']

# Média
df_HT['Media_Cantos_Marcados_Away'] = df_HT.groupby('Away')['HT_Cantos_A'].rolling(window=5, min_periods=1).mean().reset_index(0,drop=True)
df_HT['Media_Cantos_Sofridos_Away'] = df_HT.groupby('Away')['HT_Cantos_H'].rolling(window=5, min_periods=1).mean().reset_index(0,drop=True)
df_HT['Media_Cantos_Total_Away'] = df_HT.groupby('Away')['HT_Cantos_Total'].rolling(window=5, min_periods=1).mean().reset_index(0,drop=True)

# Desvio Padrão
df_HT['DesvP_Cantos_Marcados_Away'] = df_HT.groupby('Away')['HT_Cantos_A'].rolling(window=5, min_periods=1).std().reset_index(0,drop=True)
df_HT['DesvP_Cantos_Sofridos_Away'] = df_HT.groupby('Away')['HT_Cantos_H'].rolling(window=5, min_periods=1).std().reset_index(0,drop=True)
df_HT['DesvP_Cantos_Total_Away'] = df_HT.groupby('Away')['HT_Cantos_Total'].rolling(window=5, min_periods=1).std().reset_index(0,drop=True)

# Coeficiente de Variação
df_HT['CV_Cantos_Marcados_Away'] = df_HT['DesvP_Cantos_Marcados_Away'] / df_HT['Media_Cantos_Marcados_Away']
df_HT['CV_Cantos_Sofridos_Away'] = df_HT['DesvP_Cantos_Sofridos_Away'] / df_HT['Media_Cantos_Sofridos_Away']
df_HT['CV_Cantos_Total_Away'] = df_HT['DesvP_Cantos_Total_Away'] / df_HT['Media_Cantos_Total_Away']
# %%
df_HT = df_HT[['Home','Away','HT_Cantos_H','HT_Cantos_A','HT_Cantos_Total',
 'Media_Cantos_Marcados_Home','CV_Cantos_Marcados_Home','Media_Cantos_Sofridos_Home','CV_Cantos_Sofridos_Home',
 'Media_Cantos_Total_Home','CV_Cantos_Total_Home',
 'Media_Cantos_Marcados_Away','CV_Cantos_Marcados_Away','Media_Cantos_Sofridos_Away','CV_Cantos_Sofridos_Away',
 'Media_Cantos_Total_Away','CV_Cantos_Total_Away']]
df_HT
# %%
df_HT.dropna(inplace = True)
# Ajustando o Índice
df_HT.reset_index(inplace=True, drop=True)
df_HT.index = df_HT.index.set_names(['Nº'])
df_HT = df_HT.rename(index=lambda x: x + 1)
df_HT
# %%

df_HT_Home = df_HT[['Home','Media_Cantos_Marcados_Home','CV_Cantos_Marcados_Home',
                    'Media_Cantos_Sofridos_Home','CV_Cantos_Sofridos_Home',
                    'Media_Cantos_Total_Home','CV_Cantos_Total_Home']]
df_HT_Home = df_HT_Home.tail(20)
df_HT_Home = df_HT_Home.sort_values(by=['Home'])
df_HT_Home.reset_index(inplace=True, drop=True)
df_HT_Home.index = df_HT_Home.index.set_names(['Nº'])
df_HT_Home = df_HT_Home.rename(index=lambda x: x + 1)
df_HT_Home
# %%
df_HT_Away = df_HT[['Away','Media_Cantos_Marcados_Away','CV_Cantos_Marcados_Away',
                    'Media_Cantos_Sofridos_Away','CV_Cantos_Sofridos_Away',
                    'Media_Cantos_Total_Away','CV_Cantos_Total_Away']]
df_HT_Away = df_HT_Away.tail(20)
df_HT_Away = df_HT_Away.sort_values(by=['Away'])
df_HT_Away.reset_index(inplace=True, drop=True)
df_HT_Away.index = df_HT_Away.index.set_names(['Nº'])
df_HT_Away = df_HT_Away.rename(index=lambda x: x + 1)
df_HT_Away
# %%
