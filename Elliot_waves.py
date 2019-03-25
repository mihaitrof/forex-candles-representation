from Analysis import *

class Elliot_waves:

    def __init__(self, parity):

        self.parity = parity
        technical = Analysis(self.parity)

        aux = technical.get_bearish_candlesticks()
        atts = technical.get_close_attribute(aux)
        bearish_trend = technical.get_bearish_trends(atts)
        self.max_points = []
        self.min_points = []

        aux = technical.get_bullish_candlesticks()
        atts = technical.get_close_attribute(aux)
        bullish_trend = technical.get_bullish_trends(atts)

        self.x = self.group_trends(self.remove_duplicate(bearish_trend, bullish_trend))
        self.y = self.group_trends(bullish_trend)

        self.general_elliot()

    def level_line_max(self):
        technical = Analysis(self.parity)
        data = {}
        for i in self.max_points:
            for j in self.max_points:
                if i != j:
                    if technical.is_same_line_max(i, j) == 1:
                        data[min(i, j)] = max(i, j)
        return data

    def level_line_min(self):
        technical = Analysis(self.parity)
        data = {}
        for i in self.min_points:
            for j in self.min_points:
                if i != j:
                    if technical.is_same_line_min(i, j) == 1:
                        data[min(i, j)] = max(i, j)
        return data

    def inverse_down(self, data):
        elements = []
        for i in data:
            for j in range(i, data[i] + 1):
                elements.append(j)
        return elements

    def inverse_up(self, data):
        elements = []
        for i in data:
            for j in range(i, data[i] + 1):
                elements.append(j)
        return elements

    def parse_data(self, data):
        list_data = []
        for i in data:
            list_data.append(i)
            list_data.append(data[i])
        return list_data

    def get_trends_from_trend(self):

        trends = self.find_waves()
        trends.sort()

        data = []
        aux  = []
        for index, value in enumerate(trends):
            if trends[index] == trends[index - 1] + 1:
                aux.append(trends[index - 1])
            else:
                aux.append(trends[index - 1])
                data.append(aux)
                aux = []

        data = data[1:]
        # print(len(data))
        for k in range(0, len(data)):
            n = data[k][-1]
            i = data[k][0]
            chart = self.parity.chart[i: n +1]
            a_max = {}
            a_min = {}
            min = chart[0]['close']
            max = 0
            c = 0

            for index, value in enumerate(chart):
                cand = CandleStick(self.parity, index + i)
                if cand.state == 'bearish':
                    state = 'open'
                else:
                    state = 'close'
                if(value[state] > max):
                    max = value[state]
                    c = index
                try:
                    a_max[c + i] += 1
                except KeyError:a_max[c + i] = 1

            for index, value in enumerate(chart):
                cand = CandleStick(self.parity, index + i)
                if cand.state == 'bearish':
                    state = 'close'
                else:
                    state = 'open'
                if(value[state] < min):
                    min = value[state]
                    c = index
                try:
                    a_min[c + i] += 1
                except KeyError:a_min[c + i] = 1

            top_three_max = [0, 0, 0]
            top_three_min = [0, 0, 0]
            for i in a_max:
                if a_max[i] > top_three_max[-1]:
                    top_three_max[-1] = a_max[i]
                    top_three_max.sort(reverse=True)

            for i in a_min:
                if a_min[i] > top_three_min[-1]:
                    top_three_min[-1] = a_min[i]
                    top_three_min.sort(reverse=True)

            # top_min = self.remove_point_with_less_than_three_score(top_three_min)
            # top_max = self.remove_point_with_less_than_three_score(top_three_max)

            # print(a_max)
            # print(top_max)
            self.get_index_of_top_candles(a_max, top_three_max, True)
            self.get_index_of_top_candles(a_min, top_three_min, False)

    def remove_point_with_less_than_three_score(self, data):
        for i in data:
            if i < 4:
                data.remove(i)
        return data

    def general_elliot(self):

        a_max = {}
        a_min = {}
        min = self.parity.chart[0]['close']
        max = 0
        c = 0

        chart = self.parity.chart
        # max up
        for index, value in enumerate(chart):
            cand = CandleStick(self.parity, index)
            if cand.state == 'bearish':
                state = 'open'
            else:
                state = 'close'
            if (value[state] > max):
                max = value[state]
                c = index
            try:
                a_max[c] += 1
            except KeyError:
                a_max[c] = 1

        # max down
        max = 0
        for index in range(len(chart) - 1, -1 ,-1):
            cand = CandleStick(self.parity, index)
            if cand.state == 'bearish':
                state = 'open'
            else:
                state = 'close'
            if (chart[index][state] > max):
                max = chart[index][state]
                c = index
            try:
                a_max[c] += 1
            except KeyError:
                a_max[c] = 1

        # min up
        for index, value in enumerate(chart):
            cand = CandleStick(self.parity, index)
            if cand.state == 'bearish':
                state = 'close'
            else:
                state = 'open'
            if (value[state] < min):
                min = value[state]
                c = index
            try:
                a_min[c] += 1
            except KeyError:
                a_min[c] = 1

        # print(a_max)
        # print(a_min)

        top_three_max = self.limit_candles(a_max)
        top_three_min = self.limit_candles(a_min)

        top_three_max.sort()
        top_three_min.sort()

        self.max_points = top_three_max
        self.min_points = top_three_min
        # print("Max points first ", self.max_points)
        self.more_tops(self.max_points)

    def top_filter_up(self, chart, x1, max_type = True):
        a_max = {}
        a_min = {}
        max_min = {}
        min_max = {}
        second_max = 10000
        second_min = 0
        max = 0
        min = 0
        for index, value in enumerate(chart):
            cand = CandleStick(self.parity, index + x1 + 1)
            if cand.state == 'bearish':
                state = 'open'
            else:
                state = 'close'
            if max_type == True:
                if (value[state] > max):
                    max = value[state]
                    c = index + x1 + 1

                    try:
                        a_max[c] += 1
                    except KeyError:
                        a_max[c] = 1

                if value[state] < second_max:
                    second_max = value[state]
                    c = index + x1 + 1
                    # print(c)

                    try:
                        max_min[c] += 1
                    except KeyError:
                        max_min[c] = 1

            else:
                if (value[state] < min):
                    min = value[state]
                    c = index + x1 +1

                    try:
                        a_min[c] += 1
                    except KeyError:
                        a_min[c] = 1


        # print(self.get_max_min(max_min))
        max_min.update(self.get_max_min(max_min))
        # print("max_min: ", max_min)
        # print("a_max: ", a_max)
        a_max.update(max_min)
        return a_max, a_min

    def top_filter_down(self, chart, x1, max_type = True):
        # max down
        a_max = {}
        a_min = {}
        max_min = {}
        min_max = {}
        second_max = 0
        second_min = 0
        max = 0
        min = 0
        for index in range(len(chart) - 1, -1, -1):
            cand = CandleStick(self.parity, index + x1)
            if cand.state == 'bearish':
                state = 'open'
            else:
                state = 'close'

            if max_type == True:
                if (chart[index][state] > max):
                    max = chart[index][state]
                    c = index + x1 + 1
                    try:
                        a_max[c] += 1
                    except KeyError:
                        a_max[c] = 1

                if chart[index][state] > second_max:
                    second_max = chart[index][state]
                    c = index + x1 + 1

                    try:
                        min_max[c] += 1
                    except KeyError:
                        min_max[c] = 1
            else:
                if (chart[index][state] < min):
                    max = chart[index][state]
                    c = index + x1 + 1

                    try:
                        a_min[c] += 1
                    except KeyError:
                        a_min[c] = 1

        max_min.update(self.get_max_min(max_min))
        a_max.update(max_min)
        return a_max, a_min

    def get_max_min(self, data):

        top_three_max = []
        for i in data:
            if data[i] > 3:
                top_three_max.append(data[i+1])
        return top_three_max


    def more_tops(self, data):

        x1 = data[3]
        for i in range(4, 5):
            x2 = data[i]

            chart = self.parity.chart[x1+1: x2-1]

            a_max = self.top_filter_up(chart, x1, True)[0]
            a_max.update(self.top_filter_down(chart, x1, True)[0])

            # a_min = self.top_filter_up(chart, x1, False)[1]
            # a_min.update(self.top_filter_down(chart, x1, False)[1])

            top_three_max = self.limit_candles(a_max)
            # top_three_min = self.limit_candles(a_min)
            top_three_max.sort()
            # top_three_min.sort()
            self.max_points += top_three_max
            # self.min_points += top_three_min

            x1 = x2
        self.max_points.sort()
        self.min_points.sort()

    def limit_candles(self, data):
        top_three_max = []
        for i in data:
            if data[i] > 3:
                top_three_max.append(i)
        return top_three_max

    def get_index_of_top_candles(self, a_data, data, max):
        j_max = 0
        j_min = 0
        # print(a_data)
        # print(data)
        for i in a_data:
            if a_data[i] in data:
                if max == True:
                        self.max_points.append(i)
                        j_max += 1
                else:
                        self.min_points.append(i)
                        j_min += 1
        # print(self.max_points)
        # print(self.min_points)
        # print("_____________")

    def group_trends(self, data):

        group = []
        var = []
        aux = list(data.keys())[0]
        for index, value in enumerate(data):

            if value == aux + 1 and index > 0:
                var.append(aux)
                aux = value
            else:
                var.append(aux)
                group.append(var)
                var = []
                aux = value
        return group[1:]

    def remove_duplicate(self, x, y):

        for i in y:
            try:
                del x[i]
            except KeyError:continue

        return x

    def find_waves(self):

        data = {}
        for value in (self.x):
            data[value[0]] = 0
            data[value[-1]] = 0

        for value in (self.y):
            data[value[0]] = 1
            data[value[-1]] = 1

        # print(data_x)
        # print(data)
        pairs = []
        for value in data:
            aux = value

            for k in range(aux + 1, aux + 3):
                try:
                    # print(aux, k, data[aux], data[k])
                    if data[k] != data[aux]:
                        pairs.append(aux)
                        pairs.append(k)
                except KeyError:pass

        final = {}
        for i in self.x + self.y:

            try:
                if i[-1] in pairs:
                    for j in i:
                        final[j] = 'yes'

                if i[0] in pairs:
                    for j in i:
                        final[j] = 'yes'
            except IndexError:pass

        return self.remove_duplicates(final)

    def remove_duplicates(self, values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output








