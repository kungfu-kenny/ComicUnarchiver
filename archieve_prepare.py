import os
from pprint import pprint
from config import (origin_limited,
                    origin_oneshot,
                    separator,
                    folder_workspace,
                    destination_limited,
                    destination_oneshot)


class ArchieveBasics:
    """
    class which is dedicated to produce new values of the 
    """
    def __init__(self):
        self.name_origin, self.name_destination = 'origin', 'destination'
        self.name_type = [self.name_origin, self.name_destination]
        self.folders_origin = {
            origin_limited: folder_workspace,
            origin_oneshot: folder_workspace}
        self.folders_destination = {
            destination_limited: folder_workspace,
            destination_oneshot: folder_workspace}
        self.folders_status = {origin_oneshot: False,
            origin_limited: True,
            destination_oneshot: False,
            destination_limited: True}
    
    @staticmethod
    def get_path(*args, **kwargs) -> str:
        """
        Static method which is dedicated to produce basic path
        Input:  all path which can be used
        Output: string for all of that
        """
        sep = separator if 'sep' not in kwargs.keys() else kwargs['sep']
        return sep.join(args)

    @staticmethod
    def create_folder(path_folder:str) -> None:
        """
        Static method which is dedicated to create folders
        Input:  path_folder = ful path to create
        Output: None
        """
        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

    def return_only_files(self, path_directory:str) -> list:
        """
        Static method which returns values to the directory if it is file
        Input:  path_directory = path to the location of this directory
        Output: list with all files
        """
        return [v for v in os.listdir(path_directory) if os.path.isfile(self.get_path(path_directory, v))]

    def find_directory_files(self, path_directory:str, path_type:bool) -> (list, dict):
        """
        Method which is dedicated to work with files
        Input:  path_directory = path to the directory where to put values
                path_type = boolean which means folder of folders or not
        Output: list or dictionary of lists
        """
        if path_type:
            values_lists = [v for v in os.listdir(path_directory) if os.path.isdir(self.get_path(path_directory, v))]
            return {self.get_path(path_directory, v): self.return_only_files(self.get_path(path_directory, v)) for v in values_lists}
        return {path_directory: self.return_only_files(path_directory)}

    def return_file_size(self, path_file:str, path_list:list) -> int:
        """
        Method which is dedicated to return size of the images
        Input:  path_file = path where to take these values
                path_list = list of the files
        Output: size of the files inside all of the folders
        """
        path_list_files = [self.get_path(path_file, v) for v in path_list]
        return sum([os.stat(v).st_size for v in path_list_files]) if path_list_files else 0

    def optimize_by_memory(self, folder_dict:dict) -> dict:
        """
        Method which is dedicated to perform less hevay folders on first and after them other
        Input:  folder_dict = dictionary with new values
        Output: these dictionary only optimized with a memory size
        """
        return sorted([[self.return_file_size(folder, files), folder, files] for folder, files in folder_dict.items()], key=lambda x: x[0])
        
    def check_values(self) -> dict:
        """
        Method which is dedicated to 
        Input:  all inserted values
        Output: we created values for all of that
        """
        folders_all = {}
        for path_dictionary, path_name in zip([self.folders_origin, self.folders_destination], self.name_type):
            folders_all[path_name] = {}
            for path_folder, path_begin in path_dictionary.items():
                path_full = self.get_path(path_begin, path_folder)
                folders_all[path_name][path_folder] = path_full
                self.create_folder(path_full)
        return folders_all

    def optimize_file_type(self, folder_dict:dict) -> dict:
        """
        Method which is dedicated to make optimization by the file type
        Input:  folder_dict 
        """
        return folder_dict


class ArchieveValues(ArchieveBasics):
    """
    class which is dedicated to work with as an basic archiever
    """
    def __init__(self):
        super().__init__()
        self.folders_all = self.check_values()
        
    def make_check_input(self):
        """
        Method which is dedicated to produce the input data check
        Input:  all previous values
        Output: values which we would currently use
        """
        folders_presense = {}
        for name in self.folders_all[self.name_origin]:
            folders_presense.update(self.find_directory_files(self.folders_all[self.name_origin][name], self.folders_status[name]))
        print('===============================================') 
        pprint(folders_presense)
        print('===============================================')
        folders_presense = self.optimize_file_type(folders_presense)
        list_memory_optimized = self.optimize_by_memory(folders_presense)
        print('===============================================') 
        pprint(list_memory_optimized)


if __name__ == "__main__":
    a = ArchieveValues()
    a.make_check_input()