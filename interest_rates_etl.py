import requests
import numpy as np
import pandas as pd
import json
import os
from os.path import join, dirname
from pprint import pprint
from dotenv import load_dotenv
import urllib3
import matplotlib.pyplot as plt
import datetime

def run_interest_rate_etl():

    print("INSIDE RUN INTEREST RATE")

    """
    Displays the Government Yield bond spread FR/DE 10Y
    FR
    [{"date":"2024-08-22","open":2.9186,"high":2.9614,"low":2.8907,"close":2.9594,"adjusted_close":2.9594,"volume":0},
    {"date":"2024-08-23","open":2.9333,"high":2.9333,"low":2.9333,"close":2.9333,"adjusted_close":2.9333,"volume":0}]

    DE
    {"date":"2024-08-22","open":2.1937,"high":2.249,"low":2.1823,"close":2.2487,"adjusted_close":2.2487,"volume":0},
    {"date":"2024-08-23","open":2.2325,"high":2.2325,"low":2.2325,"close":2.2325,"adjusted_close":2.2325,"volume":0}] 
    """

    dotenv_path = join(dirname(__file__), '.env')
    print(dotenv_path)
    load_dotenv(dotenv_path)

    BONDS_API_TOKEN = os.getenv('BONDS_API_TOKEN')
    print(BONDS_API_TOKEN)
    S3_UNIQUE_BUCKET_NAME = os.getenv('S3_UNIQUE_BUCKET_NAME')
    print(S3_UNIQUE_BUCKET_NAME)
    try:
        #urlFR3Y = f'https://eodhd.com/api/eod/FR3Y.GBOND?api_token=66c8a2688599a9.43777835&fmt=json'
        #urlDE3Y = f'https://eodhd.com/api/eod/DE3Y.GBOND?api_token=66c8a2688599a9.43777835&fmt=json'
        urlFR10Y = f'https://eodhd.com/api/eod/FR10Y.GBOND?api_token=\'{BONDS_API_TOKEN}\'&fmt=json'
        urlDE10Y = f'https://eodhd.com/api/eod/DE10Y.GBOND?api_token=\'{BONDS_API_TOKEN}\'&fmt=json'
        
        #dataFR3Y = requests.get(urlFR3Y).json()
        #dataDE3Y = requests.get(urlDE3Y).json()
        print(requests.get(urlFR10Y))
        dataFR10Y = requests.get(urlFR10Y).json()
        dataDE10Y = requests.get(urlDE10Y).json()

        #print(dataFR10Y)


        nbDays = len(dataFR10Y)

        #dataFR10Y = [{'date': '2024-08-13', 'open': 2.9658, 'high': 2.9834, 'low': 2.9161, 'close': 2.9235, 'adjusted_close': 2.9235, 'volume': 0}, {'date': '2024-08-14', 'open': 2.9235, 'high': 2.9671, 'low': 2.9042, 'close': 2.9159, 'adjusted_close': 2.9159, 'volume': 0}, {'date': '2024-08-15', 'open': 2.9159, 'high': 2.997, 'low': 2.906, 'close': 2.9905, 'adjusted_close': 2.9905, 'volume': 0}, {'date': '2024-08-16', 'open': 2.9905, 'high': 2.9951, 'low': 2.937, 'close': 2.9897, 'adjusted_close': 2.9897, 'volume': 0}, {'date': '2024-08-19', 'open': 2.9897, 'high': 2.9962, 'low': 2.9418, 'close': 2.9809, 'adjusted_close': 2.9809, 'volume': 0}, {'date': '2024-08-20', 'open': 2.9809, 'high': 2.9825, 'low': 2.9394, 'close': 2.9458, 'adjusted_close': 2.9458, 'volume': 0}, {'date': '2024-08-21', 'open': 2.9458, 'high': 2.9578, 'low': 2.9122, 'close': 2.9186, 'adjusted_close': 2.9186, 'volume': 0}, {'date': '2024-08-22', 'open': 2.9186, 'high': 2.9614, 'low': 2.8907, 'close': 2.9594, 'adjusted_close': 2.9594, 'volume': 0}, {'date': '2024-08-23', 'open': 2.9594, 'high': 2.9773, 'low': 2.9226, 'close': 2.9333, 'adjusted_close': 2.9333, 'volume': 0}, {'date': '2024-08-26', 'open': 2.9333, 'high': 2.9521, 'low': 2.919, 'close': 2.9489, 'adjusted_close': 2.9489, 'volume': 0}]
        #dataDE10Y = [{'date': '2024-08-13', 'open': 2.2333, 'high': 2.2333, 'low': 2.183, 'close': 2.1882, 'adjusted_close': 2.1882, 'volume': 0}, {'date': '2024-08-14', 'open': 2.1882, 'high': 2.2201, 'low': 2.1752, 'close': 2.1848, 'adjusted_close': 2.1848, 'volume': 0}, {'date': '2024-08-15', 'open': 2.1848, 'high': 2.2679, 'low': 2.1767, 'close': 2.2656, 'adjusted_close': 2.2656, 'volume': 0}, {'date': '2024-08-16', 'open': 2.2656, 'high': 2.2656, 'low': 2.2167, 'close': 2.2514, 'adjusted_close': 2.2514, 'volume': 0}, {'date': '2024-08-19', 'open': 2.2514, 'high': 2.2671, 'low': 2.2183, 'close': 2.2514, 'adjusted_close': 2.2514, 'volume': 0}, {'date': '2024-08-20', 'open': 2.2514, 'high': 2.259, 'low': 2.216, 'close': 2.2191, 'adjusted_close': 2.2191, 'volume': 0}, {'date': '2024-08-21', 'open': 2.2191, 'high': 2.2294, 'low': 2.1937, 'close': 2.1937, 'adjusted_close': 2.1937, 'volume': 0}, {'date': '2024-08-22', 'open': 2.1937, 'high': 2.249, 'low': 2.1823, 'close': 2.2487, 'adjusted_close': 2.2487, 'volume': 0}, {'date': '2024-08-23', 'open': 2.2487, 'high': 2.2636, 'low': 2.2228, 'close': 2.2325, 'adjusted_close': 2.2325, 'volume': 0}, {'date': '2024-08-26', 'open': 2.2325, 'high': 2.2442, 'low': 2.218, 'close': 2.2442, 'adjusted_close': 2.2442, 'volume': 0}]
        

        # Extraire les données pour chaque liste
        dates1, closesFR = extract_data(dataFR10Y[nbDays-100:])
        dates2, closesDE = extract_data(dataDE10Y[nbDays-100:])

        # Assurez-vous que les deux listes ont la même longueur
        min_length = min(len(closesFR), len(closesDE))
        dates = dates1[:min_length]
        diff_closes = np.array((closesFR[:min_length]) - np.array(closesDE[:min_length]))

        print(f'LAST France 10 Year vs Germany 10 Year Spread Bond Yield BP: {diff_closes[:min_length]}')
        # plotGraph(dates, diff_closes)
        export_S3(S3_UNIQUE_BUCKET_NAME, dates, diff_closes)



    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print("A connection error or timeout occurred:", e)
    except requests.exceptions.HTTPError as e:
        print("HTTP Error:", e)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except Exception as err:
        print(f'Other error occurred: {err}')


