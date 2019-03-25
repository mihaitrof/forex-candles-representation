import csv
import os
import logging
import datetime
import requests
from bs4 import BeautifulSoup

from Parity import *
from LinearRegression import *
import glob
from pathlib import Path
import psycopg2
from Database import *
from CandleStick import *
from Elliot_waves import *
from Analysis import *
from Fundamental import *
from Inverse import *
from CandleStick import *
from Simulation import *

if __name__ == "__main__":
    logging.info('[START] Starting... _____________________________________________ ')
    update_data()

    p1 = Parity('EUR', 'USD', 30)
    # print(p1.chart[3474])

    # print(str(p1.chart[2270]['day']) == '2018-05-05')
    # linear = LinearRegression(p1, 'close', start=1, end=4)

    # print(linear.open)
    # print(linear.calculus())

    # PostgresSQL
    # db = Database()
    # cc = db.get_data('EUR', 'USD', 5, """'2018-05-29'""", """'14:30:00'""")
    # db.create_fundamental_analysis_table('fundamental')

    # def get_all_bullish_engulfing():
    #     candles = list()
    #     for index, value in enumerate(p1.chart):
    #         c = CandleStick(p1, index)
    #         if c.is_three_inside_up():
    #             candles.append(c.chart[index])
    #             print(c.chart[index]['day'], c.chart[index]['hour'])
    #     return len(candles)

    # print(get_all_bullish_engulfing())

    # c = CandleStick(p1, 150)
    # print(c.types)

    # Trenduri si figuri de intoarcere

    technical = Analysis(p1)
    # print(technical.level_line_min())
    # bullish = technical.get_bullish_candlesticks(1)
    # bearish = technical.get_bearish_candlesticks(1)
    # bullish_atts = technical.get_close_attribute(bullish)
    # bearish_atts = technical.get_close_attribute(bearish)
    # bullish_trend = technical.get_bullish_trends(bullish_atts)
    # bearish_trend = technical.get_bearish_trends(bearish_atts)
    #
    # bullish_trend.update(bearish_trend)
    # print(bullish_trend)

    # Request python
    # params = (
    #     ('day', 'jun11.2018'),
    # )
    #
    # response = requests.get('https://www.forexfactory.com/calendar.php', params=params)
    #
    # soup = BeautifulSoup(response.text, 'html.parser')
    # currencies = soup.findAll("td", class_="calendar__cell calendar__currency currency ")
    # events_name = soup.findAll("span", class_="calendar__event-title")
    # impact = soup.findAll("div", class_="calendar__impact-icon calendar__impact-icon--screen")
    # # print(impact[0].find('span').attrs['title'])
    #
    # forecast = soup.findAll("td", class_="calendar__cell calendar__forecast forecast")
    # previous = soup.findAll("td", class_="calendar__cell calendar__previous previous")
    # actual   = soup.findAll("td", class_="calendar__cell calendar__actual actual")
    # time     = soup.findAll("td", class_="calendar__cell calendar__time time")
    #
    # forex_factory = {}
    # t = []
    # timing        = {"am" : {"12": "07", "1": "08", "2": "09", "3": "10", "4":"11", "5":"12", "6":"13", "7":"14", "8":"15", "9":"16", "10":"17", "11":"18"},
    #                  "pm":  {"12": "19", "1": "20", "2": "21", "3": "22", "4": "23", "5": "00", "6": "01", "7": "02", "8": "03", "9": "04", "10": "05", "11": "06"}
    #                  }
    #
    # for i in range(0, len(currencies)):
    #     forex_factory[currencies[i].text[1:-1]] = []
    #     t.append(time[i].text)
    #     if len(t[-1]) == 0:
    #         t[-1] = t[i-1]
    #     # print(t[-1], currencies[i].text[1:-1])
    #
    # for i in range(0, len(currencies)):
    #     info = {}
    #     info['event_name'] = events_name[i].text
    #     info['impact'] = impact[i].find('span').attrs['title']
    #     info['forecast'] = forecast[i].text
    #     info['previous'] = previous[i].text
    #     info['actual'] = actual[i].text
    #     info['time'] = timing[t[i][-2:]][t[i].split(':')[0]] + ":" + t[i].split(':')[1]
    #
    #     forex_factory[currencies[i].text[1:-1]].append(info)
    #
    # print(forex_factory)


    # aux = 0
    # for index, elem in enumerate(p1.chart):
    #
    #     if aux != str(p1.chart[index]['day']) and index >= 2270:
    #         # print(str(p1.chart[index]['day']))
    #         aux = str(p1.chart[index]['day'])
    #         f = Fundamental(str(p1.chart[index]['day']))
    #         f.insert_date()


    # print(x)
    # for value in x:
    #     for i in x[value]:
    #         print(value, i)

    # f = Database()
    # # print(f.get_data())
    # parity = {}
    # day = {}
    # hour = {}
    #
    # for x in f.get_fundamental_data():
    #     parity[x[0]] = {}
    #
    # for x in f.get_fundamental_data():
    #     parity[x[0]][str(x[1])] = {str(x[2]):[x[3], x[4], x[5], x[6], x[7]]}
    #
    # data = list()
    # for index, candle in enumerate(p1.chart):
    #     fund = {}
    #     color = {"Low": 'green', 'Medium': 'yellow', 'High':'red'}
    #     data.append(candle)
    #     data[-1]['day'] = str(data[-1]['day'])
    #     data[-1]['hour'] = str(data[-1]['hour'])
    #     c = CandleStick(p1, index)
    #
    #
    #     try:
    #         # print(p1.base, data[-1]['day'], data[-1]['hour'])
    #         info = [parity[p1.base][data[-1]['day']][data[-1]['hour']][0],
    #                 parity[p1.base][data[-1]['day']][data[-1]['hour']][2],
    #                 parity[p1.base][data[-1]['day']][data[-1]['hour']][3],
    #                 parity[p1.base][data[-1]['day']][data[-1]['hour']][4]]
    #
    #         fund['status'] = [color[parity[p1.base][data[-1]['day']][data[-1]['hour']][1].split(" ")[0]], info]
    #         data[-1]['fund'] = fund
    #     except KeyError:pass
    #     try:
    #         info = [parity[p1.base][data[-1]['day']][data[-1]['hour']][0],
    #                 parity[p1.base][data[-1]['day']][data[-1]['hour']][2],
    #                 parity[p1.base][data[-1]['day']][data[-1]['hour']][3],
    #                 parity[p1.base][data[-1]['day']][data[-1]['hour']][4]]
    #
    #         fund['status'] = [color[parity[p1.quote][data[-1]['day']][data[-1]['hour']][1].split(" ")[0]], info]
    #         data[-1]['fund'] = fund
    #     except KeyError:pass
    # print(data)

    # Ellit waves___________________________________________________
    # elliot = Elliot_waves(p1)
    # print(elliot.inverse_down(elliot.level_line_max()))
    # print(elliot.level_line_min())


    # Inverse _______________________________________________________
    # inverse = Inverse(p1)
    # max = inverse.max
    # min = inverse.min
    #
    #
    # inverse.big_deal(0, len(inverse.parity.chart) - 1)
    # print(inverse.candles_on_level)
    # print(inverse.set_level_lines())
    # print(inverse.down_trends())
    # print(inverse.max_inverse)
    # d = {'x': []}
    # d['x'].append(12)
    # print(d)

    # Candlesticks________________________________________________
    # c = CandleStick(p1, 1)
    # print(c.types)

    # Simulation __________________________________________________
    s = Simulation(p1)
    print(s.get_coordinates())
    # print(s.get_trends()[0])
    # print(s.is_beginning_of_trend(1550))
    # print(s.is_on_level(140))

    # print(inverse.get_last_candle_having_certain_level(25))

    # Fundamental __________________________________
    # f = Database()
    # parity = {}
    # for x in f.get_fundamental_data():
    #     parity[x[0]] = {}
    #
    # for x in f.get_fundamental_data():
    #     parity[x[0]][str(x[1])] = {str(x[2]): [x[3], x[4], x[5], x[6], x[7]]}
    #
    # print(parity)

    # Logging the end
    logging.info('[END] The end. ')


