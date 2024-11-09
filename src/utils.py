import datetime
import json
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')
tf_token = os.getenv('TF_TOKEN')
api_stocks = os.getenv('API_STOCKS')

current_date_time = datetime.datetime.now()


def greeting():
    current_date_time = datetime.datetime.now()
    opts = {"greeting": ('Доброе утро', 'Добрый день', 'Добрый вечер', 'Доброй ночи')}
    if 12 > current_date_time.hour >= 6:
        greet = opts["greeting"][0]
        return greet
    elif 18 > current_date_time.hour >= 12:
        greet = opts["greeting"][1]
        return greet
    elif 0 > current_date_time.hour >= 18:
        greet = opts["greeting"][2]
        return greet
    elif 6 > current_date_time.hour >= 0:
        greet = opts["greeting"][3]
        return greet


# print(greeting(current_date_time))


def cards(data, start_date):
    excel_data = pd.read_excel(data)
    excel_data['Дата операции'] = pd.to_datetime(excel_data['Дата операции'])
    end_date = pd.Timestamp('2021-12-01') + pd.offsets.MonthEnd(0)
    filtered_excel_data = excel_data[excel_data['Дата операции'].between(start_date, end_date)]
    sorted_by_card = filtered_excel_data.sort_values(by='Номер карты', ascending=False)
    # print(sorted_by_card.iloc[0][2])
    # card_numbers = []
    # for i in sorted_by_card:
    #     sorted_by_card.iloc[i][2].append(card_numbers)
    # unique = []
    #
    # for card in card_numbers:
    #     if card in unique:
    #         continue
    #     else:
    #         unique.append(card)



print(cards('../data/operations.xlsx', '2021.12.01'))


def top_transactions(data, start_date):
    excel_data = pd.read_excel(data)
    excel_data['Дата операции'] = pd.to_datetime(excel_data['Дата операции'])
    end_date = pd.Timestamp('2021-12-01') + pd.offsets.MonthEnd(0)
    filtered_excel_data = excel_data[excel_data['Дата операции'].between(start_date, end_date)]
    sorted_by_amount = filtered_excel_data.sort_values(by='Сумма операции с округлением', ascending=False)
    top = [{'date': sorted_by_amount.iloc[0, 1],
            'amount': sorted_by_amount.iloc[0, 14],
            'category': sorted_by_amount.iloc[0, 9],
            'description': sorted_by_amount.iloc[0, 11]},
           {'date': sorted_by_amount.iloc[1, 1],
            'amount': sorted_by_amount.iloc[1, 14],
            'category': sorted_by_amount.iloc[1, 9],
            'description': sorted_by_amount.iloc[1, 11]},
           {'date': sorted_by_amount.iloc[2, 1],
            'amount': sorted_by_amount.iloc[2, 14],
            'category': sorted_by_amount.iloc[2, 9],
            'description': sorted_by_amount.iloc[2, 11]},
           {'date': sorted_by_amount.iloc[3, 1],
            'amount': sorted_by_amount.iloc[3, 14],
            'category': sorted_by_amount.iloc[3, 9],
            'description': sorted_by_amount.iloc[3, 11]},
           {'date': sorted_by_amount.iloc[4, 1],
            'amount': sorted_by_amount.iloc[4, 14],
            'category': sorted_by_amount.iloc[4, 9],
            'description': sorted_by_amount.iloc[4, 11]}
           ]

    return top


# print(top_transactions('../data/operations.xlsx', '2021.12.01'))


def currency_rates():
    url_usd = "https://api.apilayer.com/fixer/latest?base=USD&symbols=RUB"
    url_eur = "https://api.apilayer.com/fixer/latest?base=EUR&symbols=RUB"

    headers = {"apikey": api_key}

    response_usd = requests.get(url_usd, headers=headers)
    response_eur = requests.get(url_eur, headers=headers)
    result_usd = response_usd.json()
    result_eur = response_eur.json()

    rate = [{"currency": "USD",
             "rate": round(result_usd['rates']['RUB'], 2)},
            {"currency": "EUR",
             "rate": round(result_eur['rates']['RUB'], 2)}]

    return rate


# print(currency_rates())


def stock_prices():
    with open('../data/user_settings.json', 'r') as file:
        user_stocks = json.load(file)["user_stocks"]
        a = ','.join(user_stocks)
    url = f"https://api.twelvedata.com/quote?symbol={a}"
    headers = {"apikey": api_stocks}
    response = requests.get(url, headers=headers)
    data = response.json()
    stocks = [{"stock": user_stocks[0], "price": data[user_stocks[0]]["close"]},
              {"stock": user_stocks[1], "price": data[user_stocks[1]]["close"]},
              {"stock": user_stocks[2], "price": data[user_stocks[2]]["close"]},
              {"stock": user_stocks[3], "price": data[user_stocks[3]]["close"]},
              {"stock": user_stocks[4], "price": data[user_stocks[4]]["close"]}]
    return stocks


# print(stock_prices())