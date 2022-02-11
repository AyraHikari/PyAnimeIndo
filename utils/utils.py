from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from PyQt5.QtGui import QImage, QPixmap, QIcon, QPainter, QColor


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

def make_rounded_res(pic):
	im = Image.open(pic)
	im = add_corners(im, int(im.size[0]/2))
	return pil2pixmap(im)

def write_eps_cover(img, eps):
	draw = ImageDraw.Draw(img)
	w, h = img.size
	font = ImageFont.truetype("img/Roboto.ttf", 16)
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