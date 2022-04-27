import datetime

from tkinter_manager import *
from currency import *
import urllib.request
import xml.dom.minidom


def main():
    currencies = parse_currencies()
    tkinter_manager = TkinterManager(currencies)
    tkinter_manager.create_window()


def parse_currencies():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(datetime.date.today().strftime('%d/%m/%Y'))
    print(url)
    response = urllib.request.urlopen(url)
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


main()