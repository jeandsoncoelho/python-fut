# %%
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
# %%
# Temparada Atual
df = pd.read_excel(
    "https://github.com/futpythontrader/YouTube/blob/main/x_FutPythonTrader_Base_de_Dados_2022_2024_x.xlsx?raw=true"
)
dfToDay = pd.read_excel(
    "https://github.com/futpythontrader/YouTube/blob/main/Jogos_do_Dia/2024-02-09_FutPythonTrader_Jogos_do_Dia.xlsx?raw=true"
)

# Temporadas Passadas
# df = pd.read_excel('https://github.com/futpythontrader/YouTube/blob/main/x_FutPythonTrader_Base_de_Dados_Temporadas_Pass
# %%
df.columns.to_list()
# %%
df = df[
    [
        "League",
        "Home",
        "Away",
        "Corners_H_FT",
        "Corners_A_FT",
        "TotalCorners_FT",
        "Odd_Corners_H",
        "Odd_Corners_D",
        "Odd_Corners_A",
        "Odd_Corners_Over75",
        "Odd_Corners_Over85",
        "Odd_Corners_Over95",
        "Odd_Corners_Over105",
        "Odd_Corners_Over115",
    ]
]
# df = df[['League','Home','Away','Odd_Corners_H','Odd_Corners_D','Odd_Corners_A','Odd_Corners_Over75', 'Odd_Corners_Over85', 'Odd_Corners_Over95', 'Odd_Corners_Over105', 'Odd_Corners_Over115']]
# Ajustando o Índice
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(["Nº"])
df = df.rename(index=lambda x: x + 1)

df_filtrado = df[df['Home'] == dfToDay['Home'][2]]
df = df_filtrado

# %%
df = df[
    (df.Odd_Corners_H != 0)
    & (df.Odd_Corners_D != 0)
    & (df.Odd_Corners_A != 0)
    & (df.Odd_Corners_Over75 != 0)
    & (df.Odd_Corners_Over85 != 0)
    & (df.Odd_Corners_Over95 != 0)
    & (df.Odd_Corners_Over105 != 0)
    & (df.Odd_Corners_Over115 != 0)
]
# df.dropna(inplace=True)
# Ajustando o Índice
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(["Nº"])
df = df.rename(index=lambda x: x + 1)
df
# %%
# Média
df["Media_Cantos_Marcados_Home"] = (
    df.groupby("Home")["Corners_H_FT"]
    .rolling(window=5, min_periods=1)
    .mean()
    .reset_index(0, drop=True)
)
df["Media_Cantos_Sofridos_Home"] = (
    df.groupby("Home")["Corners_A_FT"]
    .rolling(window=5, min_periods=1)
    .mean()
    .reset_index(0, drop=True)
)
df["Media_Cantos_Total_Home"] = (
    df.groupby("Home")["TotalCorners_FT"]
    .rolling(window=5, min_periods=1)
    .mean()
    .reset_index(0, drop=True)
)

# Desvio Padrão
df["DesvP_Cantos_Marcados_Home"] = (
    df.groupby("Home")["Corners_H_FT"]
    .rolling(window=5, min_periods=1)
    .std()
    .reset_index(0, drop=True)
)
df["DesvP_Cantos_Sofridos_Home"] = (
    df.groupby("Home")["Corners_A_FT"]
    .rolling(window=5, min_periods=1)
    .std()
    .reset_index(0, drop=True)
)
df["DesvP_Cantos_Total_Home"] = (
    df.groupby("Home")["TotalCorners_FT"]
    .rolling(window=5, min_periods=1)
    .std()
    .reset_index(0, drop=True)
)

# Coeficiente de Variação
df["CV_Cantos_Marcados_Home"] = (
    df["DesvP_Cantos_Marcados_Home"] / df["Media_Cantos_Marcados_Home"]
)
df["CV_Cantos_Sofridos_Home"] = (
    df["DesvP_Cantos_Sofridos_Home"] / df["Media_Cantos_Sofridos_Home"]
)
df["CV_Cantos_Total_Home"] = (
    df["DesvP_Cantos_Total_Home"] / df["Media_Cantos_Total_Home"]
)

# Média
df["Media_Cantos_Marcados_Away"] = (
    df.groupby("Away")["Corners_A_FT"]
    .rolling(window=5, min_periods=1)
    .mean()
    .reset_index(0, drop=True)
)
df["Media_Cantos_Sofridos_Away"] = (
    df.groupby("Away")["Corners_H_FT"]
    .rolling(window=5, min_periods=1)
    .mean()
    .reset_index(0, drop=True)
)
df["Media_Cantos_Total_Away"] = (
    df.groupby("Away")["TotalCorners_FT"]
    .rolling(window=5, min_periods=1)
    .mean()
    .reset_index(0, drop=True)
)

# Desvio Padrão
df["DesvP_Cantos_Marcados_Away"] = (
    df.groupby("Away")["Corners_A_FT"]
    .rolling(window=5, min_periods=1)
    .std()
    .reset_index(0, drop=True)
)
df["DesvP_Cantos_Sofridos_Away"] = (
    df.groupby("Away")["Corners_H_FT"]
    .rolling(window=5, min_periods=1)
    .std()
    .reset_index(0, drop=True)
)
df["DesvP_Cantos_Total_Away"] = (
    df.groupby("Away")["TotalCorners_FT"]
    .rolling(window=5, min_periods=1)
    .std()
    .reset_index(0, drop=True)
)

# Coeficiente de Variação
df["CV_Cantos_Marcados_Away"] = (
    df["DesvP_Cantos_Marcados_Away"] / df["Media_Cantos_Marcados_Away"]
)
df["CV_Cantos_Sofridos_Away"] = (
    df["DesvP_Cantos_Sofridos_Away"] / df["Media_Cantos_Sofridos_Away"]
)
df["CV_Cantos_Total_Away"] = (
    df["DesvP_Cantos_Total_Away"] / df["Media_Cantos_Total_Away"]
)
# %%
df.dropna(inplace=True)
# Ajustando o Índice
df.reset_index(inplace=True, drop=True)
df.index = df.index.set_names(["Nº"])
df = df.rename(index=lambda x: x + 1)
df
# %%
df.info()

# %%
