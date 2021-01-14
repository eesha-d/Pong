#!/usr/bin/python3 -u
import cv2
import numpy as np

file_name = 'scoreboard.csv'

def readScoreboard():
	with open(file_name, 'r') as f:
		data = f.read()

	#convert data into array with one line as element
	data=data.strip().split('\n')

	# We don't need the header
	data=data[1:]

	# Fill up scores dict
	scores={}
	for d in data:
		values=d.strip().split(',')
		scores[values[0]]={'Score': values[1], 'Level': values[2]}
		
	return scores

def writeScoreboard(scores):
	# Open file
	f=open(file_name, 'w')
	
	# Write header
	f.write('PlayerName,Score,Level\n')

	# Write data
	for s in scores:
		PlayerName=s
		Score=str(scores[s]['Score'])
		Level=str(scores[s]['Level'])
		line=PlayerName + ',' + Score + ',' + Level + '\n'
		f.write(line)

	f.close()	

def countPlayers(scores):
	return len(scores)

#update scoreboard with new or changed player data 
def updateScoreBoard(name, score, level):
	print ('updating scoreboard')
	# get current scoreboard
	scores=readScoreboard()

	# update player highscore (or add new one if doesn't exist)
	if name in scores:
		if int(score)<int(scores[name]['Score']):
			print('not updating highscore for',name)
			return

	scores[name]={'Score': score, 'Level': level}

	# Write back to file
	writeScoreboard(scores)

def displayScoreBoard():
	while True:
		img_height=400
		img_width=400

		#text settings
		font=cv2.FONT_HERSHEY_SIMPLEX
		colour=(255, 0, 0)
		thickness=2
		img=np.zeros([img_height,img_width],dtype=np.uint8) #image
		img.fill(0) 

		scores=readScoreboard()

		y=30
		cv2.putText(img, 'PlayerName', (img_width//3-75, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
		cv2.putText(img, 'Score', (2*img_width//3-100, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
		cv2.putText(img, 'Level', (img_width-img_width//3, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
		y+=20
		cv2.putText(img, '-------', (img_width//3-75, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
		cv2.putText(img, '----', (2*img_width//3-100, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
		cv2.putText(img, '----', (img_width-img_width//3, y), font, 0.5, colour, thickness, cv2.LINE_AA) 

		y+=20
		#display scores
		for s in scores:
			PlayerName=s
			Score=str(scores[s]['Score'])
			Level=str(scores[s]['Level'])
			cv2.putText(img, PlayerName, (img_width//3-75, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
			cv2.putText(img, Score, (2*img_width//3-100, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
			cv2.putText(img, Level, (img_width-img_width//3, y), font, 0.5, colour, thickness, cv2.LINE_AA) 
			y+=30

		cv2.putText(img, "Select p to play", (img_width//2-65, y), font, 0.5, colour, thickness, cv2.LINE_AA)

		cv2.imshow('image', img)

		selectKey=cv2.waitKey(0)
		if selectKey==ord('p'):
			return #end scoreboard display

		if selectKey==ord('q'):
			quit()

if __name__ == '__main__':
	img = displayScoreBoard()
	cv2.imshow('image', img)
	cv2.waitKey(0)



