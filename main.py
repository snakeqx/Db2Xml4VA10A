import os
import logging
import sys
from DirectoryHandler import DirectoryHandler
from DatabaseHandler import DatabaseHandler

# define the logging config, output in file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=r'.\main.log',
                    filemode='w')
# define a stream that will show log level > Warning on screen also
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def main():
    logging.debug(r"here is the main program")
    file_name='report.db'
    # if only call the script, will use ./a.dcm as input
    if len(sys.argv) == 1 or len(sys.argv) > 3:
        print("Use the script as below:")
        print("python(3) main.py [filename]|[folder name]")
        print("if filename is not given, it will use default as 'report.db'")
        print("folder name is mandatory.")
    # if with 1 parameter
    elif len(sys.argv) == 2:
        logging.debug(r"Program has 1 parameters.")
        if os.path.isdir(sys.argv[1]):
            folder_name = os.path.abspath(sys.argv[1])
            directory_handler = DirectoryHandler(folder_name, file_name)
            logging.info(str(directory_handler.Database_File_Path))
            for db in directory_handler.Database_File_Path:
                DatabaseHandler(db)
        else:
            print(r"The parameter seems not a folder, please double check")
            return
    # if with 2 parameters
    elif len(sys.argv) == 3:
        pass


if __name__ == '__main__':
    main()



