# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnimeListWidget.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AnimeIndo(object):
    def setupUi(self, AnimeIndo):
        AnimeIndo.setObjectName("AnimeIndo")
        AnimeIndo.resize(670, 504)
        AnimeIndo.setMaximumSize(QtCore.QSize(670, 520))
        self.centralwidget = QtWidgets.QWidget(AnimeIndo)
        self.centralwidget.setObjectName("centralwidget")
        self.statusInfo = QtWidgets.QLabel(self.centralwidget)
        self.statusInfo.setGeometry(QtCore.QRect(506, 462, 161, 21))
        self.statusInfo.setText("")
        self.statusInfo.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.statusInfo.setObjectName("statusInfo")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 671, 481))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setObjectName("tabWidget")
        self.Terbaru = QtWidgets.QWidget()
        self.Terbaru.setObjectName("Terbaru")
        self.AnimeList = QtWidgets.QListWidget(self.Terbaru)
        self.AnimeList.setGeometry(QtCore.QRect(0, 0, 671, 478))
        self.AnimeList.setMinimumSize(QtCore.QSize(0, 0))
        self.AnimeList.setMaximumSize(QtCore.QSize(671, 500))
        self.AnimeList.setSizeIncrement(QtCore.QSize(0, 0))
        self.AnimeList.setBaseSize(QtCore.QSize(0, 0))
        self.AnimeList.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.AnimeList.setTabKeyNavigation(False)
        self.AnimeList.setProperty("showDropIndicator", False)
        self.AnimeList.setDragEnabled(False)
        self.AnimeList.setDragDropOverwriteMode(False)
        self.AnimeList.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.AnimeList.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.AnimeList.setIconSize(QtCore.QSize(120, 167))
        self.AnimeList.setMovement(QtWidgets.QListView.Static)
        self.AnimeList.setFlow(QtWidgets.QListView.LeftToRight)
        self.AnimeList.setProperty("isWrapping", True)
        self.AnimeList.setResizeMode(QtWidgets.QListView.Adjust)
        self.AnimeList.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.AnimeList.setGridSize(QtCore.QSize(120, 200))
        self.AnimeList.setViewMode(QtWidgets.QListView.IconMode)
        self.AnimeList.setModelColumn(0)
        self.AnimeList.setUniformItemSizes(True)
        self.AnimeList.setBatchSize(100)
        self.AnimeList.setWordWrap(False)
        self.AnimeList.setObjectName("AnimeList")
        self.tabWidget.addTab(self.Terbaru, "")
        self.Cari = QtWidgets.QWidget()
        self.Cari.setObjectName("Cari")
        self.searchBar = QtWidgets.QLineEdit(self.Cari)
        self.searchBar.setGeometry(QtCore.QRect(0, 0, 561, 23))
        self.searchBar.setObjectName("searchBar")
        self.searchBtn = QtWidgets.QPushButton(self.Cari)
        self.searchBtn.setGeometry(QtCore.QRect(560, 0, 85, 23))
        self.searchBtn.setObjectName("searchBtn")
        self.AnimeList_Search = QtWidgets.QListWidget(self.Cari)
        self.AnimeList_Search.setGeometry(QtCore.QRect(0, 25, 641, 453))
        self.AnimeList_Search.setMinimumSize(QtCore.QSize(0, 0))
        self.AnimeList_Search.setMaximumSize(QtCore.QSize(671, 500))
        self.AnimeList_Search.setSizeIncrement(QtCore.QSize(0, 0))
        self.AnimeList_Search.setBaseSize(QtCore.QSize(0, 0))
        self.AnimeList_Search.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.AnimeList_Search.setTabKeyNavigation(False)
        self.AnimeList_Search.setProperty("showDropIndicator", False)
        self.AnimeList_Search.setDragEnabled(False)
        self.AnimeList_Search.setDragDropOverwriteMode(False)
        self.AnimeList_Search.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.AnimeList_Search.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.AnimeList_Search.setIconSize(QtCore.QSize(225, 314))
        self.AnimeList_Search.setMovement(QtWidgets.QListView.Static)
        self.AnimeList_Search.setFlow(QtWidgets.QListView.LeftToRight)
        self.AnimeList_Search.setProperty("isWrapping", True)
        self.AnimeList_Search.setResizeMode(QtWidgets.QListView.Fixed)
        self.AnimeList_Search.setLayoutMode(QtWidgets.QListView.Batched)
        self.AnimeList_Search.setGridSize(QtCore.QSize(100, 250))
        self.AnimeList_Search.setViewMode(QtWidgets.QListView.IconMode)
        self.AnimeList_Search.setModelColumn(0)
        self.AnimeList_Search.setUniformItemSizes(True)
        self.AnimeList_Search.setBatchSize(100)
        self.AnimeList_Search.setWordWrap(False)
        self.AnimeList_Search.setObjectName("AnimeList_Search")
        self.tabWidget.addTab(self.Cari, "")
        AnimeIndo.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AnimeIndo)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 670, 21))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuTentang = QtWidgets.QMenu(self.menubar)
        self.menuTentang.setObjectName("menuTentang")
        AnimeIndo.setMenuBar(self.menubar)
        self.actionExit = QtWidgets.QAction(AnimeIndo)
        self.actionExit.setObjectName("actionExit")
        self.actionPengaturan = QtWidgets.QAction(AnimeIndo)
        self.actionPengaturan.setObjectName("actionPengaturan")
        self.menuSettings.addAction(self.actionPengaturan)
        self.menuSettings.addAction(self.actionExit)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuTentang.menuAction())

        self.retranslateUi(AnimeIndo)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AnimeIndo)

    def retranslateUi(self, AnimeIndo):
        _translate = QtCore.QCoreApplication.translate
        AnimeIndo.setWindowTitle(_translate("AnimeIndo", "PyAnimeIndo"))
        self.AnimeList.setSortingEnabled(False)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Terbaru), _translate("AnimeIndo", "Terbaru"))
        self.searchBar.setPlaceholderText(_translate("AnimeIndo", "Pencarian..."))
        self.searchBtn.setText(_translate("AnimeIndo", "Cari"))
        self.AnimeList_Search.setSortingEnabled(False)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Cari), _translate("AnimeIndo", "Cari"))
        self.menuSettings.setTitle(_translate("AnimeIndo", "Menu"))
        self.menuTentang.setTitle(_translate("AnimeIndo", "Tentang"))
        self.actionExit.setText(_translate("AnimeIndo", "Exit"))
        self.actionPengaturan.setText(_translate("AnimeIndo", "Pengaturan"))