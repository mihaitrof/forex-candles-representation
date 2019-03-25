#!flask/bin/python
from flask import Flask, jsonify, request
from flask_cors import CORS
from CandleStick import *
from Parity import *
from Elliot_waves import *
from Analysis import *
from LinearRegression import *
from Inverse import *
from Simulation import *


app = Flask(__name__)
CORS(app)

@app.route('/coordinates/', methods=['GET'])
def get_coordinates():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    #  start
    start = request.args.get('start')

    #  end
    end = request.args.get('end')

    # candle index
    # candle_index = request.args.get('candle_index')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    # Simulation coordinates
    s = Simulation(p1, int(start), int(end))
    coordinates = s.get_coordinates()

    return jsonify(coordinates)


@app.route('/linear_regression/', methods=['GET'])
def linear_regression():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    type = 'open'

    # 'start' parameter
    start = request.args.get('start')
    #  'end' parameter
    end = request.args.get('end')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))
    linear = LinearRegression(p1, 'close', start=1, end=4)
    data = linear.calculus()

    return jsonify({'start': start, 'end': end, 'b0': data[0], 'y': data[1], 'mean_x':data[2]})

@app.route('/all_data/', methods=['GET'])
def all_data():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    # Trends
    technical = Analysis(p1)
    aux = technical.get_bearish_candlesticks()
    atts = technical.get_close_attribute(aux)
    bearish_trend = technical.get_bearish_trends(atts)

    # Fundamental analysis
    f = Database()
    parity = {}
    for x in f.get_fundamental_data():
        parity[x[0]] = {}

    for x in f.get_fundamental_data():
        parity[x[0]][str(x[1])] = {str(x[2]):[x[3], x[4], x[5], x[6], x[7]]}

    aux = technical.get_bullish_candlesticks()
    atts = technical.get_close_attribute(aux)
    bullish_trend = technical.get_bullish_trends(atts)
    # Elliot

    # e = Elliot_waves(p1)
    # elliot = e.find_waves()
    # max_points = e.max_points
    # min_points = e.min_points
    # level_line_max = e.level_line_max()
    # level_line_min = e.level_line_min()

    inv = Inverse(p1)
    inv.big_deal(0, len(inv.parity.chart) - 1)
    max_inverse       = inv.max_inverse
    min_inverse       = inv.min_inverse
    bullish_trend_new = inv.up_trends()
    bearish_trend_new = inv.down_trends()
    up_inverse        = inv.up_inverse()
    down_inverse      = inv.down_inverse()
    level_lines_el    = inv.set_level_lines()[1]
    level_lines       = inv.set_level_lines()[0]

    lvl_line_min = technical.level_line_min()
    lvl_line_max = technical.level_line_max()

    # inverse_down = e.inverse_down(lvl_line_max)
    # inverse_up   = e.inverse_up(lvl_line_min)

    # Function
    data = list()
    for index, candle in enumerate(p1.chart):
        meta = {'candlesticks':[], 'trends':'false'}
        color = {"Low": 'green', 'Medium': 'yellow', 'High': 'red'}
        data.append(candle)
        data[-1]['day'] = str(data[-1]['day'])
        data[-1]['hour'] = str(data[-1]['hour'])
        c = CandleStick(p1, index)
        c.set_types()
        if 'bullish_engulfing' in c.types:
            data[-2]['meta']['candlesticks'].append('bullish_engulfing')
        if 'bearish_engulfing' in c.types:
            data[-2]['meta']['candlesticks'].append('bearish_engulfing')
        if 'tweezer_tops' in c.types:
            data[-2]['meta']['candlesticks'].append('tweezer_tops')
        if 'tweezer_bottoms' in c.types:
            data[-2]['meta']['candlesticks'].append('tweezer_bottoms')

        if 'morning_star' in c.types:
            try:
                data[-2]['meta']['candlesticks'].append('morning_star')
                data[-3]['meta']['candlesticks'].append('morning_star')
            except IndexError:
                pass
        if 'evening_star' in c.types:
            try:
                data[-2]['meta']['candlesticks'].append('evening_star')
                data[-3]['meta']['candlesticks'].append('evening_star')
            except IndexError:
                pass
        if 'three_white_soldiers' in c.types:
            try:
                data[-2]['meta']['candlesticks'].append('three_white_soldiers')
                data[-3]['meta']['candlesticks'].append('three_white_soldiers')
            except IndexError:
                pass
        if 'three_black_crows' in c.types:
            try:
                data[-2]['meta']['candlesticks'].append('three_black_crows')
                data[-3]['meta']['candlesticks'].append('three_black_crows')
            except IndexError:
                pass
        if 'three_inside_up' in c.types:
            try:
                data[-2]['meta']['candlesticks'].append('three_inside_up')
                data[-3]['meta']['candlesticks'].append('three_inside_up')
            except IndexError:
                pass
        if 'three_inside_down' in c.types:
            try:
                data[-2]['meta']['candlesticks'].append('three_inside_down')
                data[-3]['meta']['candlesticks'].append('three_inside_down')
            except IndexError:pass


        meta['candlesticks'] = c.types
        if index in bearish_trend:
            meta['trends'] = 'bearish'
        if index in bullish_trend:
            meta['trends'] = 'bullish'
        if index in down_inverse:
            meta['inverse'] = 'down'
        if index in up_inverse:
            meta['inverse'] = 'up'
        if index in level_lines_el:
            meta['level_line'] = level_lines[index]
        # if index in elliot:
        #     meta['elliot'] = 'yes'
        if index in max_inverse:
            meta['elliot'] = 'max'
        if index in min_inverse:
            meta['elliot'] = 'min'
        # if index in [*level_line_max]:
        #     meta['level_line'] = ['max', level_line_max[index]]
        # if index in [*level_line_min]:
        #     meta['level_line'] = ['min', level_line_min[index]]
        # if index in [*lvl_line_max]:
        #     meta['level_line'] = ['max', lvl_line_max[index]]
        # if index in [*lvl_line_min]:
        #     meta['level_line'] = ['min', lvl_line_min[index]]
        # if index in inverse_down:
        #     meta['inverse'] = 'down'
        # if index in inverse_up:
        #     meta['inverse'] = 'up'

        try:
            info = [parity[p1.base][data[-1]['day']][data[-1]['hour']][0],
                    parity[p1.base][data[-1]['day']][data[-1]['hour']][2],
                    parity[p1.base][data[-1]['day']][data[-1]['hour']][3],
                    parity[p1.base][data[-1]['day']][data[-1]['hour']][4]]

            meta['fundamental'] = [color[parity[p1.base][data[-1]['day']][data[-1]['hour']][1].split(" ")[0]], info]
        except KeyError:pass

        try:
            info = [parity[p1.quote][data[-1]['day']][data[-1]['hour']][0],
                    parity[p1.quote][data[-1]['day']][data[-1]['hour']][2],
                    parity[p1.quote][data[-1]['day']][data[-1]['hour']][3],
                    parity[p1.quote][data[-1]['day']][data[-1]['hour']][4]]

            if meta['fundamental'][0] != 'red':
                meta['fundamental'] = [color[parity[p1.quote][data[-1]['day']][data[-1]['hour']][1].split(" ")[0]], info]
        except KeyError:pass

        data[-1]['meta'] = meta

    total = len(p1.chart)

    return jsonify({'data': data, 'meta': {'total': total}})

