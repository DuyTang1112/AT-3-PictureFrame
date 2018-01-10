
# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import os


def run_face_rec(app,delay):
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
    print(path)
    imgFileExt=("gif","jpg","jpeg","png")
    filelist=[files for r,dirs,files in os.walk(path,topdown=True)][0] #get the list of all files
    imgList=[]
    for file in filelist:
        if file.lower().endswith(imgFileExt):
            imgList.append(file)
    
    known_encodings=[]
    for filename in imgList:
        person=filename[:filename.find(".")]
        print("Loading sample face from "+person)
        face_encoding=face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+filename))[0]
        known_encodings.append((face_encoding,person))
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
    found_3=0
    
    folderList={}
    #start a new thread to display images
    #pid=None if app==None else app.pid
    #lock=None if app==None else app.lock
    while found_3!=3:
        print("Capturing image.")
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="rgb")

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} faces in image.".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)

        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = "<Unknown Person>"
            for known_encoding,known_name in known_encodings:
                match = face_recognition.compare_faces([known_encoding], face_encoding,threshold)
                
                if match[0]:
                    name=known_name
                    if known_name not in folderList:
                        folderList[known_name]=True
                        if app!=None:
                            app.addFolder(known_name)
                    found_3+=1         
                    
            print("I see someone named {}!".format(name))
    camera.close()
    
if __name__ =="__main__":
    run_face_rec(None,None)
   
