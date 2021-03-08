import os
from itertools import chain

folder_workspace = os.path.dirname(os.path.realpath(__file__))

folder_report = 'folder_report'
folder_used_xlxs = 'used_xlxs'
format_xlsx = '.xlsx'

origin_oneshot = 'origin_oneshot'
origin_limited = 'origin_limited'

destination_oneshot = 'destination_oneshot'
destination_limited = 'destination_limited'
format_tar_special = '.tar.gz'
format_cbr, format_cbz, format_pdf = '.cbr', '.cbz', '.pdf' 
format_rar, format_zip, format_tar, format_tar_sec = '.rar', '.zip', '.tar', '.gz'
format_comic = [format_cbr, format_cbz, format_pdf]
format_archives = [format_rar, format_zip, format_tar, format_tar_sec]
format_usefull = list(chain(format_comic, format_archives))
format_jpg, format_jpeg, format_png, format_svg = '.jpg', '.jpeg', '.png', '.svg'
format_image = [format_jpg, format_jpeg, format_png, format_svg]
list_types_remove = [] 
recursion_max = 2
processes_max = 6