from Parity import *
from Database import *
from CandleStick import *

class Analysis:

    def __init__(self, parity, start = False, end = False):

        self.parity = parity
        if start != False and end != False:
            self.chart = self.parity.chart[int(start):int(end)]
        else:
            self.chart = self.parity.chart

    def get_bearish_candlesticks(self, limit = 0):
        """ This method returns pairs of indexes. These pairs represent the bearish candlesticks of a specific parity. """
        desc = []
        length = 0
        pos = 0
        data = []

        for index, candle in enumerate(self.chart):
            c1 = CandleStick(self.parity, index)
            if c1.state == 'bearish':
                desc.append(index)

        for index, value in enumerate(desc):
            # print(desc[index], (desc[index - 1]) + 1)
            if desc[index] == (desc[index - 1] + 1):
                # print('Yes')
                length += 1
            elif length > limit:
                data.append((pos, desc[index - 1]))
                pos = value
                length = 0
            else:
                pos = value
                length = 0

        return data

    def level_line_max(self):
        lines = {}
        gap = 0
        max1 = 0
        max2 = 0
        index1 = -1
        index2 = -1
        for index, candle in enumerate(self.chart):
            gap += 1
            c1 = CandleStick(self.parity, index)
            set_max1 = self.set_max1(gap, max1, c1, index)
            set_max2 = self.set_max2(gap, max2, c1, index)
            max1 = set_max1[0]
            max2 = set_max2[0]

            if set_max1[1] != -1:
                index1 = set_max1[1]
            if set_max2[1] != -1:
                index2 = set_max2[1]
            if self.is_same_line_max(index1, index2) == 1:
                lines[index1] = index2
                gap = 0
                max1 = 0
                max2 = 0
                index1 = -1
                index2 = -1
            else:
                if max1 > max2:
                    gap = 0
                    max1 = max2
                    max2 = 0
                    index1 = index2
                    index2 = -1
                else:
                    max2 = 0
                    index2 = -1
        return lines

    def set_max1(self, gap, max1, c1, index):
        ind = -1
        if gap < 10:
            if c1.close < c1.open:
                if max1 < c1.open:
                    max1 = c1.open
                    ind = index
            else:
                if max1 < c1.close:
                    max1 = c1.close
                    ind = index

        return max1, ind

    def set_max2(self, gap, max2, c1, index):
        ind = -1
        if gap > 10:
            if c1.close < c1.open:
                if max2 < c1.open:
                    max2 = c1.open
                    ind = index
            else:
                if max2 < c1.close:
                    max2 = c1.close
                    ind = index

        return max2, ind

    def level_line_min(self):
        lines = {}
        gap   = 0
        min1 = 100
        min2 = 100
        index1 = -1
        index2 = -1
        for index, candle in enumerate(self.chart):
            gap += 1
            c1 = CandleStick(self.parity, index)
            set_min1 = self.set_min1(gap, min1, c1, index)
            set_min2 = self.set_min2(gap, min2, c1, index)
            min1 = set_min1[0]
            min2 = set_min2[0]

            if set_min1[1] != -1:
                # print('asd')
                index1 = set_min1[1]
            if set_min2[1] != -1:
                index2 = set_min2[1]
            if self.is_same_line_min(index1, index2) == 1:
                # print(min1, index1)
                # print(min2, index2)
                lines[index1] = index2
                gap = 0
                min1 = 100
                min2 = 100
                index1 = -1
                index2 = -1
            else:
                if min1 > min2:
                    gap = 0
                    min1 = min2
                    min2 = 100
                    index1 = index2
                    index2 = -1
                else:
                    min2 = 100
                    index2 = -1
        return lines

    def set_min1(self, gap, min1, c1, index):
        ind = -1
        if gap < 10:
            if c1.close < c1.open:
                if min1 > c1.close:
                    min1 = c1.close
                    ind = index
            else:
                if min1 > c1.open:
                    min1 = c1.open
                    ind = index

        return min1, ind

    def set_min2(self, gap, min2, c1, index):
        ind = -1
        if gap > 10:
            if c1.close < c1.open:
                if min2 > c1.close:
                    min2 = c1.close
                    ind = index
            else:
                if min2 > c1.open:
                    min2 = c1.open
                    ind = index
        # print('Final ' + str(ind) + ' ' + str(min2))
        return min2, ind

    def is_same_line_max(self, index1, index2):
        ok = 0

        c1 = CandleStick(self.parity, index1)
        c2 = CandleStick(self.parity, index2)

        if c1.state == 'bullish':
            part1 = (c1.body / 2) + c1.close
        else:
            part1 = (c1.body / 2) + c1.open

        if c2.state == 'bullish':
            part2 = (c2.body / 2) + c2.close
        else:
            part2 = (c2.body / 2) + c2.open

        if index1 != -1 and index2 != -1:
            if c1.state == 'bullish':
                if c1.close > c2.low and c1.close < part2:
                    ok += 1
            else:
                if c1.open > c2.low and c1.open < part2:
                    ok += 1

            if c2.state == 'bullish':
                if c2.close > c1.low and c2.close < part1:
                    ok += 1
            else:
                if c2.open > c1.low and c2.open < part1:
                    ok += 1

        if ok == 2:
            return 1
        else:
            return 0

    def is_same_line_min(self, index1, index2):
        ok = 0

        c1 = CandleStick(self.parity, index1)
        c2 = CandleStick(self.parity, index2)

        if c1.state == 'bearish':
            part1 = (c1.body / 2) + c1.close
        else:
            part1 = (c1.body / 2) + c1.open

        if c2.state == 'bearish':
            part2 = (c2.body / 2) + c2.close
        else:
            part2 = (c2.body / 2) + c2.open

        if index1 != -1 and index2 != -1:
            if c1.state == 'bearish':
                if c1.close > c2.low and c1.close < part2:
                    ok += 1
            else:
                if c1.open > c2.low and c1.open < part2:
                    ok += 1

            if c2.state == 'bearish':
                if c2.close > c1.low and c2.close < part1:
                    ok += 1
            else:
                if c2.open > c1.low and c2.open < part1:
                    ok += 1

        if ok == 2:
            return 1
        else:
            return 0

    def get_bullish_candlesticks(self, limit = 0):
        """ This method returns pairs of indexes. These pairs represent the bullish candlesticks of a specific parity. """
        asc    = []
        length = 0
        pos    = 0
        data   = []

        for index, candle in enumerate(self.chart):
            c1 = CandleStick(self.parity, index)
            if c1.state == 'bullish':
                asc.append(index)

        for index, value in enumerate(asc):
            # print(desc[index], (desc[index - 1]) + 1)
            if asc[index] == (asc[index - 1] + 1):
                # print('Yes')
                length += 1
            elif length > limit:
                data.append((pos, asc[index - 1]))
                pos = value
                length = 0
            else:
                pos = value
                length = 0

        return data

    def get_close_attribute(self, data):
        close = []
        for candle in data:
            close.append((candle[0], self.chart[candle[1]]['close']))
            close.append((candle[1], self.chart[candle[1]]['close']))

        return close

    def get_bearish_trends(self, data, limit = 3):
        """This method returns the final bearish trends of a specific parity.

        :param data: get_close_attribute(data)
        :return: pairs
        """
        pairs = {}
        pair  = [data[0]]
        for i in range(0, len(data) - 1):
            if data[i][1] >= data[i + 1][1]:
                pair.append(data[i + 1])
            else:
                # pairs.append(pair)
                if (pair[-1][0] - pair[0][0]) > limit:
                    for j in range(pair[0][0], pair[-1][0] + 1):
                        pairs[j] = self.chart[j]['close']
                pair = [data[i + 1]]

        return pairs

    def get_trends_api(self, trends, bearish = True):
        data = list()
        for index, candle in enumerate(self.chart):
            data.append(candle)
            data[-1]['day'] = str(data[-1]['day'])
            data[-1]['hour'] = str(data[-1]['hour'])
            if index in trends:
                if bearish == True:
                    data[-1]['trends'] = 'bearish'
                else:
                    data[-1]['trends'] = 'bullish'

        # print(trends[11])
        total = len(self.chart)

        return data, total

    # Bullish

    def get_bullish_trends(self, data, limit = 3):
        """This method returns the final bullish trends of a specific parity.

        :param data: get_close_attribute(data)
        :return: pairs
        """
        pairs = {}
        pair  = [data[0]]
        for i in range(0, len(data) - 1):
            if data[i][1] <= data[i + 1][1]:
                pair.append(data[i + 1])
            else:
                # pairs.append(pair)
                if (pair[-1][0] - pair[0][0]) > limit:
                    for j in range(pair[0][0], pair[-1][0] + 1):
                        pairs[j] = self.chart[j]['close']
                pair = [data[i + 1]]

        return pairs

    def get_inverse_trends_api(self, bearish, bullish):
        data = list()
        for index, candle in enumerate(self.chart):
            data.append(candle)
            data[-1]['day'] = str(data[-1]['day'])
            data[-1]['hour'] = str(data[-1]['hour'])
            if index in bearish:
                data[-1]['trends'] = 'bearish'
            if index in bullish:
                data[-1]['trends'] = 'bullish'

        total = len(self.chart)
        return data, total


