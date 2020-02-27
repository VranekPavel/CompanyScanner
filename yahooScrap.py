from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import psycopg2
import re

class YahooFinanceTickers():

    def __init__(self, url):
        self.url = url,

    def tickers(self):
        output = []
        response = requests.get(self.url[0]).text
        soup = BeautifulSoup(response, 'html.parser')

        for item in soup.find_all("a", class_="Fw(600)"):
            match = re.search(r'href="\/quote\/(?P<ticker>.*?)\?', str(item))
            output.append(match.group('ticker'))

        return output

class IOhandler():
    def __init__(self, file):
        self.file = file

    def writer(self, text):
        f = open(self.file, 'w')
        f.write(str(text))
        f.close()

