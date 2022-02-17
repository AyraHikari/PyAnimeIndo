import sys, time, requests, threading, webbrowser, os
import subprocess as subp
from platform import python_version
from multiprocessing.pool import ThreadPool

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import (
	QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt, QFile, QObject, QThread, pyqtSignal
from PyQt5.uic import loadUi

from AnimeListWidget import Ui_AnimeIndo
from AnimeInfoWidget import Ui_Dialog as Ui_AnimeInfo
from About import Ui_Dialog as Ui_About
from Settings import Ui_Dialog as Ui_Settings
from Streaming import Ui_Form as Ui_Streaming

from API.animeindo import get_main, get_episodes, get_download, searchAnime, downloadAnime4K, writeLowA4K, writeHighA4K, uninstallA4kdir
from API.zdl import zdl
from utils.database import loadSettings, saveSettings, saveDataAnime, getSavedAnime, getSavedAnimeList, deleteDataAnime, saveHistoryAnime
from utils.opendialog import OpenDialogApp
from utils.utils import remove_first_end_spaces, make_rounded, make_rounded_res, svg_color, checkMpvWorking, isWindows

DEBUG = False


class MainWindow(QMainWindow, Ui_AnimeIndo):
	dataLatest = {}

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)


		animated_spinner = QtGui.QMovie(":/images/img/ripple.gif")
		self.loadingAnim.setMovie(animated_spinner)
		animated_spinner.start()

		self.AnimeList.verticalScrollBar().setSingleStep(30)
		self.historyAnimeList.verticalScrollBar().setSingleStep(30)
		self.savedAnimeList.verticalScrollBar().setSingleStep(30)

		t = threading.Thread(target=self.getLatest)
		t.start()
		self.AnimeList.doubleClicked.connect(lambda: self.info(self.AnimeList))
		self.historyAnimeList.doubleClicked.connect(lambda: self.info(self.historyAnimeList))
		self.savedAnimeList.doubleClicked.connect(lambda: self.info(self.savedAnimeList))
		
		# Menu bar
		self.latestBtn.clicked.connect(self.latestBtnAct)
		self.jadwalBtn.clicked.connect(self.jadwalBtnAct)
		self.historyBtn.clicked.connect(self.historyBtnAct)
		self.savedBtn.clicked.connect(self.savedBtnAct)
		self.settingsBtn.clicked.connect(self.settings)

		# Others
		self.searchBar.editingFinished.connect(lambda: self.search(self.searchBar, self.AnimeList))

		stream = QFile(":/images/ayra.jpg")
		if stream.open(QFile.ReadOnly):
			profilePic = stream.readAll()
			stream.close()
			self.profilePic.setPixmap(make_rounded_res(profilePic, is_bytes=True))
		#self.settingsIcon.setPixmap(svg_color("C:/Users/tedyr/Documents/Workspace/Python/PyAnimeIndo/UI/img/gear.svg", color='#3F51B5'))

	def disableMenuBg(self):
		self.latestActive.setStyleSheet("background-color: #00000000;border-radius: 12px;")
		self.jadwalActive.setStyleSheet("background-color: #00000000;border-radius: 12px;")
		self.historyActive.setStyleSheet("background-color: #00000000;border-radius: 12px;")
		self.savedActive.setStyleSheet("background-color: #00000000;border-radius: 12px;")

	def latestBtnAct(self):
		#self.loadingAnim.setHidden(False)
		self.disableMenuBg()
		self.latestActive.setStyleSheet("background-color: #D2E5F4;border-radius: 12px;")
		self.tabWidget.setCurrentIndex(0)

	def jadwalBtnAct(self):
		#self.loadingAnim.setHidden(False)
		self.disableMenuBg()
		self.jadwalActive.setStyleSheet("background-color: #D2E5F4;border-radius: 12px;")
		self.tabWidget.setCurrentIndex(1)

	def historyBtnAct(self):
		#self.loadingAnim.setHidden(False)
		self.disableMenuBg()
		self.historyActive.setStyleSheet("background-color: #D2E5F4;border-radius: 12px;")
		self.tabWidget.setCurrentIndex(2)

	def savedBtnAct(self):
		self.loadingAnim.setHidden(False)
		self.disableMenuBg()
		self.savedActive.setStyleSheet("background-color: #D2E5F4;border-radius: 12px;")
		self.tabWidget.setCurrentIndex(3)

		t = threading.Thread(target=self.savedBtnThread)
		t.start()

	def savedBtnThread(self):
		self.savedAnimeList.clear()
		d = getSavedAnimeList()
		[d.pop("eps") for d in d if 'eps' in d]
		results = ThreadPool(16).map(self.addThumbMultiThread, d)
		for r in results:
			self.savedAnimeList.addItem(r)
		self.loadingAnim.setHidden(True)


	def getLatest(self):
		self.AnimeList.clear()
		ongoing = get_main()
		results = ThreadPool(16).map(self.addThumbMultiThread, ongoing)
		self.loadingAnim.setHidden(True)
		for r in results:
			self.AnimeList.addItem(r)
		#for data in ongoing:
			#self.addThumbThread(data)
			#t = threading.Thread(target=self.addThumbThread, args=(data,))
			#t.start()

	def addThumbThread(self, data, is_search=False):
		anime = QtWidgets.QListWidgetItem()
		anime.setText(data['title'])
		imageData = make_rounded(requests.get(data['img']).content)
		anime.setIcon(QtGui.QIcon(imageData))
		anime.setStatusTip(data['url'])
		font = QtGui.QFont()
		font.setFamily("Segoe UI")
		anime.setFont(font)
		if is_search:
			self.AnimeList_Search.addItem(anime)
		else:
			self.AnimeList.addItem(anime)

	def addThumbMultiThread(self, data):
		anime = QtWidgets.QListWidgetItem()
		anime.setText(data['title'])
		imageData = make_rounded(requests.get(data['img']).content, eps=data['eps'] if data.get('eps') else None)
		anime.setIcon(QtGui.QIcon(imageData))
		anime.setStatusTip(data['url'])
		anime.setWhatsThis(str(data))
		font = QtGui.QFont()
		font.setFamily("Segoe UI")
		anime.setFont(font)
		return anime
		

	def info(self, signalType):
		d = signalType.currentItem().statusTip()
		strd = signalType.currentItem().whatsThis()
		dialog = AnimeInfo(self)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.show()
		t = threading.Thread(target=dialog.loadURL, args=(d,strd,))
		t.start()

	def infoS(self):
		d = self.AnimeList_Search.currentItem().statusTip()
		strd = self.AnimeList.currentItem().whatsThis()
		dialog = AnimeInfo(self)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.show()
		t = threading.Thread(target=dialog.loadURL, args=(d,strd,))
		t.start()

	def search(self, signalType, listData):
		title = signalType.text()

		t = threading.Thread(target=self.searchThread, args=(title,listData,))
		t.start()

	def searchThread(self, title, listData):
		listData.clear()
		lists = searchAnime(title)
		results = ThreadPool(16).map(self.addThumbMultiThread, lists)
		for r in results:
			listData.addItem(r)

	def about(self):
		dialog = About(self)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.show()

	def settings(self):
		dialog = Settings(self)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.show()


