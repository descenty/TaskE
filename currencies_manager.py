import datetime
from currency import *
import urllib.request
import xml.dom.minidom


class CurrenciesManager:
    url: str = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req='

    @staticmethod
    def parse_currencies_by_date(date: datetime.date):
        response = urllib.request.urlopen(CurrenciesManager.url + date.strftime('%d/%m/%Y'))
        dom = xml.dom.minidom.parse(response)
        dom.normalize()
        node_array = dom.getElementsByTagName('Valute')
        currencies = []
        for node in node_array:
            children_values = [x.childNodes[0].nodeValue for x in node.childNodes]
            currency = Currency(children_values[3], children_values[1],
                                round(float(children_values[4].replace(',', '.')) / int(children_values[2]), 2))
            currencies.append(currency)
        return currencies

    @staticmethod
    def parse_currency_at_period(currency_char_code: str, period: tuple[datetime.date, datetime.date], delta_day: int):
        period = list(period)
        values = []
        while (period[1] - period[0]).days >= 0:
            values.append([x.value for x in CurrenciesManager.parse_currencies_by_date(period[0]) if x.char_code == currency_char_code][0])
            period[0] += datetime.timedelta(days=delta_day)
        return values
