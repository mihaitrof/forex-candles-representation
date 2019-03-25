import os
import csv
import datetime
import logging
import inspect
import glob

# Set date time
now = datetime.datetime.now()
date_time = str(now.day) + '_' + str(now.month) + '_' + str(now.year)

# Set logging details
line_number = str(inspect.stack()[0][2])
root_path = str(inspect.stack()[0][1])

# Set logging process and other settings
logging.basicConfig(filename=os.path.dirname(__file__) + '/logs/' + date_time + '.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p __')

# This method aims to combine two CSV files in order to compress into a single file more information
def combine_csvs(base, quote, timeframe):
    with open(get_data_path(base, quote, timeframe), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)

        with open(get_data_path(base, quote, timeframe, True)) as File:
            reader = csv.reader(File)
            rows = [r for r in reader]
            last_line = get_last_line_from_csv(base, quote, timeframe)
            ok = 0
            for row in rows:
                # print(row[0] >= last_line[0])
                # break
                if ok == 1:
                    spamwriter.writerow(row)
                if row[0] > last_line[0] and ok == 0:
                    spamwriter.writerow(row)
                    ok = 1
                if row[0] == last_line[0] and row[1] > last_line[1] and ok == 0:
                    spamwriter.writerow(row)
                    ok = 1
    logging.info('[UPDATE]' + get_data_path(base, quote, timeframe) + ' succesfully updated.')

# Get last modification date of file
def last_modificaiton_date(file_name):
    timestamp = int(os.path.getmtime(file_name))
    date = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%y %H:%M:%S')
    return date

# Get path name
def get_data_path(base, quote, timeframe, unprocessed = False):
    if unprocessed == False:
        path = os.path.dirname(__file__) + '/data/' + base + quote + '/' + get_csv_file_name(base, quote, timeframe)
        return path
    path = os.path.dirname(__file__) + '/unprocessed_data/' +  get_csv_file_name(base, quote, timeframe)
    return path

# Get CSV file name
def get_csv_file_name(base, quote, timeframe):
    file_name = base + quote + str(timeframe) + '.csv'
    return file_name

# Delete file
def delete_file(path):
    try:
        os.remove(path)
        logging.info('[DELETE] ' + path + ' succesfully deleted.')
    except:
        logging.info('[ERROR] ' + path + ' does not exist anymore!')

# Get last line from CSV in order to append data from unprocessed data starting with this line
def get_last_line_from_csv(base, quote, timeframe):
    with open(get_data_path(base, quote, timeframe)) as File:
        reader = csv.reader(File)
        rows = [r for r in reader]
    return rows[-1]

# Update data folder using CSVs from unprocessed_data.
def update_data():
    for fileName in glob.glob(os.path.dirname(__file__) + '/unprocessed_data/*', recursive=True):
        reverse_file_name = fileName[::-1]
        parity_name = fileName[(-1)*reverse_file_name.index('\\'):-4]
        base = parity_name[:3]
        quote = parity_name[3:6]
        timeframe = parity_name[6:]
        if os.path.exists(get_data_path(base, quote, timeframe)):
            combine_csvs(base, quote, timeframe)
            delete_file(get_data_path(base, quote, timeframe, True))
        else:
            try:
                os.rename(get_data_path(base, quote, timeframe, True), get_data_path(base, quote, timeframe))
            except:
                logging.info('[ERROR] Folder ' + base + quote + ' does not exist. You have to creat it.')

# Check whether a specific folder from data contains all six CSVs representing all timeframes
def complete_parity_folder(base, quote):
    file_count = 0
    for fileName in glob.glob(os.path.dirname(__file__) + '/data/' + base + quote + '/*', recursive=True):
        file_count += 1
    if file_count == 9:
        return 1
    return 0

# Split parity chart into different lists in order to acces easier data. Also can be used in different strategies
# This method is mostly used by strategy classes in constructor.
def declare_arrys(parity):

    # Logging...
    function_path = str(inspect.stack()[0][3])
    log_path(root_path, function_path)
    log_info(message='Splitting candles into distinct lists...')

    open = list()
    high = list()
    close = list()
    low = list()
    volume = list()
    for candle in parity.chart:
        point = [candle['open'], candle['day'], candle['hour']]
        open.append(point)

        point = [candle['high'], candle['day'], candle['hour']]
        high.append(point)

        point = [candle['low'], candle['day'], candle['hour']]
        low.append(point)

        point = [candle['close'], candle['day'], candle['hour']]
        close.append(point)

        point = [candle['volume'], candle['day'], candle['hour']]
        volume.append(point)

    logging.info('[INFO] Done')
    return open, high, low, close, volume

def get_mean(elements):

    #Logging...
    function_path = str(inspect.stack()[0][3])
    log_path(root_path, function_path)
    log_info(message='Calculating mean...')

    return sum(float(i) for i in elements) / len(elements)

def log_path(root_path, function_path):
    logging.info('[PATH] ' + root_path + '/' + function_path)

def log_info(message):
    logging.info('[INFO] ' + message)

def log_error(message):
    logging.info('[ERROR] ' + message)

def parse_line(row):
    """This method aims to parse the information received through the CSV file and to create useful dictionaries.

    Args:
        row(list): A list which sum up the information about a candle (e.g. date, open, high, low etc).

    Attributes:
        candle(dictionary): Store the candle information.

    Returns:
        list

    """
    candle = {}
    candle['day']    = row[0]
    candle['hour']   = row[1]
    candle['open']   = row[2]
    candle['high']   = row[3]
    candle['low']    = row[4]
    candle['close']  = row[5]
    candle['volume'] = row[6]

    return candle






