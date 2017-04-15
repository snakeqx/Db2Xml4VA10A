import logging
import os
import sys

from DatabaseHandler import DatabaseHandler
from DirectoryHandler import DirectoryHandler

# define the logging config, output in file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=r'./log/main.log',
                    filemode='w')
# define a stream that will show log level > Warning on screen also
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def main():
    """
    Main program to:
    1. Call DirectoryHandler to get the list of string of all target database file
    2. for each database file, it will call DatabaseHandler to generate xml file
    :return: no return value
    """
    logging.debug(r"here is the main program")
    file_name = 'report.db'

    # if with 1 parameter
    if len(sys.argv) == 2:
        print(r"Program has 1 parameters. Now it is assumed the given para is 'folder name'")
        if os.path.isdir(sys.argv[1]):
            folder_name = os.path.abspath(sys.argv[1])
            directory_handler = DirectoryHandler(folder_name, file_name)
            logging.info(str(directory_handler.Database_File_Path))
            for db in directory_handler.Database_File_Path:
                DatabaseHandler(db)
        else:
            print(r"The parameter seems not a folder, please double check")
            return
    if len(sys.argv) == 3:
        print(r"Program has 2 paramters, which is confusing. Program exits.")
        return
    # if with 2 parameters
    elif len(sys.argv) == 4:
        print(r"Program has 3 parameters.")
        file_name = sys.argv[1]
        if os.path.isdir(sys.argv[2]) and os.path.isdir(sys.argv[3]):
            folder_name = os.path.abspath(sys.argv[2])
            output_name = os.path.abspath(sys.argv[3])
            directory_handler = DirectoryHandler(folder_name, file_name)
            if directory_handler.Database_File_Path is None:
                print(r"No target file found. Please double check. Reversed parameters?")
                return
            for db in directory_handler.Database_File_Path:
                DatabaseHandler(db, output_path=output_name)
    else:
        print("Use the script as below:")
        print("python(3) main.py [filename] [folder name] [output path]")
        print("[filename] if filename is not given, it will use default as 'report.db'")
        print("[folder name] folder name is mandatory.")
        print("[output path] if output path is not given, it will use default as './'")


if __name__ == '__main__':
    main()



