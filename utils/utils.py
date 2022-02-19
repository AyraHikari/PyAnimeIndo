import os
import subprocess as subp
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from PyQt5.QtCore import QFile
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor
from PyQt5.QtWidgets import (
	QMessageBox
)

from .database import loadSettings, saveSettings


def isWindows():
	if os.name == 'nt':
		return True
	return False

def remove_end_spaces(string):
	return "".join(string.rstrip())

# Remove first and  end spaces
def remove_first_end_spaces(string):
	return "".join(string.rstrip().lstrip())

# Remove all spaces
def remove_all_spaces(string):
	return "".join(string.split())

# Remove all extra spaces
def remove_all_extra_spaces(string):
	return " ".join(string.split())

def add_corners(im, rad):
	circle = Image.new('L', (rad * 2, rad * 2), 0)
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
	alpha = Image.new('L', im.size, 255)
	w, h = im.size
	alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
	alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
	alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
	alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
	im.putalpha(alpha)
	return im

def make_rounded(pic, eps=None):
	im = Image.open(BytesIO(pic))
	if eps:
		im = write_eps_cover(im, eps)
	im = add_corners(im, 15)
	return pil2pixmap(im)

def make_rounded_res(pic, is_bytes=False):
	if not is_bytes:
		im = Image.open(pic)
	else:
		im = Image.open(BytesIO(pic))
	im = add_corners(im, int(im.size[0]/2))
	return pil2pixmap(im)

def write_eps_cover(img, eps):
	draw = ImageDraw.Draw(img)
	w, h = img.size

	stream = QFile(":/font/Roboto.ttf")
	if stream.open(QFile.ReadOnly):
		fontData = stream.readAll()
		stream.close()
	font = ImageFont.truetype(BytesIO(fontData), 16)
	text_w, text_h = draw.textsize(eps, font)
	draw.rounded_rectangle((-30, h - h/12-2, text_w +12, h + text_h), 5, fill="#E8EFF5")
	draw.text((5, h - text_h - 5), eps, "black", font=font)
	return img

def pil2pixmap(image):
	bytes_img = BytesIO()
	image.save(bytes_img, format='png')

	qimg = QImage()
	qimg.loadFromData(bytes_img.getvalue())

	return QPixmap.fromImage(qimg)

def svg_color(im, color='black'):
	img = QPixmap(im)
	qp = QPainter(img)
	qp.setCompositionMode(QPainter.CompositionMode_SourceIn)
	qp.fillRect( img.rect(), QColor(color) ) 
	qp.end()
	return img

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

def setPresetMPV(preset):
	preset_data = []
	if preset == "Off":
		preset_data = ["off"]
	elif preset == "Mode A (HQ)":
		preset_data = ["~~/shaders/Anime4K_Clamp_Highlights.glsl", "~~/shaders/Anime4K_Restore_CNN_M.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x2.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x4.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"]
	elif preset == "Mode B (HQ)":
		preset_data = ["~~/shaders/Anime4K_Clamp_Highlights.glsl", "~~/shaders/Anime4K_Restore_CNN_Soft_M.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x2.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x4.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"]
	elif preset == "Mode C (HQ)":
		preset_data = ["~~/shaders/Anime4K_Clamp_Highlights.glsl", "~~/shaders/Anime4K_Upscale_Denoise_CNN_x2_M.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x2.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x4.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"]
	elif preset == "Mode A+A (HQ)":
		preset_data = ["~~/shaders/Anime4K_Clamp_Highlights.glsl", "~~/shaders/Anime4K_Restore_CNN_M.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl", "~~/shaders/Anime4K_Restore_CNN_S.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x2.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x4.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"]
	elif preset == "Mode B+B (HQ)":
		preset_data = ["~~/shaders/Anime4K_Clamp_Highlights.glsl", "~~/shaders/Anime4K_Restore_CNN_Soft_M.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x2.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x4.glsl", "~~/shaders/Anime4K_Restore_CNN_Soft_S.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"]
	elif preset == "Mode C+A (HQ)":
		preset_data = ["~~/shaders/Anime4K_Clamp_Highlights.glsl", "~~/shaders/Anime4K_Upscale_Denoise_CNN_x2_M.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x2.glsl", "~~/shaders/Anime4K_AutoDownscalePre_x4.glsl", "~~/shaders/Anime4K_Restore_CNN_S.glsl", "~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"]

	if preset_data:
		if os.name == "nt":
			r = "C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\mpv.conf"
		else:
			r = f"/{os.getenv('HOME')}/.config/mpv/mpv.conf"
		
		rdata = ""
		try:
			with open(r) as mpv_conf:
				for line in mpv_conf:
					if "glsl-shader" not in line:
						rdata += line
		except FileNotFoundError:
			pass

		if preset_data[0] != "off":
			rdata += '\nglsl-shader="' + '"\nglsl-shader="'.join(preset_data)

		if os.name == "nt":
			w = open(r, "w")
		else:
			w = open(r, "w")
		w.write(rdata)
		w.close()