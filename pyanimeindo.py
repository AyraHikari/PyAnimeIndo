import sys, time, requests, threading, webbrowser
import subprocess as subp
from platform import python_version

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog
)
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.uic import loadUi

from AnimeListWidget import Ui_AnimeIndo
from AnimeInfoWidget import Ui_Dialog as Ui_AnimeInfo
from About import Ui_Dialog as Ui_About
from Settings import Ui_Dialog as Ui_Settings

from API.animeindo import get_main, get_episodes, get_download, searchAnime
from API.zdl import zdl
from utils.utils import remove_first_end_spaces
from utils.opendialog import OpenDialogApp

DEBUG = False


class MainWindow(QMainWindow, Ui_AnimeIndo):
	dataLatest = {}

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		t = threading.Thread(target=self.getLatest)
		t.start()
		self.AnimeList.doubleClicked.connect(self.info)
		self.AnimeList_Search.doubleClicked.connect(self.infoS)
		#self.searchBar.textChanged.connect(self.search)
		self.searchBar.editingFinished.connect(self.search)
		self.searchBtn.clicked.connect(self.search)
		self.menuTentang.aboutToShow.connect(self.about)
		self.actionPengaturan.triggered.connect(self.settings)
		self.actionExit.triggered.connect(self.close)

	def getLatest(self):
		self.AnimeList.clear()
		ongoing = get_main()
		for data in ongoing:
			#self.addThumbThread(data)
			t = threading.Thread(target=self.addThumbThread, args=(data,))
			t.start()

	def addThumbThread(self, data, is_search=False):
		self.statusInfo.setText("Mendapatkan data...")
		anime = QtWidgets.QListWidgetItem()
		anime.setText(data['title'])
		image = QtGui.QPixmap()
		image.loadFromData(requests.get(data['img']).content)
		anime.setIcon(QtGui.QIcon(image))
		anime.setStatusTip(data['url'])
		font = QtGui.QFont()
		font.setFamily("Segoe UI")
		anime.setFont(font)
		if is_search:
			self.AnimeList_Search.addItem(anime)
		else:
			self.AnimeList.addItem(anime)
		self.statusInfo.setText("")
		

	def info(self):
		d = self.AnimeList.currentItem().statusTip()
		dialog = AnimeInfo(self)
		dialog.show()
		t = threading.Thread(target=dialog.loadURL, args=(d,))
		t.start()

	def infoS(self):
		d = self.AnimeList_Search.currentItem().statusTip()
		dialog = AnimeInfo(self)
		dialog.show()
		t = threading.Thread(target=dialog.loadURL, args=(d,))
		t.start()

	def search(self, data=None):
		self.statusInfo.setText("Mencari...")
		data = self.searchBar.text()
		t = threading.Thread(target=self.searchThread, args=(data,))
		t.start()

	def searchThread(self, title):
		self.AnimeList_Search.clear()
		printd(title)
		lists = searchAnime(title)
		for data in lists:
			#self.addThumbThread(data)
			t = threading.Thread(target=self.addThumbThread, args=(data, True,))
			t.start()
		self.statusInfo.setText("")

	def about(self):
		dialog = About(self)
		dialog.show()

	def settings(self):
		dialog = Settings(self)
		dialog.show()


class AnimeInfo(QDialog, Ui_AnimeInfo):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.AnimeEps.itemClicked.connect(self.getQuality)
		self.AnimeQuality.itemClicked.connect(self.getDownload)
		self.StreamingBtn.clicked.connect(self.doStreaming)
		self.DownloadBtn.clicked.connect(self.doDownload)

	def loadURL(self, data):
		# Get Anime
		printd("Fetching: " + data)
		data = get_episodes(data)

		image = QtGui.QPixmap()
		image.loadFromData(requests.get(data['cover']).content)
		dataTitle = remove_first_end_spaces(data['title'].lower().replace("subtitle indonesia", "").title())
		self.AnimeTitle.setText(dataTitle)
		self.AnimeDesc.setText(data['info'] + "\n\n" + data['sinopsis'])
		self.AnimeCover.setPixmap(image)

		self.setWindowTitle(remove_first_end_spaces(data['info'].lower().split("judul:")[1].split("\n")[0]).title())

		# Parse episodes
		self.AnimeEps.clear()
		for item in data['episodes']:
			eps_title = item['title'].lower().replace("subtitle indonesia", "")
			if data['info']:
				eps_title = eps_title.replace(remove_first_end_spaces(data['info'].lower().split("judul:")[1].split("\n")[0]), "")
			eps_title = remove_first_end_spaces(eps_title.replace(dataTitle.lower(), "")).title()

			eps = QtWidgets.QListWidgetItem()
			eps.setText(eps_title)
			eps.setStatusTip(item['url'])
			self.AnimeEps.addItem(eps)

		self.AnimeEps.setEnabled(True)

	def getQuality(self, data):
		t = threading.Thread(target=self.getQualityThread, args=(data,))
		t.start()
		
	def getQualityThread(self, data):
		targeturl = data.statusTip()
		printd("Fetching: " + targeturl)
		webdata = get_download(targeturl)

		# Parse quality
		self.AnimeQuality.clear()
		for item in webdata:
			eps = QtWidgets.QListWidgetItem()
			eps.setText(item)
			eps.setStatusTip(webdata[item])
			self.AnimeQuality.addItem(eps)

		self.AnimeQuality.setEnabled(True)
		self.DownloadBtn.setDisabled(True)
		self.StreamingBtn.setDisabled(True)

	def getDownload(self, data):
		targeturl = self.AnimeQuality.currentItem().statusTip()
		self.DownloadBtn.setEnabled(True)
		if "zippyshare" in targeturl:
			self.StreamingBtn.setEnabled(True)
		else:
			self.StreamingBtn.setEnabled(False)
		self.downloadURL.setPlainText(targeturl)

	def doStreaming(self, data):
		self.disabledAll()
		iswork, comment = checkMpvWorking()
		if not iswork:
			alert = QMessageBox()
			alert.setText(comment)
			alert.exec()
			dialog = Settings(self)
			dialog.show()
			self.enabledAll()
			return
		targeturl = self.AnimeQuality.currentItem().statusTip()
		printd("Fetching: " + targeturl)
		zdirect = zdl(targeturl)

		#subp.Popen(str("D:\\Apps\\mpv" + "\\mpv " + zdirect), shell=True)
		t = threading.Thread(target=self.start_mpv, name="MPV Player", args=(zdirect,))
		t.start()

	def doDownload(self, data):
		targeturl = self.AnimeQuality.currentItem().statusTip()
		printd("Open: " + targeturl)
		webbrowser.open(targeturl)

	def disabledAll(self):
		self.AnimeEps.setDisabled(True)
		self.AnimeQuality.setDisabled(True)
		self.DownloadBtn.setDisabled(True)
		self.StreamingBtn.setDisabled(True)

	def enabledAll(self):
		self.AnimeEps.setEnabled(True)
		self.AnimeQuality.setEnabled(True)
		self.DownloadBtn.setEnabled(True)
		self.StreamingBtn.setEnabled(True)


	def start_mpv(self, url):
		mpv_cmd = "mpv"
		settings = loadSettings()
		if settings.get("mpv_path"):
			mpv_cmd = settings['mpv_path']

		p = subp.Popen(mpv_cmd + " " + url, shell=True)
		while p.poll() is None:
			time.sleep(1)
		self.enabledAll()


