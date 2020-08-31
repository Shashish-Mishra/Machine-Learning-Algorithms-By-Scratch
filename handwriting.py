import io
import cv2,os
from PIL import Image
from tkinter import *
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from google.oauth2 import service_account
from tkinter import messagebox
cred = service_account.Credentials.from_service_account_file('My First Project-35c0b557d0ed.json')


client = vision.ImageAnnotatorClient(credentials=cred)
def detect_text(path):
    """Detects text in the file."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    string = ''

    for text in texts:
        string+=' ' + text.description
    return string

cap = cv2.VideoCapture(0)
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
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    file = 'live.png'
    cv2.imwrite( file,frame)
    data=detect_text(file)
    if len(data)>1:
        print(data)
        # print OCR text
        scr=Tk()
        scr.geometry('0x0+0+0')
        if messagebox.askyesnocancel('Hand writing detection','do you want to save the text'):
            open('data.txt','a').write(str(data))
        scr.destroy()
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1)!=-1:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
