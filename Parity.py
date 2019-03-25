import csv
import os
import logging
import inspect
from helpers import *
import math
from Database import *
from CandleStick import *

class Parity:
    """The declaration of parities.

    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        base(str): The base currency (e.g. in the quotation EUR/USD, EUR represents the base currency).
        quote(str): The quote currency(e.g. in the quotation EUR/USD, USD represents the quote currency).
        timeframe(int): The timeframe (represented as minutes) which the graphic is distributed.

    Attributes:
        base(str): The base currency (e.g. in the quotation EUR/USD, EUR represents the base currency).
        quote(str): The quote currency(e.g. in the quotation EUR/USD, USD represents the quote currency).
        timeframe(int): The timeframe (represented as minutes) which the graphic is distributed.
        chart(list): A chart is composed by many candlesticks. In our case, a chart has many candles.

    """
    def __init__(self, base, quote, timeframe):


        self.base = base.upper()
        self.quote = quote.upper()
        self.timeframe = timeframe
        self.chart = []
        self.line_number = str(inspect.stack()[0][2])
        self.root_path = str(inspect.stack()[0][1])
        self.set_chart()

    def set_chart(self):
        """ Get data from database and set the chart variable

        Attributes:
            db(Database)     : Instance of Database class.
            data(list)       : Data from table.

        """
        db   = Database()
        data = db.get_data(self.base, self.quote, self.timeframe)

        for candle in data:
            self.chart.append(parse_line(candle))

    def get_chart(self, page, limit):

        data  = list()
        limit = int(limit)
        page  = int(page)

        left  = (page-1)*50
        right = left + limit
        if right > len(self.chart):
            right = len(self.chart)
        for index in range(left, right):
            limit -= 1
            data.append(self.chart[index])
            data[-1]['day']  = str(data[-1]['day'])
            data[-1]['hour'] = str(data[-1]['hour'])

        total        = len(self.chart)
        count        = 50 - limit
        per_page     = 50
        current_page = page
        total_pages  = math.ceil(total / 50)

        return data, total, count, per_page, current_page, total_pages

    def get_full_chart(self):

        data = list()
        for candle in self.chart:
            data.append(candle)
            data[-1]['day'] = str(data[-1]['day'])
            data[-1]['hour'] = str(data[-1]['hour'])

        total = len(self.chart)
        return data, total

    def read_csv(self):
        """Open the file using input data. Every file name represents a concatenation between the parity
        value (e.g. EURUSD or EURGBP) and the timeframe (e.g. 60 or 1440).

        Attributes:
            fileName(str): The file name.
            reader(_csv): Line of CSV.
            row(list): List which sum up the information about a candle (e.g. date, open, high, low etc.).

        """

        function_path = str(inspect.stack()[0][3])
        logging.info('[PATH] ' + self.root_path + '/' + function_path)
        logging.info('[INFO] Taking data from CSVs...')
        fileName = get_data_path(self.base, self.quote, self.timeframe)

        with open(fileName, newline='') as File:
            reader = csv.reader(File)
            for row in reader:
                self.chart.append(parse_line(row))

        logging.info('[INFO] Done.')

