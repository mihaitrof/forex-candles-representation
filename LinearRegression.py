from Parity import *

class LinearRegression:
    """Linear Regression applied to parity.

        Args:
            parity(Parity object): Represent an instance of Parity object.

        Attributes:
            lists(list) : Contains all types of values from candles.
            open(list)  : Represents the open values from candles.
            close(list)  : Represents the close values from candles.
            high(list)  : Represents the high values from candles.
            low(list)  : Represents the low values from candles.
            volume(list)  : Represents the volume values from candles.

        """
    def __init__(self, parity, type, last_number_of_elements = False, start = False, end = False):

        #set the attributes
        lists       = declare_arrys(parity)

        self.open   = lists[0]
        self.high   = lists[1]
        self.low    = lists[2]
        self.close  = lists[3]
        self.volume = lists[4]

        self.type   = type
        self.start  = False
        self.end    = False

        # Set attributes
        if start and end:
            self.start  = start
            self.end    = end

        if last_number_of_elements:
            self.last_number_of_elements = last_number_of_elements
        else:
            self.last_number_of_elements = False

        # set logging details
        self.line_number = str(inspect.stack()[0][2])
        self.root_path = str(inspect.stack()[0][1])

        # Set deltas
        self.delta_x               = self.delta_x()
        self.delta_y               = self.delta_y()
        self.delta_x_square        = self.delta_x_square(self.delta_x)
        self.delta_x_times_delta_y = self.delta_x_times_delta_y()

    def get_mean(self):
        """This methid aims to calculate the mean of elements from a list.

        Args:
            type(string)                 : Specific type of values (e.g. 'open', 'close' etc).
            last_number_of_elements(int) : Select the last n candles from an instance.
            start(string)                : Start date from instance.
            end(string)                  : End date from instance.

        Attributes:
            function_path(string)        : The path of file. Useful to log details.

        """
        # Logging...
        function_path = str(inspect.stack()[0][3])
        log_path(self.root_path, function_path)
        log_info(message='Calculating mean...')
        logging.info('[INFO] Done')

        type = self.type

        type = self.type
        elements = self.get_elements()

        # Get the last n elements
        if self.last_number_of_elements:
            elements = elements[(-1) * self.last_number_of_elements:]

        # Get range of elements
        if self.start and self.end:
            elements = elements[self.start:self.end]

        return sum(round(float(i[0]), 4) for i in elements) / len(elements)

    def get_elements(self):
        """Get the elements using 'type' as input

        """
        return {
            'open'  : self.open,
            'high'  : self.high,
            'low'   : self.low,
            'close' : self.close,
            'volume': self.volume
        }[self.type]

    def delta_x(self):
        """This methid aims to calculate the mean of elements from a list.

            Args:
                type(string)                 : Specific type of values (e.g. 'open', 'close' etc).
                last_number_of_elements(int) : Select the last n candles from an instance.
                start(string)                : Start date from instance.
                end(string)                  : End date from instance.

            Attributes:
                function_path(string)        : The path of file. Useful to log details.
                elements(list)               : Elements from candles.
                mean_x(float)                : Mean of elements from x axis.

            Return:
                delta(list)                  : Contains the difference between x and mean(x).
        """
        # Logging...
        function_path = str(inspect.stack()[0][3])
        log_path(self.root_path, function_path)
        log_info(message='Calculating delta_x ...')

        type = self.type
        elements = self.get_elements()

        # Get the last n elements
        if self.last_number_of_elements:
            elements = elements[(-1) * self.last_number_of_elements:]

        # Get range of elements
        if self.start and self.end:
            elements = elements[self.start:self.end]

        mean_x = get_mean([i for i in range(1, len(elements) + 1)])

        delta  = [(i - mean_x) for i in range(1, len(elements) + 1)]
        return delta
        # if self.check_delta(delta) == 1:
        #     logging.info('[INFO] Done')
        # return delta
        logging.info('[ERROR] The value of delta is not 0.')

    def delta_y(self):
        """This methid aims to calculate the mean of elements from a list.

            Args:
                type(string)                 : Specific type of values (e.g. 'open', 'close' etc).
                last_number_of_elements(int) : Select the last n candles from an instance.
                start(string)                : Start date from instance.
                end(string)                  : End date from instance.

            Attributes:
                function_path(string)        : The path of file. Useful to log details.
                elements(list)               : Elements from candles.
                mean_y(float)                : Mean of elements from y axis.

            Return:
                delta(list)                  : Contains the difference between y and mean(y).
        """

        # Logging...
        function_path = str(inspect.stack()[0][3])
        log_path(self.root_path, function_path)
        log_info(message='Calculating delta_y ...')

        elements = self.get_elements()

        # Get the last n elements
        if self.last_number_of_elements:
            elements = elements[(-1) * self.last_number_of_elements:]

        # Get range of elements
        if self.start and self.end:
            elements = elements[self.start:self.end]

        mean_y = round(self.get_mean(), 4)
        delta = [round((float(i[0]) - mean_y), 4) for i in elements]
        logging.info('[INFO] Done')
        return delta

    def delta_x_square(self, elements):
        data = []
        for n, i in enumerate(elements):
            data.append(i * i)
        return data

    def delta_x_times_delta_y(self):
        result = []
        for i in range(0,len(self.delta_x)):
            result.append(self.delta_x[i] * self.delta_y[i])

        return result

    def calculus(self):
        """
            y^ = b0 + b1 * x

        """
        # Get the last n elements
        elements = self.get_elements()

        if self.last_number_of_elements:
            elements = elements[(-1) * self.last_number_of_elements:]

        # Get range of elements
        if self.start and self.end:
            elements = elements[self.start:self.end]


        mean_x = get_mean([i for i in range(1, len(elements) + 1)])

        y = self.get_mean()
        b1 = sum(self.delta_x_times_delta_y) / sum(self.delta_x_square)

        b0 = y - b1 * mean_x

        return round(b0, 4), round(y, 4), mean_x

    def check_delta(self,delta):
        if sum(delta) == 0:
            return 1
        return sum(delta)
















