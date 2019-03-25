from bs4 import BeautifulSoup

from Parity import *
from Database import *
from CandleStick import *
import requests

class Fundamental:

    def __init__(self, date):

        self.data = {'01': ['jan', 31], '02': ['feb', 28], '03': ['mar', 31], '04': ['apr', 30], '05': ['may', 31], '06': ['jun', 30], '07': ['jul', 31], '08': ['aug', 31],
                '09': ['sep', 30], '10': ['oct', 31], '11': ['nov', 30], '12': ['dec', 31]}
        self.root_path = str(inspect.stack()[0][1])
        # Request python
        day = self.convert_date(date)
        self.segments_day = day[1]
        self.conn = psycopg2.connect(database="testdb", user="postgres", password="test123", host="db", port="5432")

        # print(self.segments_day[1])
        params = (
            ('day', day[0]),
        )
        response = requests.get('https://www.forexfactory.com/calendar.php', params=params)

        soup = BeautifulSoup(response.text, 'html.parser')
        self.currencies = soup.findAll("td", class_="calendar__cell calendar__currency currency ")
        self.events_name = soup.findAll("span", class_="calendar__event-title")
        self.impact = soup.findAll("div", class_="calendar__impact-icon calendar__impact-icon--screen")

        self.forecast = soup.findAll("td", class_="calendar__cell calendar__forecast forecast")
        self.previous = soup.findAll("td", class_="calendar__cell calendar__previous previous")
        self.actual = soup.findAll("td", class_="calendar__cell calendar__actual actual")
        self.time = soup.findAll("td", class_="calendar__cell calendar__time time")

    def generate(self):

        forex_factory = {}
        t = []
        timing = {
            "am": {"12": "07", "1": "08", "2": "09", "3": "10", "4": "11", "5": "12", "6": "13", "7": "14", "8": "15",
                   "9": "16", "10": "17", "11": "18"},
            "pm": {"12": "19", "1": "20", "2": "21", "3": "22", "4": "23", "5": "00", "6": "01", "7": "02", "8": "03",
                   "9": "04", "10": "05", "11": "06"},
            "ay": {"12": "00", "1": "00", "2": "00", "3": "00", "4": "00", "5": "00", "6": "00", "7": "00", "8": "00",
                   "9": "00", "10": "00", "11": "00"},
            "All Day": {"12": "00", "1": "00", "2": "00", "3": "00", "4": "00", "5": "00", "6": "00", "7": "00", "8": "00",
                   "9": "00", "10": "00", "11": "00"}
            }

        for i in range(0, len(self.currencies)):
            forex_factory[self.currencies[i].text[1:-1]] = []
            t.append(self.time[i].text)
            if len(t[-1]) == 0:
                t[-1] = t[i - 1]
            # print(t[-1], self.currencies[i].text[1:-1])

        for i in range(0, len(self.currencies)):
            info = {}
            # print(t[i][-2:])
            if t[i][-2:] not in ['am', 'pm']:
                continue
            info['event_name'] = self.events_name[i].text
            info['impact']     = self.impact[i].find('span').attrs['title']
            info['forecast']   = self.forecast[i].text
            info['previous']   = self.previous[i].text
            info['actual']     = self.actual[i].text
            info['hour']       = timing[t[i][-2:]][t[i].split(':')[0]] + ":" + t[i].split(':')[1][:-2]
            print("Loading...", self.segments_day)
            month = self.remove_zero_from_date(self.segments_day[1])
            day   = self.remove_zero_from_date(self.segments_day[2])

            if int(timing[t[i][-2:]][t[i].split(':')[0]]) < 7:
                day += 1
                # print(int(self.data[self.segments_day[1]][1]), self.segments_day[2])
                if int(self.data[self.segments_day[1]][1]) == int(self.segments_day[2]):
                    day   = 1
                    month += 1

            if day < 10:
                day = '0' + str(day)
            if month < 10:
                month = '0' + str(month)

            info['day']        = self.segments_day[0] + "-" + str(month) + "-" + str(day)
            forex_factory[self.currencies[i].text[1:-1]].append(info)

        return forex_factory

    def convert_date(self, date):

        segments = date.split("-")
        # print(segments[1])
        year     = segments[0]
        month    = segments[1]
        day      = segments[2]

        param = self.data[month][0] + day + '.' + year
        return param, segments

    def remove_zero_from_date(self, data):

        if data[0] == '0':
            return int(data[1][-1])
        else:
            return int(data)

    # Insert data into database
    def insert_row(self, table_name, data):

        """Insert data in certain table
        """
        function_path = str(inspect.stack()[0][3])

        sql = """INSERT INTO """ + table_name + """(currency, day, hour, event_name, impact, forecast, previous, actual) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
        # print(sql)
        try:
            # create a new cursor
            cur = self.conn.cursor()
            # execute the INSERT statement
            cur.executemany(sql, data)
            # commit the changes to the database
            self.conn.commit()
            # close communication with the database
            cur.close()

            # Logging...
            log_path(self.root_path, function_path)
            log_info(message='Data in ' + table_name + ' table inserted succesfully.')

        except (Exception, psycopg2.DatabaseError) as error:
             # Logging...
             log_path(self.root_path, function_path)
             log_error(message='Data can NOT be inserted in ' + table_name + ' table. ' + str(error))
             print(error)

    def insert_date(self):

        """Insert data for certain parity.
        """
        function_path = str(inspect.stack()[0][3])
        x = self.generate()
        for value in x:
            data = list()
            for i in x[value]:
                data.append([value, i['day'], i['hour'], i['event_name'], i['impact'], i['forecast'], i['previous'], i['actual']])
                self.insert_row('fundamental', data)
                # Logging...
                log_path(self.root_path, function_path)
                log_info(message='Success!')

