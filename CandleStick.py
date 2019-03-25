from Parity import *
from Database import *
import sys
sys.setrecursionlimit(2000)

class CandleStick:
    """This class aims to illustrate a candlestick. It is useful to identify the state and the type of a candlestick.

        Args:
            parity(Parity)   : Instance of Parity Class.
            candle_index(int): Index of candle in Parity.chart list.

        Attributes:
            chart(list)       : The chart of parity.
            candle_index(int) : Index of candle in chart.
            state(int)        : Bullish, bearish or steady.
            open(float)       :
            close(float)      :
            high(float)       :
            low(float)        :

        """

    def __init__(self, parity, candle_index):

        state             = ['bullish', 'bearish', 'neutral']
        self.parity       = parity
        self.chart        = parity.chart
        self.candle_index = candle_index
        self.state        = state[self.get_type(candle_index)]
        self.open         = self.chart[self.candle_index]['open']
        self.close        = self.chart[self.candle_index]['close']
        self.high         = self.chart[self.candle_index]['high']
        self.low          = self.chart[self.candle_index]['low']
        shadows           = self.set_shadows()
        self.upper_shadow = shadows[0]
        self.lower_shadow = shadows[1]
        self.body         = self.set_body()
        self.types        = []

    def set_types(self):
        if self.is_spinning_top():
            self.types.append('spinning_top')
        if self.is_doji():
            self.types.append('doji')
        if self.is_long_legged_doji():
            self.types.append('long_legged_doji')
        if self.is_dragonfly_doji():
            self.types.append('dragonfly_doji')
        if self.is_gravestone_doji():
            self.types.append('gravestone_doji')
        if self.is_marubozu():
            self.types.append('marubozu')
        if self.is_hammer():
            self.types.append('hammer')
        if self.is_hanging_man():
            self.types.append('hanging_man')
        if self.is_inverted_hammer():
            self.types.append('inverted_hammer')
        if self.is_shooting_star():
            self.types.append('shooting_star')
        if self.is_bullish_engulfing():
            self.types.append('bullish_engulfing')
        if self.is_bearish_engulfing():
            self.types.append('bearish_engulfing')
        if self.is_tweezer_tops():
            self.types.append('tweezer_tops')
        if self.is_tweezer_bottoms():
            self.types.append('tweezer_bottoms')
        if self.is_morning_star():
            self.types.append('morning_star')
        if self.is_evening_star():
            self.types.append('evening_star')
        if self.is_three_white_soldiers():
            self.types.append('three_white_soldiers')
        if self.is_three_black_crows():
            self.types.append('three_black_crows')
        if self.is_three_inside_up():
            self.types.append('three_inside_up')
        if self.is_three_inside_down():
            self.types.append('three_inside_down')

    def set_body(self):

        if self.state == 'bullish':
            return self.close - self.open
        if self.state == 'bearish':
            return self.open - self.close
        return 0

    def set_shadows(self):

        upper_shadow = 0
        lower_shadow = 0
        if self.state == 'bullish':
            upper_shadow = self.high - self.close
            lower_shadow = self.open - self.low

        if self.state == 'bearish':
            upper_shadow = self.high - self.open
            lower_shadow = self.close - self.low

        if self.state == 'neutral':
            upper_shadow = self.high - self.open
            lower_shadow = self.close - self.low

        return upper_shadow, lower_shadow

    def is_doji(self):

        if self.state == 'neutral' and self.upper_shadow == 0 and self.lower_shadow == 0:
            return 1
        return 0

    def is_long_legged_doji(self):

        if self.state == 'neutral' and self.is_doji() == 0:
            return 1
        return 0

    def is_dragonfly_doji(self):

        if self.state == 'neutral' and self.upper_shadow == 0 and self.lower_shadow >= 0.0001:
            return 1
        return 0

    def is_gravestone_doji(self):

        if self.state == 'neutral' and self.upper_shadow >= 0.0001 and self.lower_shadow == 0:
            return 1
        return 0

    def is_spinning_top(self):

        if self.upper_shadow >= 2*self.body and self.lower_shadow >= 2*self.body and self.state != 'neutral' and self.body > 0.0001:
            return 1
        return 0

    def is_bullish_engulfing(self):

        open1   = self.chart[self.candle_index - 1]['open']
        close1  = self.chart[self.candle_index - 1]['close']

        open2   = self.open
        close2  = self.close

        if self.state == 'bullish' and self.get_type(self.candle_index-1) == 1:
            if close1 > open2 and open1 < close2 and self.body > 2 * (open1-close1):
                # print(open1, close1)
                # print(open2, close2)
                return 1
        return 0

    def is_bearish_engulfing(self):

        open1 = self.chart[self.candle_index - 1]['open']
        close1 = self.chart[self.candle_index - 1]['close']

        open2 = self.open
        close2 = self.close

        if self.state == 'bearish' and self.get_type(self.candle_index - 1) == 0:
            if close1 < open2 and open1 > close2 and self.body < 2 * (close1 - open1):
                return 1
        return 0

    def is_marubozu(self):

        if self.state == 'bullish':
            if self.open == self.low and self.close == self.high:
                return 1

        if self.state == 'bearish':
            if self.open == self.high and self.close == self.low:
                return 1

        return 0

    def is_hammer(self):

        if self.state == 'bullish' and self.upper_shadow <= self.body and self.lower_shadow >= 5*self.body:
            return 1
        return 0

    def is_hanging_man(self):

        if self.state == 'bearish' and self.upper_shadow <= self.body and self.lower_shadow >= 5*self.body:
            return 1
        return 0

    def is_inverted_hammer(self):

        if self.state == 'bullish' and self.lower_shadow <= self.body and self.upper_shadow >= 5*self.body:
            return 1
        return 0

    def is_shooting_star(self):

        if self.state == 'bearish' and self.lower_shadow <= self.body and self.upper_shadow >= 5*self.body:
            return 1
        return 0

    def is_tweezer_tops(self):

        open1  = self.chart[self.candle_index - 1]['open']
        close1 = self.chart[self.candle_index - 1]['close']
        low1   = self.chart[self.candle_index - 1]['low']
        high1  = self.chart[self.candle_index - 1]['high']

        open2  = self.open
        close2 = self.close
        low2   = self.low
        high2 = self.high

        if self.state == 'bearish' and self.get_type(self.candle_index - 1) == 0:
            if abs(high1 - high2) <= 0.1 * self.body and abs(close1 - open2) < 0.2 * self.body and abs(open1 - close2) < 0.2 * self.body:
                # print(open1, close2)
                return 1
        return 0

    def is_tweezer_bottoms(self):

        open1  = self.chart[self.candle_index - 1]['open']
        close1 = self.chart[self.candle_index - 1]['close']
        low1   = self.chart[self.candle_index - 1]['low']
        high1  = self.chart[self.candle_index - 1]['high']

        open2  = self.open
        close2 = self.close
        low2   = self.low
        high2 = self.high

        if self.state == 'bullish' and self.get_type(self.candle_index - 1) == 1:
            if abs(low1 - low2) <= 0.1 * self.body and abs(close2 - open1) < 0.2 * self.body and abs(open2 - close1) < 0.2 * self.body:
                # print(abs(low1 - low2), self.body)
                return 1
        return 0

    def is_morning_star(self):

        c1 = CandleStick(self.parity, self.candle_index - 2)
        c2 = CandleStick(self.parity, self.candle_index - 1)

        if c1.state == 'bearish' and c2.is_long_legged_doji() and self.state == 'bullish' and self.close > (c1.close + c1.open) / 2:
            return 1
        return 0

    def is_evening_star(self):

        c1 = CandleStick(self.parity, self.candle_index - 2)
        c2 = CandleStick(self.parity, self.candle_index - 1)

        if c1.state == 'bullish' and c2.is_long_legged_doji() and self.state == 'bearish' and self.close < (c1.close + c1.open) / 2:
            return 1
        return 0

    def is_three_white_soldiers(self):

        c1 = CandleStick(self.parity, self.candle_index - 2)
        c2 = CandleStick(self.parity, self.candle_index - 1)

        if  c1.state == 'bullish' and \
            c2.state == 'bullish' and \
            self.state == 'bullish' and \
            c2.low > c1.open and \
            c2.close > c1.high and \
            self.low > c2.open and \
            self.close > c2.high:
            return 1
        return 0

    def is_three_black_crows(self):

        c1 = CandleStick(self.parity, self.candle_index - 2)
        c2 = CandleStick(self.parity, self.candle_index - 1)

        if  c1.state == 'bearish' and \
            c2.state == 'bearish' and \
            self.state == 'bearish' and \
            c1.low > c2.close and \
            c2.high < c1.open and \
            c2.low > self.close and \
            self.high < c2.open:
            return 1
        return 0

    def is_three_inside_up(self):

        c1 = CandleStick(self.parity, self.candle_index - 2)
        c2 = CandleStick(self.parity, self.candle_index - 1)

        if c1.state == 'bearish' and \
           c2.state == 'bullish' and \
           self.state == 'bullish' and \
           c2.close < c1.open and \
           self.close > c1.open and \
            c2.low > c1.low and \
            self.low > c2.low:
            return 1
        return 0

    def is_three_inside_down(self):

        c1 = CandleStick(self.parity, self.candle_index - 2)
        c2 = CandleStick(self.parity, self.candle_index - 1)

        if c1.state == 'bullish' and \
                c2.state == 'bearish' and \
                self.state == 'bearish' and \
                c2.close > c1.open and \
                self.close < c1.open and \
                c2.high < c1.high and \
                self.high < c1.high:
            return 1
        return 0

    def get_type(self, candle_index):
        close = self.chart[candle_index]['close']
        open = self.chart[candle_index]['open']
        if open < close:
            return 0
        if open > close:
            return 1
        return 2