class About(QDialog, Ui_About):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.aboutSource.setText(self.aboutSource.text().replace("__pythonVer__", python_version()))
		self.aboutSource.linkActivated.connect(self.openURL)
		self.closeBtn.clicked.connect(self.close)
		self.githubBtn.clicked.connect(self.openGithub)
		self.donateBtn.clicked.connect(self.openDonate)

	def openURL(self, url):
		webbrowser.open(url)

	def openGithub(self):
		webbrowser.open("https://github.com/AyraHikari/PyAnimeIndo")

	def openDonate(self):
		webbrowser.open("https://ko-fi.com/ayrahikari")


class Settings(QDialog, Ui_Settings):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		settings = loadSettings()
		if settings.get("mpv_path"):
			self.mpvCustomPath.setText(settings['mpv_path'])

		self.testMPV.clicked.connect(self.testVideoPlayer)
		self.mpvBrowse.clicked.connect(self.browseMPV)
		self.saveConfig.clicked.connect(self.saveSettings)

	def testVideoPlayer(self):
		mpvPath = "mpv"
		if self.mpvCustomPath.text() != "":
			mpvPath = self.mpvCustomPath.text()
		print(mpvPath)

		try:
			process = subp.Popen([mpvPath, '-V'], stdout=subp.PIPE, stderr=subp.PIPE)
			out, err = process.communicate()
		except FileNotFoundError:
			out, err = ("", "FileNotFoundError")
		except OSError:
			out, err = ("", "File tidak valid!")

		alert = QMessageBox()
		if out and not err:
			outp = "MPV ini valid!"
			outp += "\n\n" + out.decode('utf-8')
			alert.setText(outp)
		elif err == "FileNotFoundError":
			alert.setText("MPV tidak ditemukan!\nKalian bisa install MPV atau atur path kustom MPV diatas")
		else:
			alert.setText("MPV ditemukan, tapi gagal!\n\n" + str(err))
		alert.exec()

	def browseMPV(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			self.mpvCustomPath.setText(fileName)

	def saveSettings(self):
		data = {}
		if self.mpvCustomPath.text() != "":
			data['mpv_path'] = self.mpvCustomPath.text()
		isok = saveSettings(data)
		alert = QMessageBox()
		if isok:
			alert.setText("Data tersimpan!")
		alert.exec()
		self.close()


def loadSettings():
	data = {}
	try:
		r = open("config.ini", "r")
		for l in r.read().split("\n"):
			if "=" in l:
				data[l.split("=")[0]] = l.split("=")[1]
	except FileNotFoundError:
		pass
	return data

def saveSettings(data):
	cfile = ""
	for l in data:
		cfile += "{}={}\n".format(l, data[l])
	w = open("config.ini", "w")
	w.write(cfile)
	w.close
	return True

def checkMpvWorking():
	mpvPath = "mpv"

	settings = loadSettings()
	if settings.get("mpv_path"):
		mpvPath = settings['mpv_path']
	print(mpvPath)

	try:
		process = subp.Popen([mpvPath, '-V'], stdout=subp.PIPE, stderr=subp.PIPE)
		out, err = process.communicate()
	except FileNotFoundError:
		out, err = ("", "FileNotFoundError")
	except OSError:
		out, err = ("", "File tidak valid!")

	alert = QMessageBox()
	if out and not err:
		return 1, out.decode('utf-8')
	elif err == "FileNotFoundError":
		return 0, "MPV tidak ditemukan!\nKalian bisa install MPV atau atur path kustom MPV diatas"
	else:
		return 0, "MPV ditemukan, tapi gagal!\n\n" + str(err)

def printd(text):
	if DEBUG:
		print(text)


if __name__ == "__main__":
	DEBUG = True

	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec())