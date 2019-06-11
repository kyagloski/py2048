
#2048 - Automator

from pynput.keyboard import Key, Controller
from collections import OrderedDict
import time
import random
import webbrowser
import gtk.gdk
import sys

'''
STATE
'''
#keyboard
kb = Controller()

#list of all possible moves
keylst = [Key.left, Key.right, Key.up, Key.down]

#list of optimal moves
optkeylst = [Key.left, Key.down]

#dictionary of all observable coords
#  key=1/16square : value=(x, y)coordinate
# intended use 1280x720 resolution
coordsdict = OrderedDict()

coordsdict["topCornerLeft"] = [480, 180]
coordsdict["topMidLeft"] = [595, 180]
coordsdict["topMidRight"] = [700, 180]
coordsdict["topCornerRight"] = [810, 180]
coordsdict["upCornerLeft"] = [480, 285]
coordsdict["upMidLeft"] = [595, 285]
coordsdict["upMidRight"] = [700, 285]
coordsdict["upCornerRight"] = [810, 285]
coordsdict["lowCornerLeft"] = [480, 400]
coordsdict["lowMidleft"] = [595, 400]
coordsdict["lowMidRight"] = [700, 400]
coordsdict["lowCornerRight"] = [810, 400]
coordsdict["bottomCornerleft"] = [480, 510]
coordsdict["bottomMidLeft"] = [595, 510]
coordsdict["bottomMidRight"] = [700, 510]
coordsdict["bottomCornerRight"] = [810, 510]

#dicitonary of all colors of different square values
#  key=numbervalue : value=RGBvalueofcolor
colorsdict = {195:"0",
              230:"2",
	      	  226:"4",
	      	  191:"8",
	      	  173:"16",
			  158:"32",
			  136:"64",
			  207:"128",
			  203:"256",
			  199:"512",
			  197:"1024",
			  193:"2048",
			  60:"4096",
			  60:"8192"}

'''
CORE FUNCTIONALITY
'''
#prints out formatted color value of each square
def coordsColorPrintOut():
	for i in coordsdict:
		print("______________________________________________\n")
		print(i)
		print("Greyscale Value : ")
		print(pixelAt(coordsdict.get(i)[0], coordsdict.get(i)[1]))	

#presses key
def pressKey(key):
	kb.press(key)
	kb.release(key)

#adds current board greyscale values 
def coordsColorMatrix():
	colorcords = []
	idx = 0
	for i in range(0, 4):
		inner = []
		for j in range(0, 4):
			inner.append(pixelAt(coordsdict.get(coordsdict.keys()[idx])[0], coordsdict.get(coordsdict.keys()[idx])[1]))
			idx += 1
		colorcords.append(inner)
	return colorcords

#ASCII GUI to view what is happening
# on the board as text output
def ptuiPrintOut():
	ca = coordsColorMatrix()
	idx = 0
	for r in range(0, 4):
		for c in range(0, 4):
			print(colorsdict.get(ca[r][c])),
			idx += 1
		print("")
	print("")

#gets pixel at coordinate 
# returns array of r, g, b color values 
# converted to grayscale
#   0.3r +  0.6g +  0.1b = grey 
def pixelAt(x, y):
	w = gtk.gdk.get_default_root_window()
	sz = w.get_size()
	pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
	pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
	pixel_array = pb.get_pixels_array()
	rgb = pixel_array[y][x]	
	grey = (0.3 * rgb[0]) + (0.6 * rgb[1]) + (0.1 * rgb[2])
	return round(grey)

#presses keys ctrl + w to close the tab of the browser
def killBrowser():
	kb.press(Key.ctrl)
	kb.press('w')
	kb.release(Key.ctrl)
	kb.release('w')

'''
SOLVING ALGORITHMS
'''

def checkForwards(matrix):
	mergableNum = 0
	mergableTiles = []
	for row in range(0, 3):
		for col in range(0, 3):
			elem = matrix[row][col]
			try:
				#forwards
				if elem == matrix[row][col+1] and matrix[row][col+1] != 195.0:
					mergableTiles.append(matrix[row][col+1])
					mergableNum += 1
				elif matrix[row][col+1] == 195.0:
					if elem == matrix[row][col+2] and matrix[row][col+2] != 195.0:
						mergableTiles.append(matrix[row][col+2])
						mergableNum += 1
					elif matrix[row][col+2] == 195.0:
						if elem == matrix[row][col+3] and matrix[row][col+3] != 195.0:
							mergableTiles.append(matrix[row][col+3])
							mergableNum += 1
						else:
							print(elem)
					else:
						print(elem)
				else:
					print(elem)
			except:
				print(elem, "1")
	return mergableNum, mergableTiles

