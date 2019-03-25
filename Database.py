import psycopg2
import inspect
from helpers import *

class Database:
    """This class aims to manage database functions.

    """

    def __init__(self):

        # Logging...
        self.root_path = str(inspect.stack()[0][1])
        function_path = str(inspect.stack()[0][3])
        log_path(self.root_path, function_path)
        log_info(message='Opened database successfully.')

        self.conn = psycopg2.connect(database="testdb", user="postgres", password="test123", host="db", port="5432")

        logging.info('[INFO] Done')

    def create_fundamental_analysis_table(self, table_name):

        function_path = str(inspect.stack()[0][3])

        command = """ CREATE TABLE """ + table_name + """ (
                                currency varchar(3),
                                day DATE,
                                hour TIME,
                                event_name varchar(50),
                                impact varchar(50),
                                forecast varchar(20),
                                previous varchar(20),
                                actual varchar(20)
                                )
                        """
        try:
            cur = self.conn.cursor()
            cur.execute(command)
            cur.close()
            self.conn.commit()

            # Logging...
            log_path(self.root_path, function_path)
            log_info(message='Table ' + table_name + ' created succesfully.')

        except (Exception, psycopg2.DatabaseError) as error:
            # Logging...
            log_path(self.root_path, function_path)
            log_error(message='Table ' + table_name + ' can not be created. ' + str(error))
            print(error)
        # finally:
        #      if self.conn is not None:
        # self.conn.close()


    def create_table(self, table_name):
        """Create a new table in Postgres.

        Args:
            table_name(str): Table's name.

        Attributes:
            function_path(str): Function's name.
            command(str)      : Sql command.
            cur(list)         : Postgres cursor.

        """
        function_path = str(inspect.stack()[0][3])

        command = """ CREATE TABLE """ + table_name + """ (
                        day DATE,
                        hour TIME,
                        open float(5),
                        high float(5),
                        low float(5),
                        close float(5),
                        volume integer    
                        )
                """
        try:
             cur = self.conn.cursor()
             cur.execute(command)
             cur.close()
             self.conn.commit()

             # Logging...
             log_path(self.root_path, function_path)
             log_info(message='Table ' + table_name + ' created succesfully.')

        except (Exception, psycopg2.DatabaseError) as error:
             # Logging...
             log_path(self.root_path, function_path)
             log_error(message='Table ' + table_name + ' can not be created. ' + str(error))
             print(error)
        # finally:
        #      if self.conn is not None:
                # self.conn.close()

    def insert_data(self, table_name, data):

        """Insert data in certain table.

            Args:
            table_name(str): Table's name.
            data(list)     : Data to insert into table.

            Attributes:
            function_path(str): Function's name.
            sql(str)          : Sql command.
            cur(list)         : Postgres cursor.

        """

        function_path = str(inspect.stack()[0][3])

        sql = """INSERT INTO """ + table_name + """(day, hour, open, high, low, close, volume) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        # print(sql)
        try:
            # create a new cursor
            cur = self.conn.cursor()
            # execute the INSERT statement
            cur.executemany(sql, data)
            # commit the changes to the database
            self.conn.commit()
            # close communication with the database
            cur.close()

            # Logging...
            log_path(self.root_path, function_path)
            log_info(message='Data in ' + table_name + ' table inserted succesfully.')

        except (Exception, psycopg2.DatabaseError) as error:
             # Logging...
             log_path(self.root_path, function_path)
             log_error(message='Data can NOT be inserted in ' + table_name + ' table. ' + str(error))
             print(error)
        # finally:
        #      if self.conn is not None:
        #         # self.conn.close()

    def create_parity_tables(self, base, quote):
        timeframes = [1, 5, 15, 30, 60, 240, 1440, 10080, 43200]

        for timeframe in timeframes:
            self.create_table(base.lower() + quote.lower() + str(timeframe))

    def upload_parity(self, base, quote):

        """Insert data for certain parity.

            Args:
            base(str)  : The base currency (e.g. in the quotation EUR/USD, EUR represents the base currency).
            quote(str) : The quote currency(e.g. in the quotation EUR/USD, USD represents the quote currency).

            Attributes:
            timeframes(list)  : The basic timeframes of forex.
            function_path(str): Function's name.
            sql(str)          : Sql command.
            cur(list)         : Postgres cursor.
            fileName(str)     : CSV's name.
            data(list)        : Data to be push into database.
            reader(_csv)      : Line of CSV.

        """

        self.create_parity_tables(base, quote)
        timeframes    = [1, 5, 15, 30, 60, 240, 1440, 10080, 43200]
        function_path = str(inspect.stack()[0][3])
        # print(timeframes)
        for timeframe in timeframes:
            fileName = get_data_path(base, quote, timeframe)

            data = list()
            with open(fileName, newline='') as File:
                reader = csv.reader(File)
                for row in reader:
                    data.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

                self.insert_data(base.lower() + quote.lower() + str(timeframe), data)
                # Logging...
                log_path(self.root_path, function_path)
                log_info(message='Success!')

    def get_data(self, base, quote, timeframe, day = False, hour = False, sql = False) -> list:

        """Get data from database according to the parameters from function's header.

            Args:
            base(str)         : The base currency (e.g. in the quotation EUR/USD, EUR represents the base currency).
            quote(str)        : The quote currency(e.g. in the quotation EUR/USD, USD represents the quote currency).
            timeframes(list)  : The basic timeframes of forex.
            day(str)          : Day.
            hour(str)         : Hour.
            sql(str)          : SQL syntax.

            Attributes:
            function_path(str): Function's name.
            command(str)      : SQL command.
            cur(list)         : Postgres cursor.
            table_name(str)   : Table's name.
            where(str)        : WHERE syntax for SQL.
            rows(list)        : Returned data from fething the table.

        """

        table_name = base.lower() + quote.lower() + str(timeframe)

        # WHERE clause
        where = """ WHERE """
        if day != False:
            where += """day = """ + day
        if hour != False:
            where += """ AND hour = """ + hour

        command = """ SELECT * FROM """ + table_name
        if len(where) > 7:
            command += where

        # print(command)
        # Execute SELECT
        cur = self.conn.cursor()
        cur.execute(command + ';')
        rows = cur.fetchall()
        # self.conn.close()
        return rows

    # def get_candle(self, base, quote, timeframe, day, hour):
    #     table_name = base.lower() + quote.lower() + str(timeframe)
    #     command = """ SELECT * FROM """ + table_name
    #
    #     # Execute SELECT
    #     cur = self.conn.cursor()
    #     cur.execute(command)
    #     rows = cur.fetchall()
    #     self.conn.close()
    #     return rows

    def get_fundamental_data(self, table_name = 'fundamental') -> list:

        command = """ SELECT * FROM """ + table_name

        # print(command)
        # Execute SELECT
        cur = self.conn.cursor()
        cur.execute(command + ';')
        rows = cur.fetchall()
        # self.conn.close()
        return rows


