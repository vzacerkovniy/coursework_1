import json
from src.utils import greeting, cards, top_transactions, currency_rates, stock_prices


def main(data):
    report = {
    "greeting": greeting(data),
    "cards": cards,
    "top_transactions": top_transactions,
    "currency_rates": currency_rates,
    "stock_prices": stock_prices
}
    json_report = json.dumps(report)
    return json_report