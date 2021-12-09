
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

#state that determines if game has ended
gameOverCoord = [632, 415]
gameOverColor = 175.0

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

def checkForwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	#print(row, col)
	if col == 3:
		#print("no merge")
		return mergableNum, mergableTiles
	try:
	#forwards
		if elem == matrix[row][col+1] and matrix[row][col+1] != 195.0:
			mergableTiles.append(matrix[row][col+1])
			mergableNum += 1
			#print("merge found f + 1")
			return mergableNum, mergableTiles
		elif matrix[row][col+1] == 195.0:
			if elem == matrix[row][col+2] and matrix[row][col+2] != 195.0:
				mergableTiles.append(matrix[row][col+2])
				mergableNum += 1
				#print("merge found f + 2")
				return mergableNum, mergableTiles
			elif matrix[row][col+2] == 195.0:
				if elem == matrix[row][col+3] and matrix[row][col+3] != 195.0:
					mergableTiles.append(matrix[row][col+3])
					mergableNum += 1
					#print("merge found f + 3")
					return mergableNum, mergableTiles
	except:
		pass
		#print(elem, "forwards idx")
	#print("no merge")
	return mergableNum, mergableTiles

def checkBackwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	#print(row, col)
	if col == 0:
		#print("no merge")
		return mergableNum, mergableTiles
	try:
	#backwards
		if elem == matrix[row][col-1] and matrix[row][col-1] != 195.0:
			mergableTiles.append(matrix[row][col-1])
			mergableNum += 1
			#print("merge found b - 1")
			return mergableNum, mergableTiles
		elif matrix[row][col-1] == 195.0 and col - 2 >= 0:
			if elem == matrix[row][col-2] and matrix[row][col-2] != 195.0:
				mergableTiles.append(matrix[row][col-2])
				mergableNum += 1
				#print("merge found b - 2")
				return mergableNum, mergableTiles
			elif matrix[row][col-2] == 195.0 and col - 3 >= 0:
				if elem == matrix[row][col-3] and matrix[row][col-3] != 195.0:
					mergableTiles.append(matrix[row][col-3])
					mergableNum += 1
					#print("merge found b - 3")
					return mergableNum, mergableTiles
	except:
		pass
		#print(elem, "backwards idx")
	#print("no merge")
	return mergableNum, mergableTiles

def checkUpwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	#print(row, col)
	if row == 0:
		#print("no merge")
		return mergableNum, mergableTiles
	try:
	#upwards
		if elem == matrix[row-1][col] and matrix[row-1][col] != 195.0:
			mergableTiles.append(matrix[row-1][col])
			mergableNum += 1
			#print("merge found u - 1")
			return mergableNum, mergableTiles
		elif matrix[row-1][col] == 195.0 and row - 2 >= 0:
			if elem == matrix[row-2][col] and matrix[row-2][col] != 195.0:
				mergableTiles.append(matrix[row-2][col])
				mergableNum += 1
				#print("merge found u - 2")
				return mergableNum, mergableTiles
			elif matrix[row-2][col] == 195.0 and row - 3 >= 0:
				if elem == matrix[row-3][col] and matrix[row-3][col] != 195.0:
					mergableTiles.append(matrix[row-3][col])
					mergableNum += 1
					#print("merge found u - 3")
					return mergableNum, mergableTiles
	except:
		pass
		#print(elem, "upwards idx")
	#print("no merge")
	return mergableNum, mergableTiles

def checkDownwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	#print(row, col)
	if row == 3:
		#print("no merge")
		return mergableNum, mergableTiles
	try:
	#downwards
		if elem == matrix[row+1][col] and matrix[row+1][col] != 195.0:
			mergableTiles.append(matrix[row+1][col])
			mergableNum += 1
			#print("merge found d + 1")
			return mergableNum, mergableTiles
		elif matrix[row+1][col] == 195.0:
			if elem == matrix[row+2][col] and matrix[row+2][col] != 195.0:
				mergableTiles.append(matrix[row+2][col])
				mergableNum += 1
				#print("merge found d + 2")
				return mergableNum, mergableTiles
			elif matrix[row+2][col] == 195.0:
				if elem == matrix[row+3][col] and matrix[row+3][col] != 195.0:
					mergableTiles.append(matrix[row+3][col])
					mergableNum += 1
					#print("merge found d + 3")
					return mergableNum, mergableTiles
	except:
		pass
		#print(elem, "downwards idx")
	#print("no merge")
	return mergableNum, mergableTiles

