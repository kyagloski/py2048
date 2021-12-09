
#2048 - Automator

from pynput.keyboard import Key, Controller
from selenium import webdriver
import time
import random

'''
STATE
'''
#keyboard
kb = Controller()

chromePath = "/home/kyle/gitrepos/py2048/chromedriver"

#list of all possible moves
keylst = [Key.left, Key.right, Key.up, Key.down]

#list of optimal moves
optkeylst = [Key.left, Key.down]

#url containing game
url = 'http://2048game.com/'
#url = 'https://hczhcz.github.io/2048/20ez/'

#script that grabs storage to be run in the driver
scriptArray = """localStorage.setItem("key1", 'new item');
               localStorage.setItem("key2", 'second item'); 
				return Array.apply(0, new Array(localStorage.length)).map(function (o, i) { return localStorage.getItem(localStorage.key(i)); }
				)""" 	

'''
CORE FUNCTIONALITY
'''

#presses key
def pressKey(key):
	kb.press(key)
	kb.release(key)

#presses keys ctrl + w to close the tab of the browser
def killBrowser():
	kb.press(Key.ctrl)
	kb.press('w')
	kb.release(Key.ctrl)
	kb.release('w')

#grabs board data
def getData(driver):
	data = driver.execute_script(scriptArray)
	return data[0]

#the single most beautiful piece of code I have ever written
#creates a matrix out of a data string
def buildDataMatrix(string):
	idx = 0
	tile_array_unformatted = []
	tile_array = []
	for i in string:
		if i == 'v' and string[idx+1] == 'a' and string[idx+2] == 'l' and string[idx+3] == 'u' and string[idx+4] == 'e':
			iter = 7
			number = ""
			while string[idx+iter].isdigit():
				number += string[idx+iter]
				iter += 1
			tile_array_unformatted.append(int(number))
		if i == 'n' and string[idx+1] == 'u' and string[idx+2] == 'l' and string[idx+3] == 'l':
			tile_array_unformatted.append(0)
		idx += 1
	for i in range(4):
		tile_array.append(tile_array_unformatted[i::4]) #this is pure magic
	return(tile_array)

#creates visualization of the current board
def buildPTUI(matrix):
	idx = 0
	for r in range(0, 4):
		for c in range(0, 4):
			try:
				print(matrix[r][c], end =" ")
			except:
				pass
		print("")
	print("")


'''
SOLVING ALGORITHMS
'''

#checks forwards 1 - 3 tiles
def checkForwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	if col == 3:
		return mergableNum, mergableTiles
	try:
		if elem == matrix[row][col+1] and matrix[row][col+1] != 0:
			mergableTiles.append(matrix[row][col+1])
			mergableNum += 1
			return mergableNum, mergableTiles
		elif matrix[row][col+1] == 0:
			if elem == matrix[row][col+2] and matrix[row][col+2] != 0:
				mergableTiles.append(matrix[row][col+2])
				mergableNum += 1
				return mergableNum, mergableTiles
			elif matrix[row][col+2] == 0:
				if elem == matrix[row][col+3] and matrix[row][col+3] != 0:
					mergableTiles.append(matrix[row][col+3])
					mergableNum += 1
					return mergableNum, mergableTiles
	except:
		pass
	return mergableNum, mergableTiles

#checks backwards 1 - 3 tiles
def checkBackwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	if col == 0:
		return mergableNum, mergableTiles
	try:
		if elem == matrix[row][col-1] and matrix[row][col-1] != 0:
			mergableTiles.append(matrix[row][col-1])
			mergableNum += 1
			return mergableNum, mergableTiles
		elif matrix[row][col-1] == 0 and col - 2 >= 0:
			if elem == matrix[row][col-2] and matrix[row][col-2] != 0:
				mergableTiles.append(matrix[row][col-2])
				mergableNum += 1
				return mergableNum, mergableTiles
			elif matrix[row][col-2] == 0 and col - 3 >= 0:
				if elem == matrix[row][col-3] and matrix[row][col-3] != 0:
					mergableTiles.append(matrix[row][col-3])
					mergableNum += 1
					return mergableNum, mergableTiles
	except:
		pass
	return mergableNum, mergableTiles

#checks upwards 1 - 3 tiles
def checkUpwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	if row == 0:
		return mergableNum, mergableTiles
	try:
		if elem == matrix[row-1][col] and matrix[row-1][col] != 0:
			mergableTiles.append(matrix[row-1][col])
			mergableNum += 1
			return mergableNum, mergableTiles
		elif matrix[row-1][col] == 0 and row - 2 >= 0:
			if elem == matrix[row-2][col] and matrix[row-2][col] != 0:
				mergableTiles.append(matrix[row-2][col])
				mergableNum += 1
				return mergableNum, mergableTiles
			elif matrix[row-2][col] == 0 and row - 3 >= 0:
				if elem == matrix[row-3][col] and matrix[row-3][col] != 0:
					mergableTiles.append(matrix[row-3][col])
					mergableNum += 1
					return mergableNum, mergableTiles
	except:
		pass
	return mergableNum, mergableTiles

#checks downwards 1 - 3 tiles
def checkDownwards(matrix, row, col):
	mergableNum = 0
	mergableTiles = []
	elem = matrix[row][col]
	if row == 3:
		return mergableNum, mergableTiles
	try:
		if elem == matrix[row+1][col] and matrix[row+1][col] != 0:
			mergableTiles.append(matrix[row+1][col])
			mergableNum += 1
			return mergableNum, mergableTiles
		elif matrix[row+1][col] == 0:
			if elem == matrix[row+2][col] and matrix[row+2][col] != 0:
				mergableTiles.append(matrix[row+2][col])
				mergableNum += 1
				return mergableNum, mergableTiles
			elif matrix[row+2][col] == 0:
				if elem == matrix[row+3][col] and matrix[row+3][col] != 0:
					mergableTiles.append(matrix[row+3][col])
					mergableNum += 1
					return mergableNum, mergableTiles
	except:
		pass
	return mergableNum, mergableTiles

def checkDiagonal(matrix):
	diagonalMerge = 0
	for col in range(0, 4):
		for row in range(0, 4):
			try:
				if matrix[row-1][col-1] == matrix[row][col]:
					diagonalMerge += 1
			except:
				pass
	return diagonalMerge
				

#calculates currently available merge directions and mergable blocks
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
			try:
				if matrix[row][col] != 0:
					TEMPmergableNum, TEMPmergableTiles = checkForwards(matrix, row, col)
					if TEMPmergableNum != 0:
						forwardMerges += TEMPmergableNum
						forwardList = TEMPmergableTiles
					TEMPmergableNum, TEMPmergableTiles = checkBackwards(matrix, row, col)
					if TEMPmergableNum != 0:
						backwardMerges += TEMPmergableNum
						backwardList = TEMPmergableTiles
					TEMPmergableNum, TEMPmergableTiles = checkUpwards(matrix, row, col)
					if TEMPmergableNum != 0:
						upwardMerges += TEMPmergableNum
						upwardList = TEMPmergableTiles
					TEMPmergableNum, TEMPmergableTiles = checkDownwards(matrix, row, col)
					if TEMPmergableNum != 0:
						downwardMerges += TEMPmergableNum
						downwardList = TEMPmergableTiles
			except:
				pass
	return forwardList, backwardList, upwardList, downwardList, forwardMerges, backwardMerges, upwardMerges, downwardMerges 

#determines if game has ended
def isGameOver(string):
	if string == "second item":
		return True
	return False

