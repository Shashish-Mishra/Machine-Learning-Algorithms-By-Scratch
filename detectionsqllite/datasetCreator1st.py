import cv2
import numpy as np
import sqlite3

faceDetect=cv2.CascadeClassifier('C:\\Users\\amit\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)

def InsertOrUpdate(Id, Name, Gender, Occupation, Age):
    con=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(Id)
    cursor=con.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name=%r ,Gender=%r ,Occupation=%r ,Age=%r WHERE ID=%d"%(Name,Gender,Occupation,Age,int(Id))
        con.execute(cmd)
        con.commit()
        
    else:
        cmd="INSERT INTO People Values(%r,%r,%r,%r,%r)"%(Id, Name, Gender, Occupation, Age)
        con.execute(cmd)
        con.commit()
        con.close()

id1=input('Enter User ID')
name=input('Enter your Name')
gender=input('Enter your Gender')
occupation=input('Enter your Occupation')
Age=input('Enter your Age')
InsertOrUpdate(id1, name, gender, occupation, Age)

sampleNum=0
while(True):
    ret, img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray, 1.3,5)
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1
        cv2.imwrite("Dataset/User."+str(id1)+"."+str(sampleNum)+".jpg", gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.waitKey(100)
    cv2.imshow("Frame", img)
    cv2.waitKey(1)
    if(sampleNum>30):
        break
cam.release()
cv2.destroyAllWindows()
