import cv2
import numpy as np

#all the colors
mycolors = [[21,153,22,165,255,255],[15,168,40,87,255,221]]
mycolorvalues = [[255,0,0],[0,255,0]]
mypoints = []

#detecting colour
def findcolor(img,mycolors,mycolorvalues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in mycolors:#need to use for loop to create mask for each color
        lower = np.array(color[:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = findcontours(mask)
        cv2.circle(imgResult,(x,y),10,mycolorvalues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(color[0]),mask)
    return newpoints

#detecting object
def findcontours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500 :
            # cv2.drawContours(imgResult,cnt, -1, (255,0,0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.03*peri,True)#passing approxPolyDP(cotour, perimeter, closed = true or open = False)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y    

#drawing function
def draw(mypoints,mycolorvalues):
    for point in mypoints:
        cv2.circle(imgResult,(point[0],point[1]),10,mycolorvalues[point[2]],cv2.FILLED)     
#reading camera
cap = cv2.VideoCapture(1)#0 stands for primary camera id, if you have other camera use that id
#set function used to define different parameter with each parameter having its own id
cap.set(3,640)#here 3 = width, which is set to 640
cap.set(4,480)#here 4 = height, which is set to 480
cap.set(10,10)##here 10 = brightness, which is set to 100
#you can see rest parameters on internet
while True:
    success, img = cap.read()
    imgResult = img.copy()
    newpoints = findcolor(img,mycolors,mycolorvalues)
    if len(newpoints)!=0:
        for newp in newpoints:
            mypoints.append(newp)
    if len(mypoints)!=0:
        draw(mypoints,mycolorvalues)
            
    cv2.imshow('video',imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break