# -*- coding:utf-8 -*-
import logging
import os


class DirectoryHandler:
    """
    The class will iterate the input directory to find target database file.
    And store each found database file full path in a list of string "Database_File_Path"
    """
    Database_File_Path = []
    Directory_Iterate = 1
    Tree_indicator = "---"
    Target_To_Find = "report.db"

    def __init__(self, input_directory, target_to_find):
        """
        :param input_directory: 
        :param target_to_find: target database file name
        """
        if input_directory is not None:
            if os.path.isdir(input_directory):
                logging.debug(r"Input is a folder which is correct.")
            else:
                logging.error(r"Input is not a folder, please double check!")
                return
        self.Target_To_Find = target_to_find
        logging.debug("The target is: " + str(self.Target_To_Find))
        self.list_files(input_directory)

    def list_files(self, input_directory):
        """
        :param input_directory: 
        :return: no return. Directly write all target files found in Database_File_Path
        """
        dir_list = os.listdir(input_directory)
        for dl in dir_list:
            full_dl = os.path.join(input_directory, dl)
            if os.path.isfile(full_dl):
                # judge if hitting target
                if os.path.basename(full_dl) == self.Target_To_Find:
                    self.Database_File_Path.append(os.path.abspath(full_dl))
                    logging.info(self.Directory_Iterate * self.Tree_indicator +
                                 "|" + r"find a file: " + str(full_dl) +
                                 "<------Hitting Target!")
                else:
                    logging.info(self.Directory_Iterate * self.Tree_indicator +
                                 "|" + r"find a file: " + str(full_dl))
            else:
                logging.info(self.Directory_Iterate*self.Tree_indicator +
                             r"find a folder: " + str(full_dl))
                self.Directory_Iterate += 1
                self.list_files(full_dl)
        self.Directory_Iterate -= 1


if __name__ == '__main__':
    print("please do not use it individually.")
    # below codes for debug
    # define the logging config, output in file
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=r'./log/DirectoryHandler.log',
                        filemode='w')
    # define a stream that will show log level > Warning on screen also
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    a = DirectoryHandler(r"./data", "report.db")

