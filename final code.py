
import numpy as np
import cv2
import time
from datetime import datetime
import pyttsx
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)
p = GPIO.PWM(7, 50)
p.start(7.5)


app1= ClarifaiApp(api_key='f05450e2dce34fe39034900d9fe5d1d7')
#app1= ClarifaiApp(api_key='a75a5d1ddf924167a62f700e800b31be')
model1 = app1.models.get('hb')

face_cascade = cv2.CascadeClassifier('haar-face.xml')

def voice():
    engine = pyttsx.init()
    engine.say(Voice)
    engine.runAndWait()
    time.sleep(2)

cap = cv2.VideoCapture(0)
print 'camera is initialized'

while True:
    Voice='please stand in the position...we are capturing your image'
    voice()
    time.sleep(5)
    ret, img = cap.read()
    if ret:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            picname = datetime.now().strftime("%y-%m-%d-%H-%M")
            picname = picname+'.jpg'
            cv2.imwrite(picname,img)
            print "Saving Photo"
            pic='/home/pi/Downloads/111.jpg'
            print pic
            pic1='/home/pi/Downloads/'+picname
            print pic1
            image = ClImage(file_obj=open(pic, 'rb'))
            response=model1.predict([image])
            data1 = response['outputs'][0]['data']['concepts']
            print data1
            for row in data1: 
                if row['name'] == 'helmet':
                    if row['value']>= 1.590712e-08:
                        x=1
                    else:
                        print 'please wear the helmet'
            time.sleep(2)
            t=model1.predict([image])
            data2 = t['outputs'][0]['data']['concepts']
            print data2
            d="Men"+"'"+"s"+" "+"Sandals"
            e="Men"+"'"+"s"+" "+"Boots"
            for row in data2:
                if row['name'] ==d:
                    if row['value']>0.00001:
                        y=1
                elif row['name'] ==e:
                    if row['name']>0.00001:
                        y=1
                else:
                    z=0           
            if(x==1 and y==1):
                print "you can enter inside"  
                p.ChangeDutyCycle(12.5) #180°
                time.sleep(2)
                p.ChangeDutyCycle(7.5) 
                Voice = 'you   can   enter   inside'
                voice()
                  
            else:
                print "your     entry is restricted"
                Voice = 'please     wear     the    shoes  and   helmet  to  enter'
                voice()
                time.sleep(10)
                
    cv2.imshow('img',img)
    time.sleep(0.1)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
cap.release()
cv2.destroyAllWindows()