# Fonction pour extraire les dates et les valeurs de clôture en BP (point de base)
def extract_data(data_list):
    dates = [datetime.datetime.strptime(item['date'], '%Y-%m-%d') for item in data_list]
    closes = [item['close']*100 for item in data_list]
    return dates, closes

def plotGraph(dates, diff_closes):
   # Création du graphique
    plt.figure(figsize=(12, 6))
    plt.plot(dates, diff_closes, marker='o')

    plt.title("Évolution de la différence des valeurs de clôture en BP (point de base)")
    plt.xlabel("Date")
    plt.ylabel("Différence de clôture")
    plt.grid(True)

    # Rotation des étiquettes de date pour une meilleure lisibilité
    plt.gcf().autofmt_xdate()

    # Affichage du graphique
    plt.show()

def export_S3(S3_UNIQUE_BUCKET_NAME, dates, diff_closes):

    # Convertir diff_closes en DataFrame pandas
    df = pd.DataFrame({'date': dates, 'diff_close': diff_closes})

    # Exporter en CSV
    # csv_buffer = df.to_csv(index=False)

    # Configurer le client S3
    #s3_client = boto3.client('s3')

    # Télécharger vers S3
    bucket_name = S3_UNIQUE_BUCKET_NAME
    # file_name = 'spread10Y_FR_GER.csv'

    df.to_csv('s3://gov-bonds-spread-fr-ger-har/spread10Y_FR_GER.csv')

    """ s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=csv_buffer
    ) """    

urllib3.disable_warnings()    
run_interest_rate_etl()