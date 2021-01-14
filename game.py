
import cv2
import numpy as np
import math
import random
import time
import scoreboard
import csv
import sys

img_height=400
img_width=400

#display home to the user 
def getHomeScreen():
	#text settings
	font=cv2.FONT_HERSHEY_SIMPLEX
	colour=(255, 0, 0)
	thickness=2
	img = np.zeros([img_height,img_width],dtype=np.uint8) #image
	img.fill(0) 
	cv2.putText(img, "Pong", (175, 50), font, 0.8, colour, thickness, cv2.LINE_AA)
	cv2.putText(img, "Select p to play", (img_width//2-65, 200), font, 0.5, colour, thickness, cv2.LINE_AA)
	cv2.putText(img, "Select s to see scoreboard", (img_width//2-100, 250), font, 0.5, colour, thickness, cv2.LINE_AA)
	return img

#runs the game, allowing the user to view the scoreboard before and after each round
#also allows the user to replay the game
if __name__ == '__main__':

	condition1=True #will run until 'q' key is pressed to quit
	while(condition1):
		cv2.imshow("image", getHomeScreen()) # Show home screen in the beginning

		key=cv2.waitKey(0)

		if(key==ord('s')):
			scoreboard.displayScoreBoard() #display scoreboard
			key=ord('p') #load game
		
		condition2=True #will run while user is 'alive' in the game
		while(condition2):
			if(key==ord('p')):
				box_height=8 #height of box used to hit ball
				box_width=50 #width of box used to hit ball
				circle_radius=10 #radius of ball

				x1=img_width//2-box_width//2 #left edge of box
				y1=img_height-box_height #top edge of box
				y_centre=img_height//2 #y-coordinate of centre of screen
				x_centre=img_width//2 #x-coordinate of centre of screen

				x_increment=20 #increment by which box moves

				shiftSpeed=3 #initial speed of ball
				speedCounter=0 #counter for rounds to determine when speed should change


				img = np.zeros([img_height,img_width],dtype=np.uint8) #image
				img.fill(255) 


				cv2.rectangle(img,(x1,y1),(x1+box_width, y1+box_height), 0, -1) #create black rectangle
				cv2.circle(img, (y_centre, x_centre), circle_radius, 0, -1) #create black circle


				degrees=30 #initial angle in degrees
				originalAngle=degrees*math.pi/180 #convert to radians


				#calculate the reference angle
				if(originalAngle>=0 and originalAngle<=math.pi/2): #first quadrant 
					referenceAngle=originalAngle

				elif(originalAngle>math.pi/2 and originalAngle<=math.pi): #second quadrant 
					referenceAngle=math.pi-originalAngle

				elif(originalAngle>math.pi and originalAngle<=3*math.pi/2): #third quadrant
					referenceAngle=originalAngle-math.pi

				elif(originalAngle>3*math.pi/2 and originalAngle<2*math.pi): #fourth quadrant
					referenceAngle=2*math.pi-originalAngle


				y_shift=round(shiftSpeed*math.sin(originalAngle)) #calculate each y shift for circle
				x_shift=round(shiftSpeed*math.cos(originalAngle)) #calculatue eaxh x shift for circle


				prev_speedCounter = -1
				while True and condition2:
					key = cv2.waitKey(20)

					level = (speedCounter//3)+1
					level_text="Level "+str(level) #levels up every 3 rounds
					
					if prev_speedCounter != speedCounter:
						name=sys.argv[1]
						scoreboard.updateScoreBoard(name, speedCounter, level)
					prev_speedCounter = speedCounter

					cv2.rectangle(img,(img_width//2-75,img_height//2-50),(img_width//2 + 75,img_height//2+50), 255, -1) #clear Level text area
					cv2.putText(img, level_text, (img_width//2 - 50,img_height//2), cv2.FONT_HERSHEY_SIMPLEX, 1, 200, 1, cv2.LINE_AA)


					cv2.rectangle(img,(x1,y1),(x1+box_width, y1+box_height), 255, -1) #clear rectangle

					#if user moves left
					if key==ord('a'): 
						if (x1-x_increment>0 and x1>0): #shift box
							x1-=x_increment
						elif(x1-x_increment<0 and x1>0): #will go past bounds, turn around
							x1=0

					#if user moves right
					elif key==ord('d'): 
						if (x1+box_width<img_width and x1+box_width+x_increment<img_width): 
							x1+=x_increment
						elif(x1+box_width<img_width and x1+box_width+x_increment>box_width):
							x1=img_width-box_width



					
					if ((y_centre>circle_radius and y_centre<img_height-circle_radius) and (x_centre>circle_radius and x_centre<img_height-circle_radius)): #in bounds
					
						cv2.circle(img, (x_centre, y_centre), circle_radius+15, 255, -1) #cover black circle
					
						#shift ball
						y_centre-=y_shift 
						x_centre+=x_shift

						cv2.circle(img, (x_centre, y_centre), circle_radius, 0, -1) #translated black circle



					elif(y_centre<=circle_radius and x_shift>=0): #upper boundary hit while travelling to the right
						angle=2*math.pi-referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 #generate random change in angle and convert to radians
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift
						


					elif(y_centre<=circle_radius and x_shift<0): #upper boundary hit while travelling to the left
						angle=math.pi+referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift


					elif(x_centre+x_shift>=x1 and x_centre<=x1+box_width and y_centre+y_shift>=img_height-box_height-circle_radius and x_shift<=0): #box hit from left
						x_centre=x_centre+x_shift
						y_centre=img_height-box_height-circle_radius
						angle=math.pi-referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift
						speedCounter+=1
						if(speedCounter%3==0): #speed increases every 3 hits
							shiftSpeed+=1


					elif(x_centre+x_shift>=x1 and x_centre<=x1+box_width and y_centre+y_shift>=img_height-box_height-circle_radius and x_shift>0): #box hit from right
						x_centre=x_centre+x_shift
						y_centre=img_height-box_height-circle_radius
						angle=referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift
						speedCounter+=1
						if(speedCounter%3==0): 
							shiftSpeed+=1


					elif(y_centre>=img_height-circle_radius and x_shift<=0): #lower boundary hit and travelling to the left
						name=sys.argv[1]
						level=str((speedCounter//3)+1)
						scoreboard.updateScoreBoard(name, speedCounter, level)
						speedCounter=0 #reset speedCounter
						shiftSpeed=3 #reset shiftSpeed
						condition2=False #don't go through second and third while loops after player 'dies'


					elif(y_centre>=img_height-circle_radius and x_shift>0): #lower boundary hit and travelling to the right
						name=sys.argv[1]
						level=str((speedCounter//3)+1)
						scoreboard.updateScoreBoard(name, speedCounter, level)
						speedCounter=0 
						shiftSpeed=3 
						condition2=False


					elif(x_centre<=circle_radius and y_shift>=0): #left boundary hit and travelling upwards
						angle=referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift


					elif(x_centre<=circle_radius and y_shift<0): #left boundary hit and travelling downwards
						angle=2*math.pi-referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift


					elif(x_centre>=img_width-circle_radius and y_shift<=0): #right boundary hit and travelling downwards
						angle=math.pi+referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift


					elif(x_centre>=img_width-circle_radius and y_shift>0): #right boundary hit and travelling upwards
						angle=math.pi-referenceAngle
						angleShift=math.pi*random.randint(-5,5)/180 
						angle+=angleShift
						x_shift=round(shiftSpeed*math.cos(angle))
						y_shift=round(shiftSpeed*math.sin(angle)) 
						x_centre+=x_shift
						y_centre-=y_shift




					cv2.rectangle(img,(x1,y1),(x1+box_width, y1+box_height), 0, -1) #new rectangle



					cv2.imshow('image', img)

					if key==ord('q'):
						quit()

			if key==ord('q'):
						quit()
	














