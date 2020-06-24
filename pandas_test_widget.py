import pandas as pd

import monk, load_data

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QHeaderView, QAbstractScrollArea



class PandasModel(QtCore.QAbstractTableModel):

    def __init__(self, df = pd.DataFrame(), parent=None):

        QtCore.QAbstractTableModel.__init__(self, parent=parent)

        self._df = df



    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):

        if role != QtCore.Qt.DisplayRole:

            return QtCore.QVariant()



        if orientation == QtCore.Qt.Horizontal:

            try:

                return self._df.columns.tolist()[section]

            except (IndexError, ):

                return QtCore.QVariant()

        elif orientation == QtCore.Qt.Vertical:

            try:

                # return self.df.index.tolist()

                return self._df.index.tolist()[section]

            except (IndexError, ):

                return QtCore.QVariant()



    def data(self, index, role=QtCore.Qt.DisplayRole):



        if role == QtCore.Qt.SizeHintRole:

            print("Model.data(role == Qt.SizeHintRole) row: ; column",index.row(), index.column())

            # See below for the data structure.

            #return QtCore.QSize(500,5)



        if role != QtCore.Qt.DisplayRole:

            return QtCore.QVariant()



        if not index.isValid():

            return QtCore.QVariant()



        # ROLE FOR COL SIZE?

        # https://www.learnpyqt.com/courses/model-views/qtableview-modelviews-numpy-pandas/



        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))



    def setData(self, index, value, role):

        row = self._df.index[index.row()]

        col = self._df.columns[index.column()]

        if hasattr(value, 'toPyObject'):

            # PyQt4 gets a QVariant

            value = value.toPyObject()

        else:

            # PySide gets an unicode

            dtype = self._df[col].dtype

            if dtype != object:

                value = None if value == '' else dtype.type(value)

        self._df.set_value(row, col, value)

        return True



    def rowCount(self, parent=QtCore.QModelIndex()):

        return len(self._df.index)



    def columnCount(self, parent=QtCore.QModelIndex()):

        return len(self._df.columns)



    def sort(self, column, order):

        colname = self._df.columns.tolist()[column]

        self.layoutAboutToBeChanged.emit()

        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)

        self._df.reset_index(inplace=True, drop=True)

        self.layoutChanged.emit()





class PandasWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):

        self.root = "/home/jonas/Shared/Notes_usages"

        self.file_key = [".txt"]

        self.topics = []

        self.tags = []

        self.content = []

        self.notes = []

        self.all = []

        self.data_base = load_data.get_data(load_data.get_valid_files(self.root, self.file_key))

        QtWidgets.QWidget.__init__(self, parent=None)

        vLayout = QtWidgets.QVBoxLayout(self)



        hLayout0 = QtWidgets.QHBoxLayout()

        self.sRoot = QtWidgets.QLineEdit(self)

        self.sRoot.setPlaceholderText("./")

        self.sFileKey = QtWidgets.QLineEdit(self)

        self.sFileKey.setPlaceholderText("[.txt]")

        self.sAll = QtWidgets.QLineEdit(self)

        self.sAll.setPlaceholderText("Tags, Content or Notes")

        self.loadBtn0 = QtWidgets.QPushButton("Set", self)

        self.loadBtn0.clicked.connect(self.set_conf_get_df)

        hLayout0.addWidget(self.sRoot)

        hLayout0.addWidget(self.sFileKey)

        hLayout0.addWidget(self.loadBtn0)

        hLayout0.addWidget(self.sAll)

        vLayout.addLayout(hLayout0)





        hLayout = QtWidgets.QHBoxLayout()

        self.sTopics = QtWidgets.QLineEdit(self)

        self.sTopics.setPlaceholderText("Topics")

        self.sTags = QtWidgets.QLineEdit(self)

        self.sTags.setPlaceholderText("Tags")

        self.sContent = QtWidgets.QLineEdit(self)

        self.sContent.setPlaceholderText("Content")

        self.sNotes = QtWidgets.QLineEdit(self)

        self.sNotes.setPlaceholderText("Notes")

        hLayout.addWidget(self.sTopics)

        hLayout.addWidget(self.sTags)

        hLayout.addWidget(self.sContent)

        hLayout.addWidget(self.sNotes)



        self.loadBtn = QtWidgets.QPushButton("Search", self)

        hLayout.addWidget(self.loadBtn)

        vLayout.addLayout(hLayout)

        self.pandasTv = QtWidgets.QTableView(self)

        self.pandasTv.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        vLayout.addWidget(self.pandasTv)

        self.loadBtn.clicked.connect(self.search_df)

        self.pandasTv.setSortingEnabled(True)





    def set_conf_get_df(self):

        root_temp = self.sRoot.text()

        file_key_temp = self.sFileKey.text().split(",")

        if not len(root_temp) < 2: self.root = root_temp

        if not len(file_key_temp[0]) == 0: self.file_key = file_key_temp

        print("22xs", self.root, self.file_key)

        print("29sj9",self.data_base.head())

        self.data_base = load_data.get_data(load_data.get_valid_files(self.root, self.file_key))

        print("29sdfdj9",self.data_base.head())

        load_data.get_data(load_data.get_valid_files(" /home/jonas/Shared/Notes_usages/", [".txt"]))



    def search_df(self):

        print("Topics")

        self.topics = self.sTopics.text().split(",")

        print("Tags")

        self.tags = self.sTags.text().split(",")

        print("Content")

        self.content = self.sContent.text().split(",")

        print("Notes")

        self.notes = self.sNotes.text().split(",")

        print("All")

        self.all = self.sAll.text().split(",")



        if len(self.topics[0]) == 0: self.topics = []

        if len(self.tags[0]) == 0: self.tags = []

        if len(self.content[0]) == 0: self.content = []

        if len(self.notes[0]) == 0: self.notes = []



        # if search all is set, set other searches

        if len(self.all[0]) == 0: self.all = []

        else:

            self.tags = self.all

            self.content = self.all

            self.notes = self.all



        self.df_show = monk.search(self.data_base, topics=self.topics, tags=self.tags, content=self.content, notes=self.notes)



        # if all fields are cleared after failed search, refresh with base frame

        # if self.df_show.topics.tolist()[0] == "no result":

        #     self.df_show = self.data_base



        model = PandasModel(self.df_show)

        self.pandasTv.setModel(model)

        self.pandasTv.setColumnWidth(1, 300)

        self.pandasTv.setColumnWidth(2, 800)

        self.pandasTv.setColumnWidth(3, 1200)

        # self.pandasTv.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        #self.pandasTv.columnResized(1, 200, 2000)

        #self.pandasTv.resizeColumnToContents(2)

        #self.pandasTv.resizeColumnToContents(3)

        # self.pandasTv.resizeColumnsToContents()

        #self.pandasTv.resizeRowToContents(True)
