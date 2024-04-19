import requests
import json
from config import currencies, API
class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    # Т.К. используемый API возвращает не конвертированную сумму, а курс валюты, то base_ticker и quote_ticker
    # изменены местами, чтобы конвертация была правильной (при вводимом по ТЗ запросу).
    def get_price(quote, base, amount):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}.')

        try:
            base_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            quote_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
            if amount <= 0:
                raise APIException(f'Количество валюты не может быть отрицательным')
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        r = requests.get(f'https://api.currencyapi.com/v3/latest?apikey={API}&currencies={quote_ticker}&base_currency={base_ticker}')
        conversion_rate = json.loads(r.content)['data'][quote_ticker]['value']


        return conversion_rate