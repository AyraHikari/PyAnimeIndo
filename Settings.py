# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.EnvSettings = QtWidgets.QGroupBox(self.tab)
        self.EnvSettings.setGeometry(QtCore.QRect(10, 10, 561, 81))
        self.EnvSettings.setObjectName("EnvSettings")
        self.mpvCustomPath = QtWidgets.QLineEdit(self.EnvSettings)
        self.mpvCustomPath.setGeometry(QtCore.QRect(110, 20, 351, 21))
        self.mpvCustomPath.setObjectName("mpvCustomPath")
        self.mpvBrowse = QtWidgets.QPushButton(self.EnvSettings)
        self.mpvBrowse.setGeometry(QtCore.QRect(470, 20, 75, 23))
        self.mpvBrowse.setObjectName("mpvBrowse")
        self.label = QtWidgets.QLabel(self.EnvSettings)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 21))
        self.label.setObjectName("label")
        self.testMPV = QtWidgets.QPushButton(self.EnvSettings)
        self.testMPV.setGeometry(QtCore.QRect(470, 50, 75, 23))
        self.testMPV.setObjectName("testMPV")
        self.label_15 = QtWidgets.QLabel(self.EnvSettings)
        self.label_15.setGeometry(QtCore.QRect(10, 60, 451, 16))
        self.label_15.setObjectName("label_15")
        self.ProxySettings = QtWidgets.QGroupBox(self.tab)
        self.ProxySettings.setEnabled(True)
        self.ProxySettings.setGeometry(QtCore.QRect(10, 100, 551, 81))
        self.ProxySettings.setObjectName("ProxySettings")
        self.HttpProxyT = QtWidgets.QLabel(self.ProxySettings)
        self.HttpProxyT.setGeometry(QtCore.QRect(10, 22, 71, 16))
        self.HttpProxyT.setObjectName("HttpProxyT")
        self.HttpProxy = QtWidgets.QLineEdit(self.ProxySettings)
        self.HttpProxy.setEnabled(True)
        self.HttpProxy.setGeometry(QtCore.QRect(90, 20, 161, 20))
        self.HttpProxy.setPlaceholderText("")
        self.HttpProxy.setObjectName("HttpProxy")
        self.HttpsProxy = QtWidgets.QLineEdit(self.ProxySettings)
        self.HttpsProxy.setEnabled(True)
        self.HttpsProxy.setGeometry(QtCore.QRect(90, 50, 161, 20))
        self.HttpsProxy.setObjectName("HttpsProxy")
        self.HttpsProxyT = QtWidgets.QLabel(self.ProxySettings)
        self.HttpsProxyT.setGeometry(QtCore.QRect(10, 52, 71, 16))
        self.HttpsProxyT.setObjectName("HttpsProxyT")
        self.ProxyTest = QtWidgets.QPushButton(self.ProxySettings)
        self.ProxyTest.setEnabled(True)
        self.ProxyTest.setGeometry(QtCore.QRect(270, 20, 75, 23))
        self.ProxyTest.setObjectName("ProxyTest")
        self.retms = QtWidgets.QLabel(self.ProxySettings)
        self.retms.setGeometry(QtCore.QRect(270, 50, 47, 13))
        self.retms.setText("")
        self.retms.setObjectName("retms")
        self.label_13 = QtWidgets.QLabel(self.ProxySettings)
        self.label_13.setGeometry(QtCore.QRect(345, 60, 200, 16))
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 190, 551, 101))
        self.groupBox_2.setObjectName("groupBox_2")
        self.slowMode = QtWidgets.QCheckBox(self.groupBox_2)
        self.slowMode.setGeometry(QtCore.QRect(20, 20, 521, 17))
        self.slowMode.setChecked(False)
        self.slowMode.setObjectName("slowMode")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 551, 81))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(10, 22, 81, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setGeometry(QtCore.QRect(110, 20, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setGeometry(QtCore.QRect(110, 48, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(10, 50, 101, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_3)
        self.label_6.setGeometry(QtCore.QRect(240, 22, 81, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_5.setGeometry(QtCore.QRect(320, 20, 211, 20))
        self.lineEdit_5.setText("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.installA4k1 = QtWidgets.QPushButton(self.tab_3)
        self.installA4k1.setGeometry(QtCore.QRect(10, 10, 141, 31))
        self.installA4k1.setObjectName("installA4k1")
        self.installA4k2 = QtWidgets.QPushButton(self.tab_3)
        self.installA4k2.setGeometry(QtCore.QRect(160, 10, 141, 31))
        self.installA4k2.setObjectName("installA4k2")
        self.uninstallA4k = QtWidgets.QPushButton(self.tab_3)
        self.uninstallA4k.setGeometry(QtCore.QRect(310, 10, 141, 31))
        self.uninstallA4k.setObjectName("uninstallA4k")
        self.groupBox = QtWidgets.QGroupBox(self.tab_3)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 551, 171))
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(100, 20, 131, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 71, 20))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(100, 50, 131, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 50, 71, 20))
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(100, 80, 131, 20))
        self.label_7.setObjectName("label_7")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_7.setEnabled(False)
        self.lineEdit_7.setGeometry(QtCore.QRect(10, 110, 71, 20))
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(100, 110, 131, 20))
        self.label_8.setObjectName("label_8")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_6.setEnabled(False)
        self.lineEdit_6.setGeometry(QtCore.QRect(10, 80, 71, 20))
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(330, 80, 131, 20))
        self.label_11.setObjectName("label_11")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(330, 50, 131, 20))
        self.label_10.setObjectName("label_10")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_8.setEnabled(False)
        self.lineEdit_8.setGeometry(QtCore.QRect(240, 20, 71, 20))
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_10.setEnabled(False)
        self.lineEdit_10.setGeometry(QtCore.QRect(240, 80, 71, 20))
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(330, 20, 131, 20))
        self.label_9.setObjectName("label_9")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_9.setEnabled(False)
        self.lineEdit_9.setGeometry(QtCore.QRect(240, 50, 71, 20))
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.presetA4k = QtWidgets.QComboBox(self.groupBox)
        self.presetA4k.setGeometry(QtCore.QRect(330, 110, 131, 22))
        self.presetA4k.setObjectName("presetA4k")
        self.presetA4k.addItem("")
        self.presetA4k.addItem("")
        self.presetA4k.addItem("")
        self.presetA4k.addItem("")
        self.presetA4k.addItem("")
        self.presetA4k.addItem("")
        self.presetA4k.addItem("")
        self.presetA4k.addItem("")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(240, 110, 81, 20))
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setGeometry(QtCore.QRect(10, 145, 531, 16))
        self.label_14.setObjectName("label_14")
        self.uninstallA4k_2 = QtWidgets.QPushButton(self.tab_3)
        self.uninstallA4k_2.setEnabled(False)
        self.uninstallA4k_2.setGeometry(QtCore.QRect(460, 10, 101, 31))
        self.uninstallA4k_2.setObjectName("uninstallA4k_2")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 10, 281, 221))
        self.groupBox_4.setObjectName("groupBox_4")
        self.resetSaved = QtWidgets.QPushButton(self.groupBox_4)
        self.resetSaved.setGeometry(QtCore.QRect(10, 20, 161, 41))
        self.resetSaved.setObjectName("resetSaved")
        self.resetHistory = QtWidgets.QPushButton(self.groupBox_4)
        self.resetHistory.setGeometry(QtCore.QRect(10, 70, 161, 41))
        self.resetHistory.setObjectName("resetHistory")
        self.resetData = QtWidgets.QPushButton(self.groupBox_4)
        self.resetData.setGeometry(QtCore.QRect(10, 120, 161, 41))
        self.resetData.setObjectName("resetData")
        self.resetConfig = QtWidgets.QPushButton(self.groupBox_4)
        self.resetConfig.setGeometry(QtCore.QRect(10, 170, 161, 41))
        self.resetConfig.setObjectName("resetConfig")
        self.tabWidget.addTab(self.tab_4, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.saveConfig = QtWidgets.QPushButton(Dialog)
        self.saveConfig.setObjectName("saveConfig")
        self.verticalLayout.addWidget(self.saveConfig)
        self.exitBtn = QtWidgets.QPushButton(Dialog)
        self.exitBtn.setObjectName("exitBtn")
        self.verticalLayout.addWidget(self.exitBtn)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pengaturan"))
        self.EnvSettings.setTitle(_translate("Dialog", "Path Environment*"))
        self.mpvCustomPath.setPlaceholderText(_translate("Dialog", "Default"))
        self.mpvBrowse.setText(_translate("Dialog", "Browse"))
        self.label.setText(_translate("Dialog", "Video Player Path: "))
        self.testMPV.setText(_translate("Dialog", "Test Player"))
        self.label_15.setText(_translate("Dialog", "Di rekomendasikan menggunakan MPV, atau VLC jika tidak menggunakan Anime4k"))
        self.ProxySettings.setTitle(_translate("Dialog", "Proxy"))
        self.HttpProxyT.setText(_translate("Dialog", "Http Proxy:"))
        self.HttpsProxy.setPlaceholderText(_translate("Dialog", "Opsional..."))
        self.HttpsProxyT.setText(_translate("Dialog", "Https Proxy:"))
        self.ProxyTest.setText(_translate("Dialog", "Tes koneksi"))
        self.label_13.setText(_translate("Dialog", "Restart aplikasi untuk menerapkan proxy"))
        self.groupBox_2.setTitle(_translate("Dialog", "Lainnya"))
        self.slowMode.setText(_translate("Dialog", "Mode lambat (centang ini jika kecepatan internet anda lambat)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Sistem"))
        self.groupBox_3.setTitle(_translate("Dialog", "Tampilan awal"))
        self.label_4.setText(_translate("Dialog", "Judul Aplikasi: "))
        self.lineEdit_3.setText(_translate("Dialog", "PyAnimeIndo"))
        self.lineEdit_4.setText(_translate("Dialog", "By Ayra Hikari"))
        self.label_5.setText(_translate("Dialog", "Sub-judul Aplikasi: "))
        self.label_6.setText(_translate("Dialog", "Gambar Profil:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tampilan"))
        self.installA4k1.setText(_translate("Dialog", "Install (High-end VGA)"))
        self.installA4k2.setText(_translate("Dialog", "Install (Low-end VGA)"))
        self.uninstallA4k.setText(_translate("Dialog", "Uninstall"))
        self.groupBox.setTitle(_translate("Dialog", "Shortcut"))
        self.label_2.setText(_translate("Dialog", "Anime4K: Mode A (HQ)"))
        self.lineEdit.setText(_translate("Dialog", "CTRL+1"))
        self.label_3.setText(_translate("Dialog", "Anime4K: Mode B (HQ)"))
        self.lineEdit_2.setText(_translate("Dialog", "CTRL+2"))
        self.label_7.setText(_translate("Dialog", "Anime4K: Mode C (HQ)"))
        self.lineEdit_7.setText(_translate("Dialog", "CTRL+0"))
        self.label_8.setText(_translate("Dialog", "Clear GLSL shaders"))
        self.lineEdit_6.setText(_translate("Dialog", "CTRL+3"))
        self.label_11.setText(_translate("Dialog", "Anime4K: Mode C+A (HQ)"))
        self.label_10.setText(_translate("Dialog", "Anime4K: Mode B+B (HQ)"))
        self.lineEdit_8.setText(_translate("Dialog", "CTRL+4"))
        self.lineEdit_10.setText(_translate("Dialog", "CTRL+6"))
        self.label_9.setText(_translate("Dialog", "Anime4K: Mode A+A (HQ)"))
        self.lineEdit_9.setText(_translate("Dialog", "CTRL+5"))
        self.presetA4k.setCurrentText(_translate("Dialog", "Default"))
        self.presetA4k.setItemText(0, _translate("Dialog", "Default"))
        self.presetA4k.setItemText(1, _translate("Dialog", "Off"))
        self.presetA4k.setItemText(2, _translate("Dialog", "Mode A (HQ)"))
        self.presetA4k.setItemText(3, _translate("Dialog", "Mode B (HQ)"))
        self.presetA4k.setItemText(4, _translate("Dialog", "Mode C (HQ)"))
        self.presetA4k.setItemText(5, _translate("Dialog", "Mode A+A (HQ)"))
        self.presetA4k.setItemText(6, _translate("Dialog", "Mode B+B (HQ)"))
        self.presetA4k.setItemText(7, _translate("Dialog", "Mode C+A (HQ)"))
        self.label_12.setText(_translate("Dialog", "Default Preset: "))
        self.label_14.setText(_translate("Dialog", "*Anime4k hanya tersedia untuk MPV Player saja"))
        self.uninstallA4k_2.setText(_translate("Dialog", "Check"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Anime4k"))
        self.groupBox_4.setTitle(_translate("Dialog", "Database"))
        self.resetSaved.setText(_translate("Dialog", "Reset daftar tersimpan"))
        self.resetHistory.setText(_translate("Dialog", "Reset riwayat nonton"))
        self.resetData.setText(_translate("Dialog", "Reset semua data"))
        self.resetConfig.setText(_translate("Dialog", "Reset pengaturan"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Database"))
        self.saveConfig.setText(_translate("Dialog", "Save"))
        self.exitBtn.setText(_translate("Dialog", "Cancel"))
