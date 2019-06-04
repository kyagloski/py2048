#2048 - Automator

from pynput.keyboard import Key, Controller
import time
import random
import webbrowser
import gtk.gdk
import sys

#keyboard
kb = Controller()

#list of all possible moves
keylst = [Key.left, Key.right, Key.up, Key.down]

#list of optimal moves
optkeylst = [Key.left, Key.down]

#dictionary of all observable coords
#  key=1/16square : value=(x, y)coordinate
# intended use 1280x720 resolution
coordsdict = {"topCornerLeft":[480, 180],
			  "topMidLeft":[595, 180],
			  "topMidRight":[700, 180],
			  "topCornerRight":[810, 180],
			  "upCornerLeft":[480, 285],
			  "upMidLeft":[595, 285],
			  "upMidRight":[700, 285],
			  "upCornerRight":[810, 285],
			  "lowCornerLeft":[480, 400],
			  "lowMidleft":[595, 400],
			  "lowMidRight":[700, 400],
			  "lowCornerRight":[810, 400],
			  "bottomCornerleft":[480, 510],
			  "bottomMidLeft":[595, 510],
			  "bottomMidRight":[700, 510],
			  "bottomCornerRight":[810, 510]}

#dicitonary of all colors of different square values
#  key=numbervalue : value=RGBvalueofcolor
colorsdict = {"empty":195,
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

#adds current board colors 
def coordsColorArray():
	colorcords = []
	for i in coordsdict:
		colorcords.append(pixelAt(coordsdict.get(i)[0], coordsdict.get(i)[1]))
	return colorcords	

#ASCII GUI to view what is happening
# on the board as text output
def ptuiPrintOut():
	count = 0
	ca = coordsColorArray()
	for j in range(0,3):
		for j in range(count, len(ca)):
			if ca[j] in colorsdict:
				print(colorsdict.get(ca[j])),
			else:
				print("n/a"),
			count += 1
		print(" ")
		
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
	runTime = 1
	time.sleep(1)
	for i in range(0, runTime):
		time.sleep(breakTime)
		pressKey(Key.up)
		time.sleep(breakTime)
		pressKey(Key.down)
		for i in range(0, 15):
			time.sleep(breakTime)
			idx = random.randint(0,1)
			pressKey(optkeylst[idx])

'''
MAIN
'''
def main():
	url = "http://2048game.com/"
	wb = webbrowser.get("google-chrome")
	wb.open(url, 1, True)

	kb.press(Key.f11)
	kb.release(Key.f11)

	time.sleep(2)

	print(ptuiPrintOut())
	#time.sleep(5)
	
	#coordsColorPrintOut()
	#randomOptimalMoveSet()
	
	killBrowser()

	#testing below
	
	#pixelAt(coordsdict.get("topCornerLeft")[0], coordsdict.get("topCornerLeft")[1])
	
main()

