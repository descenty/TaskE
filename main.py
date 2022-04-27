import datetime

from tkinter_manager import *
import urllib.request
import xml.dom.minidom


def main():
    parse_currencies()
    create_window()


def parse_currencies():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(datetime.date.today().strftime('%d/%m/%y'))
    print(url)
    response = urllib.request.urlopen(url)
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    nodeArray = dom.getElementsByTagName('')


main()