#VERSION 2
from PIL import Image, ImageDraw, ImageFilter
import numpy as np


IMG_PATH = "port.jpg" # Leave blank to be asked to input
GAP = 100
MAX = 2000000
MAX_CHANGE = 5

#spiral constants
a = 1.5
b = -2.4

#inputted ImageDraw, center (numpy array [x,y]), color(greyscale 0-255), radius
def drawDot(imgDraw, center, color, radius):
	(x,y) = center
	imgDraw.ellipse([(x - radius, y - radius), (x + radius), (y + radius)] ,fill=color)

def func(t):
	#constants
	global a, b

	#actual function
	x = (a + b*t) * np.cos(t)
	y = (a + b*t) * np.sin(t)
	#return Point(x,y)
	return np.array([x, y])

#given an arclength solves for a time t
def arcLengthSolver(arclength):
	global a, b
	co = [(b**2)/3, a * b, b**2 + a**2, arclength * -1]
	for value in np.roots(co):
		if np.isreal(value):
			return value.real

def darkVector(point, px, maxWidth = np.inf, maxHeight = np.inf):
	'''returns a weighted average of all the points in an NxN square around it,
	and creates a vector pointing towards the darkest spot'''
	x,y = point
	x = int(x)
	y = int(y)
	
	N = 31 # has to be odd
	MIN = -int(N/2)
	MAX = -MIN + 1

	vectors = []
	weights = []

	for i in range(MIN + x, MAX + x):
		for j in range(MIN + y, MAX + y):
			if (i >= 0 and j >= 0 and i < maxWidth and j < maxHeight):
				vectors.append(np.array([i - x, j - y]))
				weights.append(255/2 - px[i, j])
	
	vectors = np.asarray(vectors)
	weights = np.asarray(weights)

	try:
		return np.average(vectors, axis=0, weights=weights)
	except ZeroDivisionError:
		return np.array([0,0])


def main():
	print("Running")
	global MAX, GAP, IMG_PATH, MAX_CHANGE

	if (IMG_PATH == ""):
		IMG_PATH = input("Path: ")

	# Read in the image
	try:
		raw_img  = Image.open(IMG_PATH, mode='r')
	except IOError:
		print("Image not found")
		exit()


	img = raw_img.convert(mode = 'L') # convert to grayscale image
	img = img.filter(ImageFilter.GaussianBlur(radius=2))
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
	#generate points along our position function ------------------ DOING THIS
	for i in range(0, MAX, GAP): # creates points equidistant from eachother
		point = func(arcLengthSolver(i)) + [img.width/2, img.height/2]
		points.append(point)
		#drawDot(draw, point, 100, 1)


	finalPoints = []
	
	for p in points:
		#break
		darkvector = darkVector(p, pixelData, maxWidth=img.width, maxHeight=img.height)
		#print(darkvector)
		normalized = np.linalg.norm(darkvector)
		if (normalized != 0):
			if (normalized > MAX_CHANGE): # if its above this amount of pixels change then we max it out
				darkvector = (darkvector / normalized) * MAX_CHANGE
			#darkvector = (darkvector / np.linalg.norm(darkvector)) * 100 #fix nan problem
			#print(p, p+darkvector)
			p = p + darkvector

		finalPoints.append(p)

		#drawDot(draw, p, 0, 1)
	
	draw.line([tuple(x) for x in np.asarray(finalPoints)])

	drawImg.show()


if __name__ == "__main__":
	main()