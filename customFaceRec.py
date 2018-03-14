
# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import os
from multiprocessing import Process
import time


def writeLastModified(lines):
    fh=open('id_track.txt','w')
    fh.writelines(lines)
    fh.close()
def readLastModified():
    fh=open('id_track.txt','r')
    lm={}
    for line in fh:
        name,date=line.split('|')[0],line.split('|')[1][:-1]
        lm[name]=date
    fh.close()
    return lm

def run_face_rec(app=None,known_encodings={}):
    
    # Get a reference to the Raspberry Pi camera.
    # If this fails, make sure you have a camera connected to the RPi and that you
    # enabled your camera in raspi-config and rebooted first.
    width,height=320,240 #320,240 by default
    camera = picamera.PiCamera()
    camera.resolution = (width, height)
    output = np.empty((height, width, 3), dtype=np.uint8)
    threshold=0.55 #how strict the camera should recognize

    # Load a sample picture and learn how to recognize it.
    print("Loading known face image(s)")

    #reading from "users" folder
    path=os.getcwd()+"/users"
    #print(path)
    imgFileExt=("gif","jpg","jpeg","png")
    filelist=[files for r,dirs,files in os.walk(path,topdown=True)][0] #get the list of all files
    imgList=[]
    #Select the file with name that like this "_abc.jpeg"
    lm=readLastModified()
    #print(lm)
    #print(filelist)
    #print(known_encodings.keys())
    lines_to_write=[]
    for file in filelist:
        #check if file is image and in the right format
        if file.lower().endswith(imgFileExt) and file[0]=="_":
            #check if new file or file has changed
            person=file[1:file.find(".")]
            if file not in lm or str(os.path.getmtime(path+'/'+file))!=lm[file] or (person not in known_encodings):   
                imgList.append(file)
            lines_to_write.append(file +"|"+ str(os.path.getmtime(path+'/'+file))+"\n")
    print(imgList)
    writeLastModified(lines_to_write)# write the list of read id
    
    
    for filename in imgList:
        person=filename[1:filename.find(".")]
        print("Loading sample face from "+person)
        face_encoding=face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+filename))[0]
        known_encodings[person]=face_encoding
    """    
    my_image = face_recognition.load_image_file("my.jpg")
    my_face_encoding = face_recognition.face_encodings(my_image)[0]
    neha_encoding= face_recognition.face_encodings(face_recognition.load_image_file("neha.jpeg"))[0]
    guk_encoding= face_recognition.face_encodings(face_recognition.load_image_file("guk.jpeg"))[0]
    known_encodings=[(my_face_encoding,"Duy Tang"),(neha_encoding,"Neha"),(guk_encoding,"Guk")]
    """

    # Initialize some variables
    face_locations = []
    face_encodings = []
    found=0
    
    folderList={}
    #start a new thread to display images
    #pid=None if app==None else app.pid
    #lock=None if app==None else app.lock
    if app!=None:
        app.newPerson.put("#Start capturing...")
    while found<len(known_encodings):
        print("Capturing ...")
        if app!=None:
            if app.exitQueue.qsize()>0:
                if app.exitQueue.get()=='x':
                    break
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="rgb")

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} face(s)".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)

        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = "<Unknown Person>"
            for known_name in known_encodings:
                known_encoding=known_encodings[known_name]
                match = face_recognition.compare_faces([known_encoding], face_encoding,threshold)
                if match[0]:
                    name=known_name
                    if known_name not in folderList:
                        folderList[known_name]=True
                        if app!=None:
                            app.newPerson.put(known_name)
                            print(app.newPerson.qsize())
                        found+=1
                    break
                    
            print("{} detected!".format(name))
    camera.close()
    print("Stop capturing")
    return known_encodings
