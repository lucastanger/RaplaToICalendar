import random
import re
from datetime import datetime

import icalendar
import pytz
import requests
from bs4 import BeautifulSoup
from icalendar import Event
from icalendar import vCalAddress, vText

from DateReceiver import DateReceiver


class RaplaExtractor:
    def __init__(self, key, year):
        self.key = key
        self.year = year
        self.url = "https://rapla.dhbw-stuttgart.de/rapla?"
        self.lectures = []
        self.dates = []
        self.compute()

    def compute(self):
        dr = DateReceiver(int(self.year))
        days = dr.getAllMondays()

        cal = icalendar.cal.Calendar()
        cal.add('prodid', '-//My calendar product//mxm.dk//')
        cal.add('version', '2.0')

        for day in days:
            try:
                t_url = self.compose_url(self.url, self.key, str(day[0]), str(day[1]), self.year)
                print(t_url)
                self.get_html_from_url(t_url, cal)
            except KeyError:
                print(t_url + ' failed.')

        f = open('example.ics', 'wb')
        f.write(cal.to_ical())
        f.close()

    def create_events(self, cal, room, person, lecture_name, time_start, time_end, day):
        try:
            event = Event()
            event.add('summary', lecture_name[0].contents[0])
            event.add('dtstart', datetime(2019, int(day[0][1]), int(day[0][0]), int(time_start[1]), int(time_start[2]), 0, tzinfo=pytz.timezone('Europe/Berlin')))
            event.add('dtend', datetime(2019, int(day[0][1]), int(day[0][0]), int(time_end[1]), int(time_end[2]), 0, tzinfo=pytz.timezone('Europe/Berlin')))
            event.add('dtstamp', datetime.now())

            organizer = vCalAddress('MAILTO:platzhalter@lehre.dhbw-stuttgart.de')

            organizer.params['cn'] = vText(lecture_name[-1].contents[0])
            organizer.params['role'] = vText('CHAIR')
            event['organizer'] = organizer
            event['location'] = vText(lecture_name[-2].contents[0])

            event['uid'] = random.random() * 1000000000000000
            event.add('priority', 5)

            cal.add_component(event)
        except TypeError:
            return False

    def get_html_from_url(self, t_url, cal):
        """

        :param t_url: str
        """
        result = requests.get(url=t_url)
        f = open('rapla.html', 'wb')
        f.write(result.content)
        f.close()
        soup = BeautifulSoup(result.content, features='html.parser')

        #result = open('rapla.html', 'r')
        #if result.mode == 'r':
        #    contents = result.read()

        #soup = BeautifulSoup(contents, features='html.parser')
        samples = soup.find_all(attrs={'class': 'week_block'})
        date = soup.find_all(attrs={'class': 'week_header'})
        dates = {}
        # Creates list with assigned days FORMAT: MO -> {01,01}
        for x in date:
            if 'Mo' in x.text:
                dates['Mo'] = re.findall('(\d\d).(\d\d)', x.text)
            if 'Di' in x.text:
                dates['Di'] = re.findall('(\d\d).(\d\d)', x.text)
            if 'Mi' in x.text:
                dates['Mi'] = re.findall('(\d\d).(\d\d)', x.text)
            if 'Do' in x.text:
                dates['Do'] = re.findall('(\d\d).(\d\d)', x.text)
            if 'Fr' in x.text:
                dates['Fr'] = re.findall('(\d\d).(\d\d)', x.text)

        for lec in samples:
            room = lec.find_all('span', attrs={'class': 'resource'})
            person = lec.find('span', attrs={'class': 'person'})
            lecture_name = lec.find_all('td', attrs={'class': 'value'})
            day = lec.find_all('div')
            day_exact = re.findall("\w\w ", day[-1].contents[0])
            dayA = dates[day_exact[0].strip()]
            time = re.findall("((\d{2}):(\d{2}))", lec.contents[0].text)
            time_start = time[0]
            time_end = time[1]
            try:
                self.create_events(cal, room, person, lecture_name, time_start, time_end, dayA)
            except TypeError:
                return False

    def compose_url(self, t_url, t_key, t_day, t_month, t_year):
        """
        Composes the url
        :param t_url: str
        :param t_key: str
        :param t_day: str
        :param t_month: str
        :param t_year: str
        :return:
        """
        return t_url + "key=" + t_key + "&day=" + t_day + "&month=" + t_month + "&year=" + t_year