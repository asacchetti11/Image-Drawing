#VERSION 1
from PIL import Image, ImageDraw, ImageFilter
import numpy as np


IMG_PATH = "port.jpg" # Leave blank to be asked to input
NUM_POINTS = 8000
MAX = 200

#inputted ImageDraw, center (numpy array [x,y]), color(greyscale 0-255), radius
def drawDot(imgDraw, center, color, radius):
	(x,y) = center
	imgDraw.ellipse([(x - radius, y - radius), (x + radius), (y + radius)] ,fill=color)

def func(t):
	#constants
	a = 1.5
	b = -2.4
	c = 1.5
	d = -2.4

	#actual function
	x = (a + b*t) * np.cos(t)
	y = (c + d*t) * np.sin(t)
	#return Point(x,y)
	return np.array([x, y])


def darkVector(point, px, maxWidth = np.inf, maxHeight = np.inf):
	'''returns a weighted average of all the points in an NxN square around it,
	and creates a vector pointing towards the darkest spot'''
	x,y = point
	x = int(x)
	y = int(y)
	
	N = 51 # has to be odd
	MIN = -int(N/2)
	MAX = -MIN + 1

	vectors = []
	weights = []

	for i in range(MIN + x, MAX + x):
		for j in range(MIN + y, MAX + y):
			if (i >= 0 and j >= 0 and i < maxWidth and j < maxHeight):
				vectors.append(np.array([i - x, j - y]))
				weights.append(255 - px[i, j])
	
	vectors = np.asarray(vectors)
	weights = np.asarray(weights)

	try:
		return np.average(vectors, axis=0, weights=weights)
	except ZeroDivisionError:
		return np.array([0,0])


def main():
	print("Running")
	global MAX, NUM_POINTS, IMG_PATH

	if (IMG_PATH == ""):
		IMG_PATH = input("Path: ")

	# Read in the image
	try:
		raw_img  = Image.open(IMG_PATH, mode='r')
	except IOError:
		print("Image not found")
		exit()


	img = raw_img.convert(mode = 'L') # convert to grayscale image
	pixelData = img.load()

	points = []
	drawImg = Image.new('L', img.size, 255)
	# drawImg = img.copy() # testing
	# drawImg.putalpha(50)# testing
	#drawImg = drawImg.convert(mode = 'RGBA')# testing
	draw = ImageDraw.Draw(drawImg)

	'''#testing 
	point = np.array([200, 400])
	darkvector = darkVector(point, pixelData, maxWidth=img.width, maxHeight=img.height)
	#darkvector = (darkvector / np.linalg.norm(darkvector)) * 100
	print(point, darkvector)
	drawDot(draw, point, (0,200,0), 4)
	drawDot(draw, point + darkvector, (255,0,0), 4)
	'''
	#generate points along our position function
	for i in np.linspace(0, MAX, NUM_POINTS): # TODO calculate arclength and create points equidistant
		point = func(i) + [img.width/2, img.height/2]
		points.append(point)
		#drawDot(draw, point, 100, 1)

	#
	for p in points:
		#break
		darkvector = darkVector(p, pixelData, maxWidth=img.width, maxHeight=img.height)
		#print(darkvector)
		normalized = np.linalg.norm(darkvector)
		if (normalized != 0):
			if (normalized > 100): # if its above 10 pixels change then we max it out
				darkvector = (darkvector / normalized) * 100
			#darkvector = (darkvector / np.linalg.norm(darkvector)) * 100 #fix nan problem
			#print(p, p+darkvector)
			p = p + darkvector


		drawDot(draw, p, 0, 1)
	''''''
	drawImg.show()


if __name__ == "__main__":
	main()