'''
class RecognizeScript(Process):
    
    def __init__(self,camera,app=None,threshold=0.55):
        self.camera=camera
        print("Script initialized")
        self.width,self.height=320,240 #320,240 by default
        self.camera.resolution = (self.width, self.height)
        self.known_encodings={}
        self.threshold=threshold #how strict the camera should recognize
        self.app=app#slideshow app is expected here
        self.lastModified={}
        Process.__init__(self)

    def run(self):
        self.run_face_rec(self.app)
        
    def run_face_rec(self,app):
        # Get a reference to the Raspberry Pi camera.
        # If this fails, make sure you have a camera connected to the RPi and that you
        # enabled your camera in raspi-config and rebooted first.
        
        output = np.empty((self.height, self.width, 3), dtype=np.uint8)
        # Load a sample picture and learn how to recognize it.
        print("Loading known face image(s)")

        #reading from "users" folder
        path=os.getcwd()+"/users"
        #print(path)
        imgFileExt=("gif","jpg","jpeg","png")
        filelist=[files for r,dirs,files in os.walk(path,topdown=True)][0] #get the list of all files
        imgList=[]
        #Select the file with name that like this "_abc.jpeg" 
        for file in filelist:
            if file.lower().endswith(imgFileExt) and file[0]=="_":
                #check if the file is new or is modified
                if not file in self.lastModified:#if new
                    imgList.append(file)
                    self.lastModified[file]=os.path.getmtime(path+'/'+file)
                else:
                    #check for last modified date, see if not match
                    if self.lastModified[file]!=os.path.getmtime(path+'/'+file):
                        self.lastModified[file]=os.path.getmtime(path+'/'+file)
                        imgList.append(file)
        print(imgList)
        
        for filename in imgList:
            person=filename[1:filename.find(".")]
            print("Loading sample face from "+person)
            face_encoding=face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+filename))[0]
            self.known_encodings[person]=face_encoding
        """    
        my_image = face_recognition.load_image_file("my.jpg")
        my_face_encoding = face_recognition.face_encodings(my_image)[0]
        neha_encoding= face_recognition.face_encodings(face_recognition.load_image_file("neha.jpeg"))[0]
        guk_encoding= face_recognition.face_encodings(face_recognition.load_image_file("guk.jpeg"))[0]
        known_encodings=[(my_face_encoding,"Duy Tang"),(neha_encoding,"Neha"),(guk_encoding,"Guk")]
        """

        # Initialize some variables
        face_locations = []
        face_encodings = []
        found=0
        
        folderList={}
        #start a new thread to display images
        #pid=None if app==None else app.pid
        #lock=None if app==None else app.lock
        if app!=None:
            app.newPerson.put("#Start capturing...")
        print('number: {} '.format(len(self.known_encodings)))    
        while found<3:
            print("loop Capturing ...")
            if app!=None:
                if app.exitQueue.qsize()>0:
                    if app.exitQueue.get()=='x':
                        break
            # Grab a single frame of video from the RPi camera as a numpy array
            self.camera.capture(output, format="rgb")
            #time.sleep(1)
            print("Captured")
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(output)
            print("Found {} face(s)".format(len(face_locations)))
            face_encodings = face_recognition.face_encodings(output, face_locations)

            # Loop over each face found in the frame to see if it's someone we know.
            for face_encoding in face_encodings:
                print('comparing')
                # See if the face is a match for the known face(s)
                name = "<Unknown Person>"
                for known_name in selfknown_encodings:
                    known_encoding=self.known_encodings[known_name]
                    match = face_recognition.compare_faces([known_encoding], face_encoding,self.threshold)
                    if match[0]:
                        name=known_name
                        if known_name not in folderList:
                            folderList[known_name]=True
                            if app!=None:
                                #app.lock.acquire()
                                #app.addFolder(known_name)
                                app.newPerson.put(known_name)
                                print(app.newPerson.qsize())
                                #app.lock.release()
                            found+=1
                        break
                        
                print("{} detected!".format(name))
        self.camera.close()
        print("Stop capturing")
        pass
'''
def test(s):
    print(s)
if __name__ =="__main__":
    #p=RecognizeScript(camera=picamera.PiCamera())
    #p=Process(target=run_face_rec, args=(None,))
    #p.start()
    #p.join()
    print(readLastModified())
    #run_face_rec(None)
   
