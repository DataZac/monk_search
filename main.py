import load_data, monk

import pandas as pd

import pdb

from tabulate import tabulate

import collections

from pprint import  pprint

import pandas_test_widget

from PyQt5 import QtWidgets, uic, QtCore

import sys









# d = df.to_dict(orient="records")

# l = []

# for item in d:

#     item_ordered = collections.OrderedDict(item)

#     item_ordered.move_to_end("tags")

#     item_ordered.move_to_end("content")

#     item_ordered.move_to_end("notes")

#     l.append(item_ordered)



if __name__ == '__main__':

    # pd.set_option('display.max_columns', 5)  # or 1000

    # pd.set_option('display.max_rows', 100)  # or 1000w

    # pd.set_option('display.max_colwidth', 50)  # or 199

    # pd.set_option('display.width', 200)  # or 199



    PATTERN = [".txt"]

    SEARCH_ROOT = "./"

    df = load_data.get_data(load_data.get_valid_files(SEARCH_ROOT, PATTERN))

    # /home/jonas/Shared/Notes_usages



    app = QtWidgets.QApplication(sys.argv)

    w = pandas_test_widget.PandasWidget(df)

    w.resize(1200, 1000)

    w.show()

    sys.exit(app.exec_())

