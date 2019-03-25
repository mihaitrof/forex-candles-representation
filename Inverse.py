from Parity import *
from Database import *
from CandleStick import *

class Inverse:

    def __init__(self, parity):
        self.parity           = parity
        self.max              = self.get_max()
        self.min              = self.get_min()
        self.range            = self.get_range()
        self.intervals        = self.set_intervals()
        self.candles_on_level = self.get_chandles_on_level()
        self.inverse          = {'up': [], 'down':[]}
        self.max_inverse      = []
        self.min_inverse      = []
        self.up_trend         = []
        self.down_trend       = []
        self.level_lines      = []

    def get_max(self):
        max = 0
        for index, candle in enumerate(self.parity.chart):
            c = CandleStick(self.parity, index)
            if c.state == 'bearish':
                if max <= c.open:
                    max = c.open
            else:
                if max <= c.close:
                    max = c.close
        return max

    def get_min(self):
        min = self.parity.chart[0]['open']
        for index, candle in enumerate(self.parity.chart):
            c = CandleStick(self.parity, index)
            if c.state == 'bearish':
                if min >= c.close:
                    min = c.close
            else:
                if min >= c.open:
                    min = c.open
        return min

    def get_range(self):
        return (self.max - self.min) / 30

    def set_intervals(self):
        data = {}
        rang = self.min
        data[0] = rang
        for i in range(1, 32):
            data[i] = rang + self.range
            rang += self.range
        return data

    def get_chandles_on_level(self):
        data = {}
        for index, candle in enumerate(self.parity.chart):

            for j, interval in enumerate(self.intervals):
                if j < 31 and candle['open'] >= self.intervals[j] and candle['open'] < self.intervals[j + 1]:
                    data[index] = j
        return data

    def big_deal(self, int1, int2, ok = 1):
        line  = self.candles_on_level[int1]
        first = int1
        last  = int2
        int1  = 0
        int2  = 0
        data  = self.candles_on_level

        for i in range(first, last):
            if data[i] == line and int2 != 0 and int1 != int2:
                self.push_inverse(int1, int2, line)
                self.level_lines.append((int1, int2))
                self.big_deal(int1, int2, ok = 0)
                int1 = 0
                int2 = 0
            if data[i] != line and int1 != 0:
                int2 = i

            if data[i] != line and int1 == 0:
                int1 = i


        if ok == 1 and self.get_last_candle_having_certain_level(line) < last:
            self.big_deal(self.get_last_candle_having_certain_level(line) + 1, last)

    def push_inverse(self, int1, int2, line):

        if self.candles_on_level[int1] >= self.candles_on_level[int1 - 1]:
            self.inverse['up'].append({'int1': int1, 'int2': int2, 'line': line})
            self.max_elem_from_inverse(int1, int2)
            # self.min_inverse.append(int1)
            # self.min_inverse.append(int2)
        else:
            self.inverse['down'].append({'int1': int1, 'int2': int2, 'line': line})
            self.min_elem_from_inverse(int1, int2)
            # self.max_inverse.append(int1)
            # self.max_inverse.append(int2)

    def get_last_candle_having_certain_level(self, line):

        aux = 0
        for index, candle in enumerate(self.candles_on_level):
            if self.candles_on_level[index] == line:
                aux = index
        return aux

    def max_elem_from_inverse(self, int1, int2):

        max = 0
        i   = 0
        for index in range(int1, int2 + 1):
            c = CandleStick(self.parity, index)
            if c.state == 'bearish':
                if max < c.open:
                    max = c.open
                    i = index
            else:
                if max <= c.close:
                    max = c.close
                    i = index

        self.max_inverse.append(i)
        return i

    def min_elem_from_inverse(self, int1, int2):

        min = self.parity.chart[int1]['open']
        i   = 0
        for index in range(int1, int2 + 1):
            c = CandleStick(self.parity, index)
            if c.state == 'bearish':
                if min > c.close:
                    min = c.close
                    i = index
            else:
                if min >= c.open:
                    min = c.open
                    i = index
        self.min_inverse.append(i)
        return i

    def up_inverse(self):

        data = []
        for index in self.inverse['up']:
            for j in range(index['int1'], index['int2'] + 1):
                data.append(j)
        return data

    def down_inverse(self):

        data = []
        for index in self.inverse['down']:
            for j in range(index['int1'], index['int2'] + 1):
                data.append(j)
        return data


    def up_trends(self):
        data = []
        for index in self.inverse['up']:
            max = self.max_elem_from_inverse(index['int1'], index['int2'])
            for j in range(index['int1'], max + 1):
                data.append(j)

        for index in self.inverse['down']:
            min = self.min_elem_from_inverse(index['int1'], index['int2'])
            for j in range(min, index['int2'] + 1):
                data.append(j)

        return data

    def down_trends(self):
        data  = []
        for index in self.inverse['down']:
            min = self.min_elem_from_inverse(index['int1'], index['int2'])
            for j in range(index['int1'], min + 1):
                data.append(j)

        for index in self.inverse['up']:
            max = self.max_elem_from_inverse(index['int1'], index['int2'])
            for j in range(max, index['int2'] + 1):
                data.append(j)

        return data

    def set_level_lines(self):
        data     = {}
        elements = []
        level    = 0

        for index in self.inverse['up']:
            min = self.min_elem_from_inverse(index['int1'], index['int2'])
            for j in range(index['int1'], index['int2'] + 1):
                c = CandleStick(self.parity, min)
                try:
                    data[j].append({'pos': c.close, 'level': level})
                except KeyError:
                    data[j] = []
                    data[j].append({'pos': c.close, 'level': level})
                elements.append(j)
            level += 1

        for index in self.inverse['down']:
            max = self.max_elem_from_inverse(index['int1'], index['int2'])
            for j in range(index['int1'], index['int2'] + 1):
                c = CandleStick(self.parity, max)
                try:
                    data[j].append({'pos': c.open, 'level': level})
                except KeyError:
                    data[j] = []
                    data[j].append({'pos': c.open, 'level': level})
                elements.append(j)
            level += 1

        return data, elements





