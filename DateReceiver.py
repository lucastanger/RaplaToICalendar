import requests
from bs4 import BeautifulSoup
import re


class DateReceiver:
    def __init__(self, year):
        self.year = year
        self.__scrape__()

    def __scrape__(self):
        self.html = requests.get('https://www.aktuelle-kalenderwoche.com/kalenderwochen-' + str(self.year) + '.html')
        self.samples = BeautifulSoup(self.html.content, features='html.parser')
        td = self.samples.find_all(attrs={'class': 'even'})
        self.days = []
        for tr in td:
            self.days.append(re.findall('(\d\d).(\d\d)', tr.text))

    def getAllMondays(self):
        _tmp = []
        for d in self.days:
            # Remove first december
            if d[0][0] == '12':
                continue
            _tmp.append(d[1])
        return _tmp

    def getAllTuesdays(self):
        _tmp = []
        for d in self.days:
            _tmp.append(d[2])
        return _tmp

    def getAllWednesdays(self):
        _tmp = []
        for d in self.days:
            _tmp.append(d[3])
        return _tmp

    def getAllThursdays(self):
        _tmp = []
        for d in self.days:
            _tmp.append(d[4])
        return _tmp

    def getAllFridays(self):
        _tmp = []
        for d in self.days:
            _tmp.append(d[5])
        return _tmp

    def getAllSaturdays(self):
        _tmp = []
        for d in self.days:
            _tmp.append(d[6])
        return _tmp

    def getAllSundays(self):
        _tmp = []
        for d in self.days:
            _tmp.append(d[7])
        return _tmp