def gamePlay(driver):
	gameovers = 0
	breakTime = 0.05
	enumerator = 0
	print("Game Starting ... ")
	string = getData(driver)
	previousMatrix = [[]]
	while isGameOver(string) == False:
		string = getData(driver)
		matrix = buildDataMatrix(string)
		buildPTUI(matrix)
		mergeList = []
		directionList = []
		forwardList, backwardList, upwardList, downwardList, forwardMerges, backwardMerges, upwardMerges, downwardMerges  = mergableTiles(matrix)
		diagonalMerge = checkDiagonal(matrix)
		mergeList.append(forwardMerges)
		mergeList.append(backwardMerges)
		mergeList.append(upwardMerges)
		mergeList.append(downwardMerges)
		directionList.append(forwardList)
		directionList.append(backwardList)
		directionList.append(upwardList)
		directionList.append(downwardList)
		print("merge list : ", mergeList)
		print("direction list : ", directionList)
		largestMergeAmount = 0
		largestMergeElem = 0
		amountDirection = 0
		elemDirection = 0
		idx = -1
		for elem in mergeList:
			idx +=1 
			if elem > largestMergeAmount:
				largestMergeAmount = elem
				amountDirection = idx
		idx = -1
		for lst in directionList:
			idx += 1
			for elem in lst:
				if elem > largestMergeElem:
					largestMergeElem = elem
					elemDirection = idx
		if largestMergeElem == 0 and largestMergeAmount == 0:
			time.sleep(breakTime)
			pressKey(Key.up)
		if largestMergeAmount > largestMergeElem:
			if amountDirection == 0:
				time.sleep(breakTime)
				pressKey(Key.right)
			elif amountDirection == 1:
				time.sleep(breakTime)
				pressKey(Key.left)
			elif amountDirection == 2:
				time.sleep(breakTime)
				pressKey(Key.up)
			elif amountDirection == 3:
				time.sleep(breakTime)
				pressKey(Key.down)
		elif largestMergeElem > largestMergeAmount:
			if elemDirection == 0:
				time.sleep(breakTime)
				pressKey(Key.right)
			elif elemDirection == 1:
				time.sleep(breakTime)
				pressKey(Key.left)
			elif elemDirection == 2:
				time.sleep(breakTime)
				pressKey(Key.up)
			elif elemDirection == 3:
				time.sleep(breakTime)
				pressKey(Key.down)
		if diagonalMerge >= 6 and matrix[0][3] >= 128 and matrix[0][0] != 0:
			print(diagonalMerge, "diagonal merging ...")
			time.sleep(breakTime)
			#pressKey(Key.left)
			time.sleep(breakTime)
			#pressKey(Key.up)
		if previousMatrix == matrix:
			time.sleep(breakTime)
			pressKey(Key.up)
			previousMatrix = matrix
			string = getData(driver)
			matrix = buildDataMatrix(string)
			if previousMatrix == matrix:
				time.sleep(breakTime)
				pressKey(Key.right)
				previousMatrix = matrix
				string = getData(driver)
				matrix = buildDataMatrix(string)
				if previousMatrix == matrix and matrix[0][0] != 0:
					time.sleep(breakTime)
					pressKey(Key.left)
					previousMatrix = matrix
					string = getData(driver)
					matrix = buildDataMatrix(string)
				elif previousMatrix == matrix:
					time.sleep(breakTime)
					pressKey(Key.down)
		previousMatrix = matrix
		enumerator += 1
	string = getData(driver)
	if isGameOver(string) == True:
		print("Game Over!!")
		killBrowser()
		driver = webdriver.Chrome(executable_path=r"" + chromePath)
		driver.get(url)
		gamePlay(driver)

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
def randomOptimalMoveSet(driver):
	gameovers = 0
	breakTime = 0.0
	runTime = 10000
	time.sleep(1)
	for i in range(0, runTime):
		time.sleep(breakTime)
		pressKey(Key.up)
		time.sleep(breakTime)
		pressKey(Key.down)
		string = getData(driver)
		#print(string)
		ma = buildDataMatrix(string)
		print(mergableTiles(ma))
		buildPTUI(ma)
		if isGameOver(string) == True:
			time.sleep(1.5)
			pressKey('r')
			gameovers += 1
			print(gameovers)
		for i in range(0, 15):
			time.sleep(breakTime)
			idx = random.randint(0,1)
			pressKey(optkeylst[idx])
			string = getData(driver)
			#print(string)
			ma = buildDataMatrix(string)
			print(mergableTiles(ma))
			buildPTUI(ma)
			if isGameOver(string):
				time.sleep(1.5)
				pressKey('r')
				gameovers += 1
				print(gameovers)

'''
MAIN
'''
def main():
	
	driver = webdriver.Chrome(executable_path=r"" + chromePath)
	driver.get(url)
	#print(getData(driver))
	#randomOptimalMoveSet(driver)
	gamePlay(driver)
	#kb.press(Key.f11)
	#kb.release(Key.f11)
	
	'''
	TESTING BELOW
	'''
	
	'''
	for i in range(10000):
		time.sleep(0.5)
		matrix = buildDataMatrix(driver)
		print(mergableTiles(matrix))
	'''
	#randomOptimalMoveSet()
	#killBrowser()

if __name__ == '__main__':
	main()
