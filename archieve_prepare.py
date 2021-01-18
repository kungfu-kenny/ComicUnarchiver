import os
import shutil
import rarfile
from pprint import pprint
from pdf2image import convert_from_path
from config import (origin_limited,
                    origin_oneshot,
                    separator,
                    folder_workspace,
                    format_usefull,
                    format_pdf,
                    format_cbr,
                    format_jpg,
                    format_jpeg,
                    format_image,
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
        self.folder_rechange = {
            origin_limited: destination_limited,
            origin_oneshot: destination_oneshot,
        }
    
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

    @staticmethod
    def remove_file(path_file:str, path_status:bool=False) -> None:
        """
        Static method which is dedicated to remove previously analyzed files
        Input:  path_file = file which we had successfully worked with
                path_status = status which signifies does we work with a folder or single file
        Output: None, we deleted file
        """
        if path_status:
            return shutil.rmtree(path_file)
        os.remove(path_file)

    @staticmethod
    def move_file(path_original:str, path_destination:str) -> None:
        """
        Static method which is dedicated to move values on the cbr/cbz values
        Input:  path_original = original path of the files
                path_destination = path where to work
        Output: we changed name and move theme where to make
        """
        os.replace(path_original, path_destination)

    def return_only_files(self, path_directory:str) -> list:
        """
        Static method which returns values to the directory if it is file
        Input:  path_directory = path to the location of this directory
        Output: list with all files
        """
        return [v for v in os.listdir(path_directory) if os.path.isfile(self.get_path(path_directory, v))]

    def return_folder_output(self, file_name:str) -> str:
        """
        Method which is dedicated to create output folders to the everything which was set
        Input:  file_name = string which is dedicated to  
        Output: we created folders and subfolders if it is required
        """
        value_list, value_return = file_name.split(separator), file_name
        if len(value_list) > 1:
            value_replaced = [self.folder_rechange[v] if v in self.folder_rechange.keys() else v for v in value_list]
            if value_replaced == value_list:
                return value_return
            value_return = ''
            for tmp_folder in value_replaced:
                value_return = self.get_path(value_return, tmp_folder)
                self.create_folder(value_return)
        return value_return

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
        value_list = sorted([[self.return_file_size(folder, files), folder, files] for folder, files in folder_dict.items()], key=lambda x: x[0])
        return [[size, folder, files] for size, folder, files in value_list if size and files]

    @staticmethod
    def return_ext(file_path:str) -> (str, str):
        """
        Static method which is dedicated to return extenstion
        Input:  file_path = full path to the file
        Output: string which means the file ext
        """
        file_name, file_ext = os.path.splitext(file_path)
        return file_name, file_ext.strip().lower()

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
        Input:  folder_dict = dictionary with all possible files inside
        Output: we checked everything on the 
        """
        value_dict = {}
        for folder_path, folder_files in folder_dict.items():
            value_list = []
            for folder_file in folder_files:
                _, file_ext = self.return_ext(self.get_path(folder_path, folder_file))
                if file_ext in format_usefull:
                    value_list.append(folder_file)
            value_dict[folder_path] = value_list
        return value_dict

    def correct_everything(self, value_type:str) -> None:
        """
        Method which is dedicated to clear everything after the execution
        Input:  value_type = type which is going to be fully cleared
        Output: we cleared everything for using 
        """
        if value_type not in self.name_type:
            return None
        elif value_type in self.name_type and value_type == self.name_origin:
            dict_location = self.folders_origin
        elif value_type in self.name_type and value_type == self.name_destination:
            dict_location = self.folders_destination
        for folder_clear in [self.get_path(value, key) for key, value in dict_location.items()]:
            for folder_value in os.listdir(folder_clear):
                folder_path = self.get_path(folder_clear, folder_value)
                value_bool = False if os.path.isfile(folder_path) else True 
                self.remove_file(folder_path, value_bool)


class Archiever(ArchieveBasics):
    """
    class which is dedicated unarchieve values
    """
    def __init__(self):
        super().__init__()
        self.pdf_format_output = 'JPEG'
        self.archieve_method = {
            format_pdf: self.unarchieve_pdf,
            format_cbr: self.unarchive_cbr,
        }

    def unarchieve_pdf(self, file_path:str, file_output:str) -> None:
        """
        Method which is dedicated to unarchieve pdf files
        Input:  file_path = path to this file
                file_output = folder for aking the output to the files
        Output: we successfully created images from pdf
        """
        list_images = convert_from_path(file_path)
        for number, pages in enumerate(list_images):
            pages.save(self.get_path(file_output, f"{number}{format_jpg}"), self.pdf_format_output)

    def unarchive_cbr(self, file_path:str, file_output:str) -> None:
        """
        Method which is dedicated to unarchive the cbr files to the selected folders
        Input:  file_path = path to the selected file
                file_output = path to folder which we are going to work with
        Output: we successfully created list of images from the cbr
        """
        with rarfile.RarFile(file_path) as archive:
            value_within_folder = [True if separator in v else False for v in archive.namelist()]
            for value_page, value_name in enumerate(archive.namelist()):
                if separator in value_name:
                    _, value_format = self.return_ext(value_name)
                    if value_format in format_image:
                        file_input = self.get_path(file_output, value_name)
                        file_output_tmp = self.get_path(file_output, f"{value_page}{value_format}")
                        archive.extract(value_name, file_output)
                        self.move_file(file_input, file_output_tmp)
                    else:
                        #TODO add this posibility later
                        pass
            list_remove = [self.get_path(file_output, v) for v in os.listdir(file_output) if os.path.isdir(self.get_path(file_output, v))]
            for k in list_remove:
                self.remove_file(k, True)
            
    def unarchive_cbz(self, file_path:str, file_output:str) -> None:
        """
        Method which is dedicated to unarchive cbz files to the folders
        Input:  file_path = path of the origin
                file_output = place where to store files
        Output: we successfully unarchived everything
        """
        pass
    
    def unarchive_rar(self, file_path:str, file_output:str) -> None:
        """
        Method which is dedicated to unarchive rar files to the folders
        Input:  file_path = path of the origin
                file_output = place where to store files
        Output: we successfully unarchived everything
        """
        pass

    def unarchive_zip(self, file_path:str, file_output:str) -> None:
        """
        Method which is dedicated to unarchive zip files to the folders
        Input:  file_path = path of the origin
                file_output = place where to store files
        Output: we successfully unarchived everything
        """
        pass


class ArchieveValues(Archiever):
    """
    class which is dedicated to work with as an basic archiever
    """
    def __init__(self):
        super().__init__()
        self.folders_all = self.check_values()
        
    def correct_input_files(self, folder_path:str, folder_type:bool=False) -> None:
        """
        Method which is dedicated to remove values which were currently produced
        Input:  folder_path = path of the 
                folder_type = boolean value 
        Output: we removed processed folder
        """
        if folder_path.split(separator)[-1] not in self.folder_rechange.keys():
            self.remove_file(folder_path, True)

    def produce_extraction(self, folder_path:str, folder_file:str) -> None:
        """
        Method which is dedicated to produce basic extraction of the file
        Input:  folder_path = folder where is this file
        Output: we have extracted file to selected folder
        """
        path_input = self.get_path(folder_path, folder_file)
        name, ext = self.return_ext(path_input)
        path_output = self.return_folder_output(name)
        if ext in self.archieve_method.keys():
            self.archieve_method[ext](path_input, path_output)
            self.remove_file(path_input)
        
    def make_check_input(self):
        """
        Method which is dedicated to produce the input data check
        Input:  all previous values
        Output: values which we would currently use
        """
        folders_presense = {}
        for name in self.folders_all[self.name_origin]:
            folders_presense.update(self.find_directory_files(self.folders_all[self.name_origin][name], self.folders_status[name]))
        folders_presense = self.optimize_file_type(folders_presense)
        list_memory_optimized = self.optimize_by_memory(folders_presense)
        if not list_memory_optimized:
            return None
        for folder_size, folder_path, folder_files in list_memory_optimized:
            # TODO do I need a concurrency now?
            for folder_file in folder_files:
                self.produce_extraction(folder_path, folder_file)
            self.correct_input_files(folder_path)
        self.correct_everything(self.name_origin)
                
    def make_check_output(self):
        """
        Method which is dedicated to produce further development in case to write inside the database
        Input:  all previous values
        Output: values which were transmitted to the database
        """
        #TODO do we need to add metadata in that cases? Or remove
        pass


if __name__ == "__main__":
    a = ArchieveValues()
    a.make_check_input()