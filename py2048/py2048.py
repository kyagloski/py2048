
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
colorsdict = {"empty":[205, 193, 180],
              "2":[238, 228, 218],
	      	  "4":[237, 224, 200],
	      	  "8":[242, 177, 121],
	      	  "16":[245, 149, 99],
			  "32":[246, 124, 95],
			  "64":[246, 94, 59],
			  "128":[237, 207, 114],
			  "256":[237, 204, 97],
			  "512":[]
			  }

#prints out formatted color value of each square
def coordsColorPrintOut():
	for i in coordsdict:
		print("______________________________________________\n")
		print(i)
		print(pixelAt(coordsdict.get(i)[0], coordsdict.get(i)[1]))	

#presses key
def pressKey(key):
	kb.press(key)
	kb.release(key)

#presses random keys from the full key set array
def randomFullMoveSet():
	time.sleep(5)
	for i in range(0, 1000):
		time.sleep(0.15)
		idx = random.randint(0,1)
		pressKey(optkeylst[idx])

#presses random keys from the optimal key set array,
#also added extra functionality for a more optimal algorithm
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

#gets pixel at coordinate 
#returns array of r, g, b color values 
def pixelAt(x, y):
	w = gtk.gdk.get_default_root_window()
	sz = w.get_size()
	pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
	pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
	pixel_array = pb.get_pixels_array()
	return pixel_array[y][x]	

#Eventually implement threading to observe pixel colors
'''
def thread_function(x, y):
	return 0	

def pixelObservers():
	thread = threading.Thread(target=thread_function, args=(1,))
	thread.start()
'''

#presses keys ctrl + w to close the tab of the browser
def killBrowser():
	kb.press(Key.ctrl)
	kb.press('w')
	kb.release(Key.ctrl)
	kb.release('w')

#main
def main():
	url = "http://2048game.com/"
	wb = webbrowser.get("google-chrome")
	wb.open(url, 1, True)
	kb.press(Key.f11)
	kb.release(Key.f11)
	time.sleep(5)

	coordsColorPrintOut()
	randomOptimalMoveSet()
	
	killBrowser()

main()




