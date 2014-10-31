import math
import cv2
import numpy as np
import serial
#import cv2.cv

def nothing(x):
	pass
y_h =  0 
x_h = 0.1
x_l = 0.2
y_l = 0.3
char = 'n'
cap = cv2.VideoCapture(1)
isopen=cap.isOpened()
#cv2.namedWindow('thresh')	
cv2.namedWindow('thresh')
	
ser = serial.Serial('/dev/ttyUSB0',57600,timeout=None)
print ser.name

	
if(isopen == False):
	cap.open()
else:
	while(True):
		
		ret, frameori = cap.read()
		frame = frameori[20:400, 40:600]
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		
		thresh = cv2.blur(gray,(5,5))	
		ret,thresh = cv2.threshold(thresh,70,255,cv2.THRESH_BINARY_INV)
		#thresh = cv2.adaptiveThreshold(thresh,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            #cv2.THRESH_BINARY,11,2)
		cv2.imshow('thresh',thresh)
		_,contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #uncomment when using openCV2
		
		cv2.drawContours(frame, contours, -1, (0,255,0), 1)

		#print 'contour #',len(contours)
		for i in range(0,len(contours)):
			cnt = contours[i]
			#x,y,w,h = cv2.boundingRect(cnt)
			rect = cv2.minAreaRect(cnt)
			print 'area'+str(i)+'= ',cv2.contourArea(cnt)
			if(cv2.contourArea(cnt)<110 and cv2.contourArea(cnt)>30):
				#print 'small', rect[1]
				y_l = rect[0][1]
				x_l = rect[0][0]
			if(cv2.contourArea(cnt)>=110 and cv2.contourArea(cnt)>30):
				#print 'large', rect[1]
				y_h = rect[0][1]
				x_h = rect[0][0]
			
			#if (cv2.contourArea(cnt)>50):
				#print i,rect[2]
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			#print box
			#print rect
			#cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
			
			cv2.drawContours(frame,[box],0,(0,0,255),1)
		#if (x_h-x_l == 0):
			#orient = 90	
		#else:
			#val = (y_h-y_l)/(x_h-x_l)
		cent_x= int((x_l+x_h)/(2*5))
		cent_y= int((y_l+y_h)/(2*5))
		#roi = gray[cent_y-100:cent_y+100,cent_x-100:cent_x+100]
		#cv2.imshow('roi',roi)
		
		orient = (-1)*math.degrees(math.atan2(y_h-y_l,x_h-x_l))
		if(orient < 0):
			orient = orient + 360
		elif(orient == -0):
			orient = 0		
		print 'rot=', int(orient)
		print '('+str(cent_x)+','+str(cent_y)+','+str(int(orient))+')'
		ser.write('('+str(cent_x)+','+str(cent_y)+','+str(int(orient))+')')
		cv2.imshow('frame',frame)
		if cv2.waitKey(1) == ord('s'):
			break
		


cap.release()
cv2.destroyAllWindows()
