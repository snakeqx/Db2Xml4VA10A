# -*- coding:utf-8 -*-
import os
import logging
import sqlite3
from xml.etree import ElementTree
from EnumFunctionTable import StringFunctionTables
import base64


class DatabaseHandler:
    Database_Name = 'report.db'
    System_SerialNo = ""
    OutPut_Path = ""

    def __init__(self, file_name, output_path=r'./'):
        # deal with input database file
        if os.path.isfile(file_name):
            self.Database_Name = file_name
        else:
            logging.error(r'Can not find input file.')
            return
        # connect to database
        self.Connection = sqlite3.connect(self.Database_Name)
        logging.debug(r'Database connected')
        self.get_serial_number()
        # after get serial number, create/check the output path
        if self.initial_output_path(output_path):
            # iterate the function tables to extract xml file
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
                logging.debug(function_type + r' with SUCCESS result has not been found.!!!!!!!!!!')
                return
            else:
                while not self.parse_xml(result[0].decode(), function_type):
                    result = sql_cursor.fetchone()
                    if result is None:
                        logging.debug(function_type + r' has no <Content>, please double check!')
                        break
                logging.info(r'Read data successfully.')
        except sqlite3.Error as e:
            logging.error(str(e))
        finally:
            sql_cursor.close()

    def parse_xml(self, xml_string, function_type):
        xml_tree = ElementTree.fromstring(xml_string)
        for node in xml_tree:
            if node.tag == 'Chapter':
                content_tag = node.find(r'Downloadable/Content')
                if content_tag is not None:
                    logging.info(r'<Content> has been found.')
                    content_bytes = base64.b64decode(content_tag.text)
                    content_string = content_bytes.decode()
                    if self.output_xml(content_string, function_type):
                        logging.debug(r'Output file success.')
                    else:
                        logging.error(r'Output file error!')
                        return False
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
            find_string = r'System SerialNumber="'
            find_index = str(result).find(find_string)
            self.System_SerialNo = str(result)[find_index+len(find_string):find_index+len(find_string)+6]
            logging.info(self.System_SerialNo)
        except sqlite3.Error as e:
            logging.error(str(e))
        finally:
            sql_cursor.close()

    def initial_output_path(self, path):
        if not os.path.isdir(path):
            logging.error(r'Output path is not correct!')
            return False
        self.OutPut_Path = os.path.join(path, self.System_SerialNo)
        logging.debug(r'Output path='+str(self.OutPut_Path))
        if os.path.exists(self.System_SerialNo):
            logging.error(r'Already have the xml files, please back up manually!')
            return False
        os.mkdir(self.OutPut_Path)
        return True

    def output_xml(self, xml_string, function_type):
        file_name = function_type+'.xml'
        abs_file_name = os.path.abspath(os.path.join(self.OutPut_Path, file_name))
        try:
            fp = open(abs_file_name, 'w')
            fp.write(xml_string)
            logging.info(abs_file_name + " write success!!")
        except Exception as e:
            logging.error(str(e))
        finally:
            fp.close()
        return True


if __name__ == '__main__':
    print("please do not use it individually.")
    # define the logging config, output in file
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=r'./log/DatabaseHandler.log',
                        filemode='w')
    # define a stream that will show log level > Warning on screen also
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    a = DatabaseHandler(r"./data/report.db")
