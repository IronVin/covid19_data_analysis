#ESERCIZIO 4
#importo le librerie
import os
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#1)
#leggo il file specificato
df_covid = pd.read_csv('covid_01-01-2021.csv')
#mostro le prime 5 righe del file
print(" Leggo le prime 5 righe del file ".center(200, "*"))
print(df_covid.head())
#visualizzo le informazioni del set di dati
print(" Informazionioni del Dataset ".center(200, "*"))
print(df_covid.info())
#controllo i dati mancanti
print(" controllo dei dati mancanti ".center(200, "*")) 
print(df_covid.isnull().sum())

#2)
#calcolo e stampo a schermo l'ultimo numero di casi confermati di COVID (morti, recuperi e casi attivi) per paese
casi_confermati = df_covid.groupby("Country_Region")[["Confirmed", "Deaths", "Recovered", "Active"]].sum()
print(" Casi confermati per ogni paese ".center(200, "*")) 
print(casi_confermati)

#3)
#creo una lista dei paesi dove non ci sono casi recuperati
paesi_senza_recuperi = casi_confermati[casi_confermati["Recovered"]== 0].index.tolist()
print(" Paesi che non hanno pazienti recuperati ".center(200, "*")) 
print(paesi_senza_recuperi)

#4)
#ordino i paesi per casi confermati in modo decrescente e seleziono le prime 10 righe
top_10 = casi_confermati.sort_values(by="Confirmed", ascending=False).head(10)
#seleziono solo le colonne richieste 
top_10_info = top_10[["Confirmed", "Deaths", "Recovered", "Active"]]
#stampo
print(" Top 10 paesi per casi confermati ".center(200, "*"))
print(top_10_info)

#5)
#riutilizzo il DataFrame casi_confermati e prendo solo i paesi con piu' di 150 morti
#uso reset_index per riconvertire Country_region in una normale colonna
paesi_150 = casi_confermati[casi_confermati["Deaths"] > 150].reset_index()
paesi_150["Recovered"] = paesi_150["Recovered"].replace(0, np.nan)
df_dati = paesi_150.melt(
    id_vars = ["Country_Region"],
    value_vars = ["Confirmed", "Deaths", "Recovered"],
    var_name = "Categoria",
    value_name = "Numero Casi"
)
#creo il grafico con seaborn
plt.figure(figsize = (24, 7))
sns.lineplot(
    data = df_dati,
    x = "Country_Region",
    y = "Numero Casi",
    hue = "Categoria",
    marker = "o",
    linewidth = 2
)
#personalizzo e mostro il grafico 
plt.yscale("log")
plt.title("Confronto dati COVID-19 per Paesi con piu' di 150 decessi")   
plt.xlabel("Paesi", fontsize = 11)
plt.ylabel("Numero Casi (scala logaritmica)", fontsize = 11)
plt.xticks(rotation = 90, fontsize = 10)
plt.tight_layout()
plt.show()

#6)
#imposto lo stile visivo di seaborn
sns.set_theme(style = "whitegrid")
#lista dei file da utilizzare
files = [
    "COVID_01-01-2021.CSV",
    "COVID_01-02-2021.CSV",
    "COVID_01-03-2021.CSV"
]
#unisco e carico il DataFrame
dfs = []
for file in files:
    if os.path.exists(file):
        df_temp = pd.read_csv(file)
        #estrazione della data dal nome per la dimensione temporale
        data_str = file.replace("COVID_", "").replace(".CSV", "")
        df_temp["Date"] = pd.to_datetime(data_str, format = "%d-%m-%Y")
        dfs.append(df_temp)
df_totale = pd.concat(dfs, ignore_index = True)
df_totale.columns = df_totale.columns.str.strip()
#creo il grafico per la visualizzazione dei casi confermati nel primo trimestre del 2021
totale_per_data = (
    df_totale.groupby("Date")["Confirmed"].sum().reset_index()
)
plt.figure(figsize = (10, 5))
ax6 = sns.lineplot(
    data = totale_per_data,
    x = "Date",
    y = totale_per_data["Confirmed"] / 1e6,
    marker = "o",
    color = "tab:blue",
    linewidth = 2.5
)
plt.title(
    "Casi confermati di COVID-19 in generale/Primo trimestre 2021",
    fontsize = 13
)
plt.xlabel("Data")
plt.ylabel("Casi Confermati (in milioni)")
ax6.set_xticks(totale_per_data["Date"])
ax6.set_xticklabels(["01-01-2021", "01-02-2021", "01-03-2021"])
#aggiungo spazi automatici per evitare sovrapposizioni
plt.tight_layout()
plt.show()

#7)
#partendo dal DataFrame unito isoliamo solo i dati relativi  alla Spagna
# Isoliamo i dati relativi alla Spagna ed eliminiamo le voci non valide
df_spagna = df_totale[df_totale["Country_Region"] == "Spain"].copy()
df_spagna = df_spagna[df_spagna["Province_State"] != "Unknown"].dropna(
    subset=["Province_State"]
)

# Convertiamo la data in stringa pulita per la legenda
df_spagna["Data_Formattata"] = df_spagna["Date"].dt.strftime("%d-%m-%Y")

# [NOTA]: Verifichiamo quali date sono effettivamente disponibili per la Spagna
# (Il file del 01-01-2021 non contiene i dati della Spagna)
date_disponibili = df_spagna["Data_Formattata"].unique()
print(
    f"Nota Punto 7 - Date effettivamente presenti per la Spagna:"
    f" {date_disponibili}"
)
df_spagna = df_totale[df_totale["Country_Region"] == "Spain"].copy()
#uso un filtro per escludere la voce "Unknown"
df_spagna = df_spagna[df_spagna["Province_State"] != "Unknown"]
df_spagna = df_spagna.dropna(subset = ["Province_State"])
#pere una visione piu' chiara dei confermati e dei recuperati creo una figura con due sotto-grafici
fig, axes = plt.subplots(2, 1, figsize = (16, 8))
#creo il grafico dei casi confermati
sns.barplot(
    data = df_spagna,
    x = "Confirmed",
    y = "Province_State",
    hue = "Date",
    palette = "Blues",
    ax = axes[0]
)
axes[0].set_title("Evoluzione dei casi confermati in Spagna per Provincia (1° Trimestre 2021)", fontsize = 13, pad = 10)
axes[0].set_xlabel("Casi Confermati")
axes[0].set_ylabel("Provincia")
axes[0].legend(title = "Data", loc = "lower right")
#creo il grafico dei casi recuperati
sns.barplot(
    data = df_spagna,
    x = "Recovered",
    y = "Province_State",
    hue = "Date",
    palette = "Greens",
    ax = axes[1]
)
axes[1].set_title("Evoluzione dei pazienti recuperati in Spagna per Provincia (1° Trimestre 2021)", fontsize = 12, pad = 10)
axes[1].set_xlabel("Pazienti recuperati")
axes[1].set_ylabel("")
axes[1].legend(title = "Data", loc = "lower right")
#aggiungo spazi automatici per evitare sovrapposizioni
plt.tight_layout()
plt.show()