@app.route('/trends/inverse/', methods=['GET'])
def inverse_trends():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    technical = Analysis(p1)
    bullish = technical.get_bullish_candlesticks()
    bearish = technical.get_bearish_candlesticks()
    bullish_atts = technical.get_close_attribute(bullish)
    bearish_atts = technical.get_close_attribute(bearish)
    bullish_trend = technical.get_bullish_trends(bullish_atts)
    bearish_trend = technical.get_bearish_trends(bearish_atts)


    chart = technical.get_inverse_trends_api(bearish_trend, bullish_trend)

    return jsonify({'data': chart[0] , 'meta': {'total': chart[1]}})

@app.route('/trends/bullish/', methods=['GET'])
def bullish_trends():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    # 'start' parameter
    start = request.args.get('start')
    #  'end' parameter
    end = request.args.get('end')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    technical = Analysis(p1, start, end)
    data = technical.get_bullish_candlesticks()
    atts = technical.get_close_attribute(data)
    bullish_trend = technical.get_bullish_trends(atts)

    chart = technical.get_trends_api(bullish_trend, False)

    return jsonify({'data': chart[0], 'meta': {'total': chart[1]}})

@app.route('/trends/bearish/', methods=['GET'])
def bearish_trends():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    # 'start' parameter
    start = request.args.get('start')
    #  'end' parameter
    end = request.args.get('end')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    technical = Analysis(p1, start, end)
    data = technical.get_bearish_candlesticks()
    atts = technical.get_close_attribute(data)
    bearish_trend = technical.get_bearish_trends(atts)

    chart = technical.get_trends_api(bearish_trend)

    return jsonify({'data': chart[0], 'meta': {'total': chart[1]}})

@app.route('/data/type/', methods=['GET'])
def candlesticks_type():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    # function
    data = list()
    for index, candle in enumerate(p1.chart):
        data.append(candle)
        data[-1]['day'] = str(data[-1]['day'])
        data[-1]['hour'] = str(data[-1]['hour'])
        c = CandleStick(p1, index)
        data[-1]['types'] = c.types

    total = len(p1.chart)
    # return data, total

    # chart = p1.get_type_candlesticks()

    return jsonify({'data': data, 'meta':{'total':total}})

@app.route('/data/', methods=['GET'])
def get_full_data():

    # 'base' parameter
    base = request.args.get('base')
    # 'quote' parameter
    quote = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    chart = p1.get_full_chart()

    return jsonify({'data': chart[0], 'meta':{'total':chart[1]}})

@app.route('/candlesticks/', methods=['GET'])
def get_tasks():

    # 'base' parameter
    base      = request.args.get('base')
    # 'quote' parameter
    quote     = request.args.get('quote')
    #  'timeframe' parameter
    timeframe = request.args.get('timeframe')

    # create instance of Parity
    p1 = Parity(base.upper(), quote.upper(), int(timeframe))

    # 'page' parameter
    page = request.args.get('page')
    if page is None:
        page = 1

    # 'limit' parameter
    limit = request.args.get('limit')
    if limit is None:
        limit = 50

    if int(limit) > 50:
        limit = 50

    chart = p1.get_chart(page, limit)
    meta = {'total'       : chart[1],
            'count'       : chart[2],
            'per_page'    : chart[3],
            'current_page': chart[4],
            'total_pages' : chart[5]}

    return jsonify({'data': chart[0], 'meta': meta})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')