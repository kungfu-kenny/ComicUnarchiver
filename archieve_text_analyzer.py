import os
import shutil
import openpyxl
from pprint import pprint
from itertools import chain
from datetime import datetime, timedelta
from config import (folder_report,
                    format_xlsx,
                    folder_used_xlxs,
                    folder_workspace)

class ArchieveAnalyzer:
    """
    class which is dedicated to check values of the inserted comics
    which would go to the image server
    """
    def __init__(self) -> None:
        self.nowadays = datetime.now()
        self.name_today = self.get_datetime(self.nowadays, 'name')
        self.name_previous = self.get_datetime(self.nowadays, 'prev')
        self.folder_report_path = self.get_path(folder_workspace, folder_report)
        self.folder_report_used = self.get_path(self.folder_report_path, folder_used_xlxs)

    @staticmethod
    def get_datetime(nowadays:object, string_type:str) -> str:
        """
        Static method which is dedicated to create a datetime with a
        selected format in different cases
        Input:  nowadays = object of the datetime.now()
                string_type = string which means boolaen which we would take
        Output: datetime value which was used
        """
        if string_type == 'name':
            return nowadays.strftime('%Y_%m_%d')
        if string_type == 'prev':
            return (nowadays - timedelta(days=1)).strftime('%Y_%m_%d')
        return ''

    @staticmethod
    def get_path(*folder_path:set) -> str:
        """
        Static method which is dedicated to work with developing full path
        Input:  folder_path = set with all values which would used further
        Output: we developed values of the
        """
        return os.sep.join(folder_path)

    @staticmethod
    def remove_file(file_path:str, value_bool:bool=True) -> None:
        """
        Static method which is dedicated to remove files of the 
        Input:  file_path
        Output: we removed our file
        """
        if value_bool:
            return os.remove(file_path)
        shutil.rmtree(file_path)

    @staticmethod
    def check_folder(folder_path:str) -> None:
        """
        Static method which is dedicated to check folder prsence in the directory
        Input:  folder_path = full path to the folder
        Output: we created folder for the files
        """
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    def concatanate_reports(self, file_name:str) -> None:
        """
        Method which is dedicated to concatanate reports of the working files in cases of the doubles of them
        Input:  file_name = name of the selected files which are going to be presented
        Output: all info is stored in one file
        """
        #TODO add here pandas, sort concatanated by date and to 
        pass

    def check_input_xlsx(self) -> bool:
        """
        Method which is dedicated to work with an original xlsx values
        Input:  all containment of the folder
        Output: we successfully developed new values of it
        """
        list_check = [(self.get_path(self.folder_report_path, f), f) for f in os.listdir(self.folder_report_path) if f != folder_used_xlxs]
        
        for file_path, file_name in list_check:
            value_okay, value_file_name = self.check_report_characteristics(file_path, file_name)
            if not value_okay:
                self.remove_file(file_path)
            if value_file_name == self.name_previous:
                if not file_name in os.listdir(self.folder_report_used):
                    shutil.move(file_path, self.get_path(self.folder_report_used, file_name))
                else:
                    #TODO add here an element which could work with it
                    print('we cannot do that!')
                    pass

    @classmethod
    def get_list_together(cls, value_list:list) -> list:
        """
        Class method which is dedicated to create one list from n list of lists
        Input:  value_list = list which was given
        Output: list with no lists within
        """
        if isinstance(value_list[0], list) or isinstance(value_list[0], set) or isinstance(value_list[0], tuple):
            return cls.get_list_together(list(chain(value_list[0])))
        return value_list

    @classmethod
    def get_list_empty(cls, value_list:list) -> bool:
        """
        Method which is dedicated to check sublists on empty states
        Input:  value_list = list of the 
        Output: we successfully checked everything
        """
        if isinstance(value_list, list) or isinstance(value_list, set) or isinstance(value_list, tuple):
            return all(map(cls.get_list_empty, value_list))
        return False
    
    def check_report_characteristics(self, file_path:str, file_name:str) -> bool:
        """
        Method which is dedicated to check parameters of a file, is it empty
        is it necessary file, etc.
        Input:  file_path = full path to the file 
                file_name = file name
        Output: boolean value which signifies every value
        """
        value_bool = os.path.isfile(file_path)
        value_bool = value_bool and os.stat(file_path).st_size > 0
        value_name, value_ext = os.path.splitext(file_name)
        value_bool = value_bool and value_ext == format_xlsx
        if value_bool:
            try:
                value_xlxs = openpyxl.load_workbook(file_path)
                value_worksheets = [value_xlxs[f] for f in value_xlxs.sheetnames]
                value_worksheets_values = [[k for k in v.values] for v in value_worksheets]
                if self.get_list_empty(value_worksheets_values):
                    value_bool = False
                else:
                    value_list = [f for f in self.get_list_together(value_worksheets_values) if f not in ['', ' ']]
                    value_bool = bool(value_list)
            except Exception as e:
                #TODO add logger
                print('We have problems with reading of this file')
                value_bool = False
        check_today = value_name == self.name_today
        check_prev = value_name == self.name_previous
        if check_today:
            value_match = self.name_today
        elif check_prev:
            value_match = self.name_previous
        else:
            value_match = ''
        value_bool = value_bool and (check_today or check_prev)
        return value_bool, value_match

    def check_input(self) -> None:
        """
        Method which is dedicated to create basic xlxs value in cases of the 
        Input:  all previous values
        Output: we successfully
        """
        for f in [self.folder_report_path, self.folder_report_used]:
            self.check_folder(f)
        value_check = self.check_input_xlsx()
        """
        create file which is based on the datetime. To get know datetime in need
        use listdir. aftrthat, i need to write code for the xlxs
        I need to know the facts about the user via the os.environ
        I need to add .env for the server and token. 
        I need to add new email to this for working on the google disk
        I need 
    
        """
if __name__ == '__main__':
    a = ArchieveAnalyzer()
    a.check_input()