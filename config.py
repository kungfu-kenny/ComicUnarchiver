import os
from itertools import chain

separator = os.sep
folder_workspace = os.path.dirname(os.path.realpath(__file__))
origin_oneshot = 'origin_oneshot'
origin_limited = 'origin_limited'

destination_oneshot = 'destination_oneshot'
destination_limited = 'destination_limited'
format_cbr, format_cbz, format_pdf = '.cbr', '.cbz', '.pdf' 
format_rar, format_zip = '.rar', '.zip'
format_comic = [format_cbr, format_cbz, format_pdf]
format_archives = [format_rar, format_zip]
format_usefull = list(chain(format_comic, format_archives))
format_jpg, format_jpeg, format_png, format_svg = '.jpg', '.jpeg', '.png', '.svg'
format_image = [format_jpg, format_jpeg, format_png, format_svg]
list_types_remove = [] 
recursion_max = 2
processes_max = 6