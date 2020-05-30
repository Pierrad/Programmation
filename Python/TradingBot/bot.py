import requests
from yahoo_fin.stock_info import get_day_gainers

# Top Gainers of the day
data = get_day_gainers()
# Get the 5 first and transform the pandas dataframe into a list
topFive = data.iloc[0:5,0].values.tolist()
print(topFive)
for i in range(len(topFive)):
    # On récupère les données sur le site
    API_URL = "https://www.alphavantage.co/query"
    data = { "function": "TIME_SERIES_INTRADAY",
            "symbol": topFive[i],
            "interval": "1min",
            "outputsize": "compact",
            "datatype": "json",
            "apikey": "20M98U0442RX494K" }
    response = requests.get(API_URL, data)
    data = response.json()

    # Globalement les actions suivantes réduisent de plus en plus le dictionnaire pour ne donner qu'une liste de liste
    # Convertit le dictionnaire en list
    data = list(data.values())
    # On convertit la dict globale des dates en list en gardant les dates (les keys) (intérieur est toujours dict comme ca on peut supprimer plus facilement)
    data = list(data[1].items())
    print(topFive[i])
    print(data[0][1]['1. open'])
    print(data[1][1]['1. open'])
    print(0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i,0+i)