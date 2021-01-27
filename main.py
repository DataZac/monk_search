import load_data, monk
import pandas as pd
import pdb
import collections
from pprint import  pprint
import pandas_test_widget
from PyQt5 import QtWidgets, uic, QtCore
import sys
from tkinter import *
from tkinter import messagebox
import os


def show_initial_window(message):
    window = Tk()
    window.wm_withdraw()
    #message at x:200,y:200
    window.geometry("1x1+200+200")#remember its .geometry("WidthxHeight(+or-)X(+or-)Y")
    messagebox.showinfo(title="MonkSearch Info", message=message)


if __name__ == '__main__':
    # pd.set_option('display.max_columns', 5)  # or 1000
    # pd.set_option('display.max_rows', 100)  # or 1000w
    # pd.set_option('display.max_colwidth', 50)  # or 199
    # pd.set_option('display.width', 200)  # or 199


    # /home/jonas/Shared/Notes_usages
    # D:\Projects\Privat\Coding\monk_search\data
    PATTERN = [".txt"]
    SEARCH_ROOT = os.getcwd()

    initial_message = """
    Default pattern: {},
    Default root: {}
    
    Usage notes:
    Enter patterns e.g. in form 'xs1.txt,xs2.txt' or 'xs1,xs2'
    
    """.format(PATTERN, SEARCH_ROOT)
    show_initial_window(initial_message)

    df = load_data.get_data(load_data.get_valid_files(SEARCH_ROOT, PATTERN))

    app = QtWidgets.QApplication(sys.argv)
    w = pandas_test_widget.PandasWidget(df)
    w.resize(1200, 150)
    w.show()
    sys.exit(app.exec_())

