import pandas as pd
import os
import monk, load_data
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView, QAbstractScrollArea
from PrettyShower import PrettyShower

class PandasWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        self.root = os.getcwd()
        self.file_key = [".txt"]
        self.topics = []
        self.tags = []
        self.content = []
        self.all = []
        self.data_base = load_data.get_data(load_data.get_valid_files(self.root, self.file_key))
        self.shower = PrettyShower()
        QtWidgets.QWidget.__init__(self, parent=None)
        vLayout = QtWidgets.QVBoxLayout(self)

        # first line of buttons
        hLayout0 = QtWidgets.QHBoxLayout()
        # path button
        self.sRoot = QtWidgets.QLineEdit(self)
        self.sRoot.setPlaceholderText(os.getcwd())
        # file key
        self.sFileKey = QtWidgets.QLineEdit(self)
        self.sFileKey.setPlaceholderText("[.txt]")
        # or search
        self.sAll = QtWidgets.QLineEdit(self)
        self.sAll.setPlaceholderText("Tags or Content")
        # set button
        self.loadBtn0 = QtWidgets.QPushButton("Set", self)
        # set button function, load data function call
        self.loadBtn0.clicked.connect(self.set_conf_get_df)
        hLayout0.addWidget(self.sRoot)
        hLayout0.addWidget(self.sFileKey)
        hLayout0.addWidget(self.loadBtn0)
        hLayout0.addWidget(self.sAll)
        vLayout.addLayout(hLayout0)

        # second line of buttons
        hLayout = QtWidgets.QHBoxLayout()
        self.sTopics = QtWidgets.QLineEdit(self)
        self.sTopics.setPlaceholderText("Topics")
        self.sTags = QtWidgets.QLineEdit(self)
        self.sTags.setPlaceholderText("Tags")
        self.sContent = QtWidgets.QLineEdit(self)
        self.sContent.setPlaceholderText("Content")
        self.loadBtn = QtWidgets.QPushButton("Search", self)
        hLayout.addWidget(self.sTopics)
        hLayout.addWidget(self.sTags)
        hLayout.addWidget(self.sContent)
        hLayout.addWidget(self.loadBtn)
        vLayout.addLayout(hLayout)
        self.loadBtn.clicked.connect(self.search_df)

    def set_conf_get_df(self):
        root_temp = self.sRoot.text()
        file_key_temp = self.sFileKey.text().split(",")
        if not len(root_temp) < 2: self.root = root_temp
        if not len(file_key_temp[0]) == 0: self.file_key = file_key_temp

        self.data_base = load_data.get_data(load_data.get_valid_files(self.root, self.file_key))


    def search_df(self):
        self.topics = self.sTopics.text().split(",")
        self.tags = self.sTags.text().split(",")
        self.content = self.sContent.text().split(",")
        self.all = self.sAll.text().split(",")

        if len(self.topics[0]) == 0: self.topics = []
        if len(self.tags[0]) == 0: self.tags = []
        if len(self.content[0]) == 0: self.content = []

        # if search all is set, set other searches
        if len(self.all[0]) == 0: self.all = []
        else:
            self.tags = self.all
            self.content = self.all

        self.df_show = monk.search(self.data_base, topics=self.topics, tags=self.tags, content=self.content)
        self.shower.show(self.df_show)
        # if all fields are cleared after failed search, refresh with base frame
        # if self.df_show.topics.tolist()[0] == "no result":
        #     self.df_show = self.data_base

