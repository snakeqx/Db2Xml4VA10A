# -*- coding:utf-8 -*-
import os
import logging
import sqlite3
from xml.etree import ElementTree
from EnumFunctionTable import StringFunctionTables
# import base64

# define the logging config, output in file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=r'.\log\DatabaseHandler.log',
                    filemode='w')
# define a stream that will show log level > Warning on screen also
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


class DatabaseHandler:
    Database_Name = 'report.db'
    System_SerialNo = ""

    def __init__(self, file_name):
        if os.path.isfile(file_name):
            self.Database_Name = file_name
        else:
            logging.error(r'Can not find input file.')
            return
        self.Connection = sqlite3.connect(self.Database_Name)
        logging.debug(r'Database connected')
        for str_functions in StringFunctionTables:
            self.read_data(str_functions)
        self.Connection.close()

    def read_data(self, function_type):
        if function_type not in StringFunctionTables:
            logging.error(r'Function Type is not in EnumFunctionTable.py. Please configure it first or check spelling')
            return
        logging.debug(function_type + r" is now under query.")
        sql_cursor = self.Connection.cursor()
        sql_string = r"select data from functionstable where (functionstatus='Success' and NlsID=?) " \
                     r"order by starttime desc"
        try:
            sql_cursor.execute(sql_string, [function_type])
            result = sql_cursor.fetchone()
            if result is None:
                logging.warning(function_type + r' with SUCCESS result has not been found.!!!!!!!!!!')
                return
            else:
                while not self.parse_xml(result[0].decode()):
                    result = sql_cursor.fetchone()
                    if result is None:
                        logging.debug(function_type + r' has no <Content>, please double check!')
                        break
                logging.info(r'Read data successfully.')
        except sqlite3.Error as e:
            logging.error(str(e))
        finally:
            sql_cursor.close()

    @staticmethod
    def parse_xml(xml_string):
        xml_tree = ElementTree.fromstring(xml_string)
        for node in xml_tree:
            if node.tag == 'Chapter':
                content_tag = node.find(r'Downloadable/Content')
                if content_tag is not None:
                    logging.info(r'<Content> has been found.')
                    return True
        logging.debug(r'It seems this data has no <Content> node. Skip')
        return False

    def get_serial_number(self):
        logging.debug(r"It is now query for system serial number.")
        sql_cursor = self.Connection.cursor()
        sql_string = r"select data from servicereportstable order by starttime desc limit 1"
        try:
            sql_cursor.execute(sql_string)
            result = sql_cursor.fetchone()
            if result is None:
                logging.warning(r"Can not find serial number!")
                return
        except sqlite3.Error as e:
            logging.error(str(e))
        finally:
            sql_cursor.close()


if __name__ == '__main__':
    a = DatabaseHandler(r"E:\Programming\Python\Db2Xml4VA10A_Data\report.db")
