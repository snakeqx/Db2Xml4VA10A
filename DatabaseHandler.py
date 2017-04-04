#!coding=utf8
import os
import logging
import sqlite3
import EnumFunctionTable

# define the logging config, output in file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='DatabaseHandler.log',
                    filemode='w')
# define a stream that will show log level > Warning on screen also
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)









class DatabaseHandler:

    Database_Name = "report.db"

    def __init__(self, file_name):
        self.Database_Name = file_name
        try:
            con = sqlite3.connect(self.Database_Name)
        except sqlite3.Error as e:
            logging.debug(str(e))
            return
        finally:
            logging.debug(r"Database connected")
            con.close()

    def read_data(self):
        try:
            con = sqlite3.connect(self.Database_Name)
        except sqlite3.Error as e:
            logging.debug(str(e))
            return
        sql_cursor = con.cursor()
        sql_string = r"select integration_result from BandAssessment"
        sql_cursor.execute(sql_string)
        data = sql_cursor.fetchone()[0]
        str_result = data.split(';')
        float_result = []
        for x in str_result:
            float_result.append(float(x))
        np_result = np.array(float_result)
        print(type(np_result))
        print(np_result)
        con.close()

if __name__ == '__main__':
    a = DatabaseHandler(r"./report.db")