class AnimeInfo(QDialog, Ui_AnimeInfo):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.AnimeEps.itemClicked.connect(self.getQuality)
		self.StreamingBtn.clicked.connect(self.doStreaming)
		self.DownloadBtn.clicked.connect(self.doDownload)

		self.firstQuality.clicked.connect(self.checkDownload1)
		self.secondQuality.clicked.connect(self.checkDownload2)
		self.thirdQuality.clicked.connect(self.checkDownload3)
		self.fourthQuality.clicked.connect(self.checkDownload4)

		self.recommendList.doubleClicked.connect(self.reInfo)
		self.saveThis.clicked.connect(self.saveAnime)

	def loadURL(self, urlData, strdata=None):
		# Get Anime
		printd("Fetching: " + urlData)
		data = get_episodes(urlData)

		image = QtGui.QPixmap()
		imageData = make_rounded(requests.get(data['cover']).content)
		dataTitle = remove_first_end_spaces(data['title'].lower().replace("subtitle indonesia", "").title())
		self.AnimeTitle.setText(dataTitle)
		self.AnimeCover.setPixmap(imageData)
		self.AnimeSinopsis.setText(data['sinopsis'] if data['sinopsis'] else "Tidak ada...")

		if strdata:
			if urlData in getSavedAnime():
				self.saveThis.setIcon(QtGui.QIcon(":/icons/img/bookmark.svg"))
				self.saveThis.setStyleSheet("padding: 12px 8px;\nposition: absolute;\nborder: 1px solid rgba(45, 45, 45, 0.8);\nborder-radius: 4px;\ncolor: #000;\nbackground: #fff;")
			else:
				self.saveThis.setIcon(QtGui.QIcon(":/icons/img/bookmark_outline.svg"))
				self.saveThis.setStyleSheet("padding: 12px 8px;\nposition: absolute;\nborder: 1px solid rgba(45, 45, 45, 0.3);\nborder-radius: 4px;\ncolor: #000;\nbackground: #fff;")
			self.saveThis.setStatusTip(str(strdata))

		# Get anime info
		skor = 4
		for infoData in data['info'].split("\n"):
			if "studio" in infoData.lower():
				self.infoStudio.setText(remove_first_end_spaces(infoData.split(":")[1]))
			if "genre" in infoData.lower():
				self.infoGenre.setText(remove_first_end_spaces(infoData.split(":")[1]))
			if "status" in infoData.lower():
				self.infoStatus.setText(remove_first_end_spaces(infoData.split(":")[1]))
			if "durasi" in infoData.lower():
				self.infoType.setText(remove_first_end_spaces(infoData.split(":")[1]))
			if "skor" in infoData.lower():
				val = remove_first_end_spaces(infoData.split(":")[1])
				if val:
					skor = int(float(val)/2)
					if skor >= 1:
						self.star1.setStyleSheet("width: 30px;\nheight: 30px;\nleft: 318px;\ntop: 132px;\nborder-radius: 2px;\nborder-image: url(:/icons/img/star_on.svg);")
					if skor >= 2:
						self.star2.setStyleSheet("width: 30px;\nheight: 30px;\nleft: 318px;\ntop: 132px;\nborder-radius: 2px;\nborder-image: url(:/icons/img/star_on.svg);")
					if skor >= 3:
						self.star3.setStyleSheet("width: 30px;\nheight: 30px;\nleft: 318px;\ntop: 132px;\nborder-radius: 2px;\nborder-image: url(:/icons/img/star_on.svg);")
					if skor >= 4:
						self.star4.setStyleSheet("width: 30px;\nheight: 30px;\nleft: 318px;\ntop: 132px;\nborder-radius: 2px;\nborder-image: url(:/icons/img/star_on.svg);")
					if skor >= 5:
						self.star5.setStyleSheet("width: 30px;\nheight: 30px;\nleft: 318px;\ntop: 132px;\nborder-radius: 2px;\nborder-image: url(:/icons/img/star_on.svg);")

		self.setWindowTitle(remove_first_end_spaces(data['info'].lower().split("judul:")[1].split("\n")[0]).title())

		# Parse episodes
		self.AnimeEps.clear()
		totalEps = "0"
		for item in data['episodes']:
			eps_title = item['title'].lower().replace("subtitle indonesia", "")
			if data['info']:
				eps_title = eps_title.replace(remove_first_end_spaces(data['info'].lower().split("judul:")[1].split("\n")[0]), "")
			eps_title = remove_first_end_spaces(eps_title.replace(dataTitle.lower(), "")).title()

			if totalEps == "0":
				if x := [x for x in eps_title.split() if x.isdigit()]:
					totalEps = remove_first_end_spaces(x[0])

			eps = QtWidgets.QListWidgetItem()
			eps.setText(eps_title)
			eps.setStatusTip(item['url'])
			self.AnimeEps.addItem(eps)

		if totalEps:
			self.totalEpisode.setText(f"1 - {totalEps} Episodes")

		self.recommendList.clear()
		results = ThreadPool(5).map(self.setRecommendedList, data['recommend'])
		for r in results:
			self.recommendList.addItem(r)

		self.AnimeEps.setEnabled(True)

	def setRecommendedList(self, item):
		eps = QtWidgets.QListWidgetItem()
		aniTitle = item['title']
		if len(aniTitle) >= 11:
			aniTitle = aniTitle[:12] + "..."
		eps.setText(aniTitle)
		eps.setStatusTip(item['url'])
		imageData = make_rounded(requests.get(item['cover']).content)
		eps.setIcon(QtGui.QIcon(imageData))
		return eps

	def reInfo(self):
		d = self.recommendList.currentItem().statusTip()
		self.close()
		dialog = AnimeInfo(self)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.show()
		t = threading.Thread(target=dialog.loadURL, args=(d,))
		t.start()

	def getQuality(self, data):
		t = threading.Thread(target=self.getQualityThread, args=(data,))
		t.start()

	def checkDownload1(self):
		if self.firstQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.greyAllQ()
			self.firstQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")

		if "zippyshare" in self.firstQuality.statusTip():
			self.StreamingBtn.setEnabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #E84545;border-radius: 4px;color: #FFFFFF;")
		else:
			self.StreamingBtn.setDisabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #2D2D2D;border-radius: 4px;color: #FFFFFF;")
	
	def checkDownload2(self):
		if self.secondQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.greyAllQ()
			self.secondQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")

		if "zippyshare" in self.secondQuality.statusTip():
			self.StreamingBtn.setEnabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #E84545;border-radius: 4px;color: #FFFFFF;")
		else:
			self.StreamingBtn.setDisabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #2D2D2D;border-radius: 4px;color: #FFFFFF;")
		
	def checkDownload3(self):
		if self.thirdQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.greyAllQ()
			self.thirdQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")

		if "zippyshare" in self.thirdQuality.statusTip():
			self.StreamingBtn.setEnabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #E84545;border-radius: 4px;color: #FFFFFF;")
		else:
			self.StreamingBtn.setDisabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #2D2D2D;border-radius: 4px;color: #FFFFFF;")
	
	def checkDownload4(self):
		if self.fourthQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.greyAllQ()
			self.fourthQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")

		if "zippyshare" in self.fourthQuality.statusTip():
			self.StreamingBtn.setEnabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #E84545;border-radius: 4px;color: #FFFFFF;")
		else:
			self.StreamingBtn.setDisabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #2D2D2D;border-radius: 4px;color: #FFFFFF;")

	
	def greyAllQ(self):
		if self.firstQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.firstQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")
		if self.secondQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.secondQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")
		if self.thirdQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.thirdQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")
		if self.fourthQuality.styleSheet().split("background: ")[1].split(";")[0] != "#FFF":
			self.fourthQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")

	def getQualityThread(self, data):
		self.disabledAll()
		targeturl = data.statusTip()
		printd("Fetching: " + targeturl)
		webdata = get_download(targeturl)

		# Parse quality
		isFirst = False
		for item in webdata:
			if "360p" in item:
				self.firstQuality.setStatusTip(webdata[item])
				if not isFirst:
					self.firstQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")
					isFirst = True
				else:
					self.firstQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")
			elif "480p" in item:
				self.secondQuality.setStatusTip(webdata[item])
				if not isFirst:
					self.secondQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")
					isFirst = True
				else:
					self.secondQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")
			elif "720p" in item:
				self.thirdQuality.setStatusTip(webdata[item])
				if not isFirst:
					self.thirdQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")
					isFirst = True
				else:
					self.thirdQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")
			elif "1080p" in item:
				self.fourthQuality.setStatusTip(webdata[item])
				if not isFirst:
					self.fourthQuality.setStyleSheet("position: absolute;background: #2D2D2D;border-radius: 8px;text-align: center;color: #fff;")
					isFirst = True
				else:
					self.fourthQuality.setStyleSheet("position: absolute;background: #F4F4F4;border-radius: 8px;text-align: center;color: #333;")

		if "zippyshare" in self.firstQuality.statusTip():
			self.StreamingBtn.setEnabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #E84545;border-radius: 4px;color: #FFFFFF;")
		else:
			self.StreamingBtn.setDisabled(True)
			self.StreamingBtn.setStyleSheet("padding: 12px 8px;position: absolute;background: #2D2D2D;border-radius: 4px;color: #FFFFFF;")

		self.DownloadBtn.setEnabled(True)
		self.DownloadBtn.setStyleSheet("padding: 12px 8px;position: absolute;border: 1px solid rgba(45, 45, 45, 0.6);border-radius: 4px;color: #000;background: #fff;")
		self.enabledAll()

	def getDownload(self, data):
		targeturl = self.AnimeQuality.currentItem().statusTip()
		self.DownloadBtn.setEnabled(True)
		if "zippyshare" in targeturl:
			self.StreamingBtn.setEnabled(True)
		else:
			self.StreamingBtn.setEnabled(False)
		self.downloadURL.setPlainText(targeturl)

	def doStreaming(self):
		self.disabledAll()
		iswork, comment = checkMpvWorking()
		if not iswork:
			alert = QMessageBox()
			alert.setText(comment)
			alert.exec()
			dialog = Settings(self)
			dialog.setWindowModality(Qt.ApplicationModal)
			dialog.show()
			self.enabledAll()
			return
		targeturl = self.getAnimeQuality()
		dialog = Streaming(self)
		dialog.setWindowModality(Qt.ApplicationModal)
		dialog.setWindowFlag(Qt.WindowCloseButtonHint, False)
		dialog.show()
		printd("Fetching: " + targeturl)
		try:
			zdirect = zdl(targeturl)
			t = threading.Thread(target=self.start_mpv, name="MPV Player", args=(zdirect,dialog,))
			t.start()
		except Exception as err:
			alert = QMessageBox()
			alert.setWindowTitle("Peringatan")
			if str(err) == "Failed to get file URL. Down?":
				alert.setText("Link rusak, tolong pilih resolusi lainnya")
			alert.exec()
			dialog.close()
			self.enabledAll()

	def doDownload(self, data):
		targeturl = self.getAnimeQuality()
		printd("Open: " + targeturl)
		webbrowser.open(targeturl)

	def getAnimeQuality(self):
		targeturl = ""
		if self.firstQuality.styleSheet().split("background: ")[1].split(";")[0] == "#2D2D2D":
			targeturl = self.firstQuality.statusTip()
		if self.secondQuality.styleSheet().split("background: ")[1].split(";")[0] == "#2D2D2D":
			targeturl = self.secondQuality.statusTip()
		if self.thirdQuality.styleSheet().split("background: ")[1].split(";")[0] == "#2D2D2D":
			targeturl = self.thirdQuality.statusTip()
		if self.fourthQuality.styleSheet().split("background: ")[1].split(";")[0] == "#2D2D2D":
			targeturl = self.fourthQuality.statusTip()
		return targeturl

	def disabledAll(self):
		self.AnimeEps.setDisabled(True)
		self.firstQuality.setDisabled(True)
		self.secondQuality.setDisabled(True)
		self.thirdQuality.setDisabled(True)
		self.fourthQuality.setDisabled(True)
		self.DownloadBtn.setDisabled(True)
		self.StreamingBtn.setDisabled(True)

	def enabledAll(self):
		self.AnimeEps.setEnabled(True)
		self.firstQuality.setEnabled(True)
		self.secondQuality.setEnabled(True)
		self.thirdQuality.setEnabled(True)
		self.fourthQuality.setEnabled(True)
		self.DownloadBtn.setEnabled(True)
		self.StreamingBtn.setEnabled(True)

	def saveAnime(self):
		d = self.saveThis.statusTip()
		if not d:
			return

		if eval(d)['url'] in getSavedAnime():
			deleteDataAnime(eval(d)['url'])
			self.saveThis.setIcon(QtGui.QIcon(":/icons/img/bookmark_outline.svg"))
			self.saveThis.setStyleSheet("padding: 12px 8px;\nposition: absolute;\nborder: 1px solid rgba(45, 45, 45, 0.3);\nborder-radius: 4px;\ncolor: #000;\nbackground: #fff;")
		else:
			saveDataAnime(eval(d)['url'], d)
			self.saveThis.setIcon(QtGui.QIcon(":/icons/img/bookmark.svg"))
			self.saveThis.setStyleSheet("padding: 12px 8px;\nposition: absolute;\nborder: 1px solid rgba(45, 45, 45, 0.8);\nborder-radius: 4px;\ncolor: #000;\nbackground: #fff;")


	def start_mpv(self, url, dialog):
		mpv_cmd = "mpv"
		settings = loadSettings()
		if settings.get("mpv_path"):
			mpv_cmd = settings['mpv_path']

		p = subp.Popen("\"" + mpv_cmd + "\" -V " + url, shell=True)
		while p.poll() is None:
			time.sleep(1)

		dialog.close()
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

		if settings.get("http_proxy"):
			self.HttpProxy.setText(settings['http_proxy'])
		if settings.get("https_proxy"):
			self.HttpsProxy.setText(settings['https_proxy'])

		self.testMPV.clicked.connect(self.testVideoPlayer)
		self.ProxyTest.clicked.connect(self.testProxy)
		self.mpvBrowse.clicked.connect(self.browseMPV)
		self.saveConfig.clicked.connect(self.saveSettings)
		self.exitBtn.clicked.connect(self.close)

		self.installA4k1.clicked.connect(lambda: self.InstallA4K(1))
		self.installA4k2.clicked.connect(lambda: self.InstallA4K(2))
		self.uninstallA4k.clicked.connect(self.UninstallA4K)

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

	def testProxy(self):
		settings = loadSettings()
		if http_proxy := settings.get('http_proxy'):
			os.environ['http_proxy'] = http_proxy
		if https_proxy := settings.get('https_proxy'):
			os.environ['https_proxy'] = https_proxy
		if isWindows():
			process = subp.Popen(["ping", 'google.com', '-n', '1'], stdout=subp.PIPE, stderr=subp.PIPE)
		else:
			process = subp.Popen(["ping", 'google.com', '-c', '1'], stdout=subp.PIPE, stderr=subp.PIPE)
		out, err = process.communicate()

		try:
			if isWindows():
				retms = out.decode('utf-8').split(" time=")[1].split(" ")[0]
			else:
				retms = out.decode('utf-8').split(" time=")[1].split("\n")[0]
		except IndexError:
			retms = "RTO"
		self.retms.setText(retms)

	def InstallA4K(self, value):
		t = threading.Thread(target=self.downloada4k, args=(value,))
		t.start()

	def downloada4k(self, value):
		self.installA4k1.setDisabled(True)
		self.installA4k2.setDisabled(True)
		self.uninstallA4k.setDisabled(True)
		downloadAnime4K()
		if value == 1:
			writeHighA4K()
		else:
			writeLowA4K()
		self.installA4k1.setEnabled(True)
		self.installA4k2.setEnabled(True)
		self.uninstallA4k.setEnabled(True)


	def UninstallA4K(self):
		self.installA4k1.setDisabled(True)
		self.installA4k2.setDisabled(True)
		self.uninstallA4k.setDisabled(True)
		uninstallA4kdir()
		self.installA4k1.setEnabled(True)
		self.installA4k2.setEnabled(True)
		self.uninstallA4k.setEnabled(True)
		print("Uninstalled!")

	def saveSettings(self):
		data = {}

		# Path
		if self.mpvCustomPath.text() != "":
			data['mpv_path'] = self.mpvCustomPath.text()

		# Proxy
		#if self.mpvCustomPath.text() != "":
		#	data['http_proxy'] = self.HttpProxy.text()
		#	data['https_proxy'] = self.HttpsProxy.text()

		isok = saveSettings(data)
		alert = QMessageBox()
		if isok:
			alert.setText("Data tersimpan!")
		alert.exec()
		self.close()

class Streaming(QDialog, Ui_Streaming):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)





def printd(text):
	if DEBUG:
		print(text)


if __name__ == "__main__":
	DEBUG = True

	app = QApplication(sys.argv)
	win = MainWindow()
	win.show()
	sys.exit(app.exec())