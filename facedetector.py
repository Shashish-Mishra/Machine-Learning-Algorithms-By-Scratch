from collections import Counter
import matplotlib.pyplot as plt
import cv2
import re
import numpy as np
import os
# Imports the Google Cloud client library
from google.cloud import vision

#Emotions
emo = ['Angry', 'Surprised','Sad', 'Happy', "Under Exposed", "Blurred", "Headwear"]
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                    'LIKELY', 'VERY_LIKELY')
from google.oauth2 import service_account
cred = service_account.Credentials.from_service_account_file('My First Project-35c0b557d0ed.json')

# Instantiates a client
vision_client = vision.ImageAnnotatorClient(credentials=cred)

myemotions=[]
myemotion_acc=dict.fromkeys(['Angry', 'Surprised','Sad', 'Happy', "Under Exposed", "Blurred", "Headwear",'No sentiment'],0)
for i in myemotion_acc:
    myemotion_acc[i]=[]
compressRate = 1
video_capture = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

direc=os.listdir()
datafolder=[i for i in direc if 'output' in i]
if len(datafolder)>0:
    data=[int(re.search(r'\d+',i).group()) for i in datafolder if re.search(r'\d+',i)]
    new1=max(data)+1
    fldnaam='output{}'.format(new1)
    os.mkdir('output{}'.format(new1))
    os.chdir(os.getcwd()+'\\'+fldnaam)
else:
    os.mkdir('output1')
    os.chdir(os.getcwd()+'\\'+'output1')
_,img=video_capture.read()
cv2.imshow('Video', img)
filename='face1.jpg'
out = cv2.VideoWriter('face.avi', fourcc, 20.0, (640,480))
number=1
while cv2.getWindowProperty('Video', 0) >= 0:
    ret, img = video_capture.read()
    
    img.shape
    img = cv2.resize(img, (0,0), fx=compressRate , fy=compressRate )
    
    
    ok, buf = cv2.imencode(".jpeg",img)
    image = vision.types.Image(content=buf.tostring())

    response = vision_client.face_detection(image=image)
    faces = response.face_annotations 
    print('Number of faces: ', len(faces))
    for face in faces:
        x = face.bounding_poly.vertices[0].x
        y = face.bounding_poly.vertices[0].y
        x2 = face.bounding_poly.vertices[2].x
        y2 = face.bounding_poly.vertices[2].y
        cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)

        sentiment = [likelihood_name[face.anger_likelihood],
                    likelihood_name[face.surprise_likelihood],
                    likelihood_name[face.sorrow_likelihood],
                    likelihood_name[face.joy_likelihood],
                    likelihood_name[face.under_exposed_likelihood],
                    likelihood_name[face.blurred_likelihood],
                    likelihood_name[face.headwear_likelihood]]

        for item, item2 in zip(emo, sentiment):
            print (item, ": ", item2)

        string = 'No sentiment'

        if not (all( item == 'VERY_UNLIKELY' for item in sentiment) ):
            if any( item == 'VERY_LIKELY' for item in sentiment):
                state = sentiment.index('VERY_LIKELY')
                # the order of enum type Likelihood is:
                #'LIKELY', 'POSSIBLE', 'UNKNOWN', 'UNLIKELY', 'VERY_LIKELY', 'VERY_UNLIKELY'
                # it makes sense to do argmin if VERY_LIKELY is not present, one would espect that VERY_LIKELY
                # would be the first in the order, but that's not the case, so this special case must be added
            else:
                state = np.argmin(sentiment)

            string = emo[state]

        cv2.putText(img,string, (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        myemotions.append(string)
        print(faces[0].detection_confidence) #acuracy
        myemotion_acc[string].append(faces[0].detection_confidence)

    cv2.imshow("Video", img)
    cv2.imwrite(filename,img)
    number+=1
    filename='face{}.jpg'.format(number)
    cv2.waitKey(1)
mydata=dict.fromkeys(['Angry', 'Surprised','Sad', 'Happy', "Under Exposed", "Blurred", "Headwear",'No sentiment'],0)
mydata.update(dict(Counter(myemotions)))
x1=list(range(len(mydata.keys())))
emotiondetected=Counter(myemotions).most_common(1)[0][0]
for i in myemotion_acc:
    if len(myemotion_acc[i])>0:
        myemotion_acc[i]=np.mean(np.array(myemotion_acc[i]))
    else: myemotion_acc[i]=np.nan
print(Counter(myemotions),myemotion_acc)
pos=['Happy','No sentiment','Sad']
if pos.count(emotiondetected)!=0:
    head='the vigilance is "TRUTH"'
else:
    head='the Vigilance is "LIE"'
    

plt.bar(x1,list(mydata.values()),tick_label=list(mydata.keys()))
plt.xlabel('sentiments')
plt.ylabel('scores')
plt.title(head)
out.write(img)
plt.show()
video_capture.release()
cv2.destroyAllWindows()
