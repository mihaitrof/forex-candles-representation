from CandleStick import *
from Analysis import *
from Inverse import *
class Simulation:

    def __init__(self, parity, start, end):
        self.parity       = parity
        self.start = start
        self.end   = end
        self.candlesticks = {'spinning_top'     : 'neutral',
                             'doji'             : 'neutral',
                             'long_legged_doji' : 'neutral',
                             'dragonfly_doji'   : 'bullish',
                             'gravestone_doji'  : 'bearish',
                             'marubozu'         : 'neautral',
                             'hammer'           : 'bullish',
                             'hanging_man'      : 'bearish',
                             'inverted_hammer'  : 'bullish',
                             'shooting_star'    : 'bearish',
                             'bullish_engulfing': 'bullish',
                             'bearish_engulfing': 'bullish',
                             'tweezer_tops'     : 'bearish',
                             'tweezer_bottoms'  : 'bullish',
                             'morning_star'     : 'bullish',
                             'evening_star'     : 'bearish',
                             'three_white_soldiers' : 'bullish',
                             'three_black_crows':'bearish',
                             'three_inside_up': 'bullish',
                             'three_inside_down':'bearish'
                             }
        self.fundamental = self.set_fundamental()

    def get_coordinates(self):

        data = {}
        for index, candle in enumerate(self.parity.chart[self.start: self.end]):
            c = CandleStick(self.parity, index)
            trend       = self.points_trend(index)
            fund        = 0
            candlestick = self.points_candlesticks(index)
            level = 0
            if self.is_on_level(index) == True:
                level  = self.points_line_level(index)

            if self.is_fundamental(index):
                fund = self.points_fundamental(index)

            points = trend + fund + candlestick + level
            if points > 0:
                data[index] = {'x': index, 'y': c.body * 0.1 * points + c.high}
            else:
                data[index] = {'x': index, 'y': c.body * 0.1 * points + c.low}

        return data

    def points_trend(self, index):
        trend = 0
        x = self.is_beginning_of_trend(index)
        if  x == 'bullish':
            trend = 4
        if x == 'bearish':
            trend = -4
        return trend

    def points_candlesticks(self, index):
        c = CandleStick(self.parity, index)
        c.set_types()
        trend = 0
        if c.types:
            for i in c.types:
                if self.candlesticks[i] == 'bullish':
                    trend += 2
                if self.candlesticks[i] == 'bearish':
                    trend += -2
        return trend

    def points_line_level(self, index):
        points = 0
        inverse = Inverse(self.parity)
        inverse.big_deal(0, len(inverse.parity.chart) - 1)
        arr = inverse.inverse
        # print(arr)
        up   = arr['up']
        down = arr['down']

        for i in up:
            try:
                if i['int1'] <= index and i['int2'] >= index:
                    points = 3
            except KeyError:pass

        for i in down:
            try:
                if i['int1'] <= index and i['int2'] >= index:
                    points = -3
            except KeyError:pass

        return points

    def get_trends(self):
        technical = Analysis(self.parity)
        aux = technical.get_bearish_candlesticks()
        atts = technical.get_close_attribute(aux)
        bearish_trend = technical.get_bearish_trends(atts)

        aux = technical.get_bullish_candlesticks()
        atts = technical.get_close_attribute(aux)
        bullish_trend = technical.get_bullish_trends(atts)

        # inv = Inverse(self.parity)
        # inv.big_deal(0, len(inv.parity.chart) - 1)
        # bullish_trend_new = inv.up_trends()
        # bearish_trend_new = inv.down_trends()

        return bearish_trend, bullish_trend

    def is_beginning_of_trend(self, index):

        trend = {'bearish': 0, 'bullish': 0}
        up = self.get_trends()[1]
        down = self.get_trends()[0]
        # print(up)
        # print(down)
        for i in range(index - 5, index + 1):
            if i in up:
                trend['bullish'] += 1
            if i in down:
                trend['bearish'] += 1

        # print("__   " + str(trend['bearish']))
        # print("__   " + str(trend['bullish']))
        if trend['bullish'] >= 5:
            return 'bullish'
        if trend['bearish'] >= 5:
            return 'bearish'
        return 0

    def is_on_level(self, index):
        inv = Inverse(self.parity)
        inv.big_deal(0, len(inv.parity.chart) - 1)
        level_lines_el = inv.set_level_lines()[1]
        # print(index not in inv.up_inverse())
        ok = 0

        for i in range(index - 4, index + 1):
            if i in level_lines_el:
                ok += 1

        if ok >4:
            return 1
        return 0

    def set_fundamental(self):

        f = Database()
        parity = {}
        for x in f.get_fundamental_data():
            parity[x[0]] = {}

        for x in f.get_fundamental_data():
            parity[x[0]][str(x[1])] = {str(x[2]): [x[3], x[4], x[5], x[6], x[7]]}

        return parity

    def is_fundamental(self, index):
        base  = self.parity.base
        quote = self.parity.quote
        day   = str(self.parity.chart[index]['day'])
        hour  = str(self.parity.chart[index]['hour'])
        color = {"Low": 'green', 'Medium': 'yellow', 'High': 'red'}
        f = 0

        try:
            f = self.fundamental[base][day][hour]
        except KeyError:pass

        try:
            if color[self.fundamental[day][hour][1].split(" ")[0]] == 'red':
                f = self.fundamental[quote][day][hour]
        except KeyError:pass

        return f

    def points_fundamental(self, index):

        base = self.parity.base
        quote = self.parity.quote
        day = str(self.parity.chart[index]['day'])
        hour = str(self.parity.chart[index]['hour'])
        color = {"Low": 'green', 'Medium': 'yellow', 'High': 'red'}
        f = 0

        try:
            f = self.fundamental[base][day][hour]
        except KeyError:
            pass

        try:
            if color[self.fundamental[day][hour][1].split(" ")[0]] == 'red':
                f = self.fundamental[quote][day][hour]
        except KeyError:
            pass

        # print(f)
        actual = float(f[2][:-1])
        previous = float(f[4][:-1])

        # print(actual- previous)
        if previous - actual < 0:
            return -2
        else:
            return 2