def mergableTiles(matrix):
	forwardList = []
	backwardList = []
	upwardList = []
	downwardList = []
	
	forwardMerges = 0
	backwardMerges = 0
	upwardMerges = 0
	downwardMerges = 0
	for col in range(0, 4):
		for row in range(0, 4):
			if matrix[row][col] != 195.0:
				TEMPmergableNum, TEMPmergableTiles = checkForwards(matrix, row, col)
				if TEMPmergableNum != 0:
					forwardMerges += TEMPmergableNum
					forwardList.append(TEMPmergableTiles)
				TEMPmergableNum, TEMPmergableTiles = checkBackwards(matrix, row, col)
				if TEMPmergableNum != 0:
					backwardMerges += TEMPmergableNum
					backwardList.append(TEMPmergableTiles)
				TEMPmergableNum, TEMPmergableTiles = checkUpwards(matrix, row, col)
				if TEMPmergableNum != 0:
					upwardMerges += TEMPmergableNum
					upwardList.append(TEMPmergableTiles)
				TEMPmergableNum, TEMPmergableTiles = checkDownwards(matrix, row, col)
				if TEMPmergableNum != 0:
					downwardMerges += TEMPmergableNum
					downwardList.append(TEMPmergableTiles)
	#print( "forwards : ", forwardMerges)
	#print( "backwards : ", backwardMerges)
	#print( "upwards : ", upMerges)
	#print( "downwards : ", downMerges)
	#print( mergableTiles )
	return forwardList, backwardList, upwardList, downwardList, forwardMerges, backwardMerges, upwardMerges, downwardMerges 


#determines if the game has ended
def isGameOver():
	if pixelAt(gameOverCoord[0], gameOverCoord[1]) == gameOverColor:
		print("GAME OVER!!")
		return True
	return False
	
def gamePlay():
	print("Game Starting ... ")
	while isGameOver == False:
		ma = coordsColorMatrix()
		mergeList = []
		directionList = []
		forwardList, backwardList, upwardList, downwardList, forwardMerges, backwardMerges, upwardMerges, downwardMerges  = mergableTiles(ma)
		mergeList.append(forwardList)
		mergeList.append(backwardList)
		mergeList.append(upwardList)
		mergeList.append(downwardList)
		directionList.append(forwardList)
		directionList.append(backwardList)
		directionList.append(upwardList)
		directionList.append(downwardList)

		mergeAmount = 0
		largestMerge = "0"

		for merge in mergeAmount:
			if merge > mergeAmount:
				mergeAmount = merge

		for lst in mergeList:
			for elem in lst:
				if int(colorsdict.get(elem)) > int(largestMerge):
					largestMerge = colorsdict.get(elem)

		

	
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
	timeerwerwer = 0
	breakTime = 0.0
	runTime = 10000
	time.sleep(1)
	for i in range(0, runTime):
		time.sleep(breakTime)
		pressKey(Key.up)
		time.sleep(breakTime)
		pressKey(Key.down)
		#ptuiPrintOut()
		ma = coordsColorMatrix()
		mergableTiles(ma)
		print("")
		if isGameOver() == True:
			pressKey('r')
			timeerwerwer += 1
			print(timeerwerwer)
		for i in range(0, 15):
			time.sleep(breakTime)
			idx = random.randint(0,1)
			pressKey(optkeylst[idx])
			#ptuiPrintOut()
			ma = coordsColorMatrix()
			mergableTiles(ma)
			print("")
			if isGameOver():
				pressKey('r')
				timeerwerwer += 1
				print(timeerwerwer)

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
	'''
	TESTING BELOW
	'''
	
	randomOptimalMoveSet()
	killBrowser()

if __name__ == '__main__':
	main()
