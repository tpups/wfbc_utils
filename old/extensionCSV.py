#Works to rename files with .csv extension (8/7/18)

import os, sys

for filename in os.listdir(os.path.dirname(os.path.abspath(__file__))):
    base_file, ext = os.path.splitext(filename)
    if ext == ".xls":
        os.rename(filename, base_file + ".csv")