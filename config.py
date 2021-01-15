import os

separator = os.sep
folder_workspace = os.path.dirname(os.path.realpath(__file__))
origin_oneshot = 'origin_oneshot'
origin_limited = 'origin_limited'

destination_oneshot = 'destination_oneshot'
destination_limited = 'destination_limited'
format_cbr, format_cbz, format_pdf = 'cbr', 'cbz', 'pdf' 
format_rar, format_zip = 'rar', 'zip'

list_types_image = ['.jpg', '.jpeg', '.png', '.svg']
list_types_remove = [] 
recursion_max = 2
processes_max = 6