# -*- coding:utf-8 -*-
import base64
import logging
import os
import sqlite3
from xml.etree import ElementTree

from EnumFunctionTable import StringFunctionTables


class DatabaseHandler:
    """
    The class is to deal with sqlite3 database file.
    It will do the job as below:
    1. read the database
    2. Find the target service function
    3. Analyze if the target service function has a <content> which stores the xml file of the function result data
    4. If <content> is found, extract the content.
    5. convert the <content> with base64 decode and save to a xml file
    """
    Database_Name = 'report.db'
    System_SerialNo = ""
    OutPut_Path = ""

    def __init__(self, file_name, output_path=r'./'):
        """
        :param file_name: database file name for analyze
        :param output_path: the path of output xml files. default as ./
        """
        # deal with input database file
        if os.path.isfile(file_name):
            self.Database_Name = file_name
        else:
            logging.error(r'Can not find input file.')
            return
        # connect to database
        try:
            self.Connection = sqlite3.connect(self.Database_Name)
            logging.debug(r'Database connected')
            self.get_serial_number()
            # after get serial number, create/check the output path
            if self.initial_output_path(output_path):
                # iterate the function tables to extract xml file
                for str_functions in StringFunctionTables:
                    self.read_data(str_functions)
        except Exception as e:
            logging.error(str(e))
        finally:
            self.Connection.close()

    def read_data(self, function_type):
        """
        read the data of target service function from database.
        if the target service function has been found, it will call parse_xml function.
        :param function_type: target service function name. Should be stored in EnumFunctionTable.py
        :return: No return value.
        """
        if function_type not in StringFunctionTables:
            logging.error(r'Function Type is not in EnumFunctionTable.py. Please configure it first or check spelling')
            return
        logging.debug(function_type + r" is now under query.")
        sql_cursor = self.Connection.cursor()
        sql_string = r"select data from functionstable where (functionstatus='Success' and NlsID=?) " \
                     r"order by starttime desc"
        try:
            sql_cursor.execute(sql_string, [function_type])
            result = sql_cursor.fetchall()
            if result is None:
                logging.debug(function_type + r' with SUCCESS result has not been found.!!!!!!!!!!')
                return
            else:
                for data in result:
                    while not self.parse_xml(data[0].decode(), function_type):
                        result = sql_cursor.fetchone()
                        if result is None:
                            logging.warning(function_type + r' has no <Content>, please double check!')
                            break
                    logging.info(r'Read data successfully.')
        except sqlite3.Error as e:
            logging.error(str(e))
        finally:
            sql_cursor.close()

    def parse_xml(self, xml_string, function_type):
        """
        the service function result is stored in the database in xml string format.
        this function is try to analyze the xml string to see if has <content> node.
        <content> node is a base64 encoded string which stores the detail result of the service function. 
        e.g. actual value
        :param xml_string: the stored xml string in database
        :param function_type: target service function name. Should be stored in EnumFunctionTable.py
        :return: boolean
        """
        xml_tree = ElementTree.fromstring(xml_string)
        start_time = xml_tree.attrib['StartTime']
        for node in xml_tree:
            if node.tag == 'Chapter':
                content_tag = node.find(r'Downloadable/Content')
                if content_tag is not None:
                    logging.info(r'<Content> has been found.')
                    content_bytes = base64.b64decode(content_tag.text)
                    if self.output_xml(content_bytes, function_type, start_time):
                        logging.debug(r'Output file success.')
                    else:
                        logging.error(r'Output file error!')
                        return False
                    return True
        logging.debug(r'It seems this data has no <Content> node. Skip')
        return False

    def get_serial_number(self):
        """
        this function is to fill the class variable "System_SerialNo"
        The system serial no will be used as the output folder name
        :return: no return value
        """
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
        """
        creates the output folder.
        the folder name is "System_SerialNo"
        :param path: where the folder of "System_SerialNo" should be put
        :return: boolean
        """
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

    def output_xml(self, xml_bytes, output_file_name, start_time):
        """
        to save the <content> node in a xml file in the output folder.
        :param start_time: the start time parsed from attribute of element tree root 
        :param xml_bytes: The string of <content> which includes the detailed service function result.
        :param output_file_name: the file name that will be saved. actually the function name is used. 
        :return: boolean
        """
        file_name = output_file_name + str(start_time) + '.xml'
        file_name = file_name.replace(':', ';')
        abs_file_name = os.path.abspath(os.path.join(self.OutPut_Path, file_name))
        try:
            fp = open(abs_file_name, 'wb')
            fp.write(xml_bytes)
            logging.info(abs_file_name + " write success!!")
        except Exception as e:
            logging.error(str(e))
        finally:
            fp.close()
        return True


if __name__ == '__main__':
    print("please do not use it individually.")
    # belows codes for debug
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