def checkBackwards(matrix):
	mergableNum = 0
	mergableTiles = []
	for row in range(0, 3):
		for col in range(0, 3):
			elem = matrix[row][col]
			try:
				#backwards
				if elem == matrix[row][col-1] and matrix[row][col-1] != 195.0:
					mergableTiles.append(matrix[row][col-1])
					mergableNum += 1
				elif matrix[row][col-1] == 195.0:
					if elem == matrix[row][col-2] and matrix[row][col-2] != 195.0:
						mergableTiles.append(matrix[row][col-2])
						mergableNum += 1
					elif matrix[row][col-2] == 195.0:
						if elem == matrix[row][col-3] and matrix[row][col-3] != 195.0:
							mergableTiles.append(matrix[row][col-3])
							mergableNum += 1
						else:
							print(elem)
					else:
						print(elem)
				else:
					print(elem)
			except:
				print(elem, "2")
	return mergableNum, mergableTiles

def checkUpwards(matrix):
	mergableNum = 0
	mergableTiles = []
	for row in range(0, 3):
		for col in range(0, 3):
			elem = matrix[row][col]
			try:
				#upwards
				if elem == matrix[row+1][col] and matrix[row+1][col] != 195.0:
					mergableTiles.append(matrix[row+1][col])
					mergableNum += 1
				elif matrix[row+1][col] == 195.0:
					if elem == matrix[row+2][col] and matrix[row+2][col] != 195.0:
						mergableTiles.append(matrix[row+2][col])
						mergableNum += 1
					elif matrix[row+2][col] == 195.0:
						if elem == matrix[row+3][col] and matrix[row+3][col] != 195.0:
							mergableTiles.append(matrix[row+3][col])
							mergableNum += 1
						else:
							print(elem)
					else:
						print(elem)
				else:
					print(elem)
			except:
				print(elem, "3")
	return mergableNum, mergableTiles

def checkDownwards(matrix):
	mergableNum = 0
	mergableTiles = []
	for row in range(0, 3):
		for col in range(0, 3):
			elem = matrix[row][col]
			try:
				#downwards
				if elem == matrix[row-1][col] and matrix[row-1][col] != 195.0:
					mergableTiles.append(matrix[row-1][col])
					mergableNum += 1
				elif matrix[row]-1[col] == 195.0:
					if elem == matrix[row-2][col] and matrix[row-2][col] != 195.0:
						mergableTiles.append(matrix[row-2][col])
						mergableNum += 1
					elif matrix[row-2][col] == 195.0:
						if elem == matrix[row-3][col] and matrix[row-3][col] != 195.0:
							mergableTiles.append(matrix[row-3][col])
							mergableNum += 1
						else:
							print(elem)
					else:
						print(elem)
				else:
					print(elem)
			except:
				print(elem, "4")
	return mergableNum, mergableTiles

def mergableTiles(matrix):
	mergableNum, mergableTiles = checkForwards(matrix)
	'''
	mergableNum, mergableTiles += checkBackwards(matrix)
	mergableNum, mergableTiles += checkUpwards(matrix)
	mergableNum, mergableTiles += checkDownwards(matrix)
	'''
	print( mergableNum, mergableTiles )		

def isGameOver():
	return False
	
def gamePlay():
	print("Game Starting ... ")
	while True:
		return False
	
'''
TEST FUNCTIONS
'''
#presses random keys from the full key set array
def randomFullMoveSet():
	time.sleep(5)
	for i in range(0, 1000):
		time.sleep(0.15)
		idx = random.randint(0,1)
		pressKey(optkeylst[idx])

#presses random keys from the optimal key set array,
# also added extra functionality for a more optimal algorithm
def randomOptimalMoveSet():
	breakTime = 0.05
	runTime = 5
	time.sleep(1)
	for i in range(0, runTime):
		time.sleep(breakTime)
		pressKey(Key.up)
		time.sleep(breakTime)
		pressKey(Key.down)
		ptuiPrintOut()
		for i in range(0, 15):
			time.sleep(breakTime)
			idx = random.randint(0,1)
			pressKey(optkeylst[idx])
			ptuiPrintOut()

'''
MAIN
'''
def main():
	url = "http://2048game.com/"
	wb = webbrowser.get("google-chrome")
	wb.open(url, 1, True)

	kb.press(Key.f11)
	kb.release(Key.f11)
	
	time.sleep(1.5)
	ptuiPrintOut()
	ma = coordsColorMatrix()
	mergableTiles(ma)
		
	'''
	TESTING BELOW
	'''

	#pixelAt(coordsdict.get("topCornerLeft")[0], coordsdict.get("topCornerLeft")[1])

	#randomOptimalMoveSet()
	#killBrowser()
	
main()

