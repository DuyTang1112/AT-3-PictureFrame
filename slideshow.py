from itertools import cycle
from PIL import Image, ImageTk
import os
import ctypes
import time
#import threading
from customFaceRec import *
from multiprocessing import Process, Lock
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
class SlideShowApp(Process):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, folderList, delay,lock):
        self.folderList=folderList
        self.delay=delay
        self.lock=lock
        Process.__init__(self)
        
        
    def run(self):
        self.lock.acquire()
        self.initialize(self.folderList,self.delay)
        self.lock.release()
    def callback(self):
        self.root.quit()
        
    def initialize(self,folderList,delay):
        #tk.Tk.__init__(self)
        self.root=tk.Tk()
        # set x, y position only
        #self.geometry('+{}+{}'.format(x, y))
        self.root.attributes("-fullscreen", True)
        self.setup(folderList)
        # allows repeat cycling through the pictures
        self.pictures = cycle(ImageTk.PhotoImage(image) for image in self.image_files) if len(self.image_files)!=0 else []
        self.picture_display = tk.Label(self.root)
        self.picture_display.pack()
        self.root.configure(background='black')
        print("resolution:",(self.root.winfo_screenwidth(),self.root.winfo_screenheight()))
        self.show_slides()
        self.root.mainloop()
        self.isstop=False
        
    def show_slides(self):
        '''cycle through the images and show them'''
        # next works with Python26 or higher
        if len(self.image_files)==0:
            return
        img_object= next(self.pictures) 
        self.picture_display.config(image=img_object)
        self.root.after(self.delay, self.show_slides)
        
    def clone(self):
        _clone=SlideShowApp(self.folderList,self.delay,self.lock)
        return _clone
    def stop(self):
        self.root.destroy()
        self.isstop=True
        
    def startSlideShow():
        self.start()
        
    def addFolder(self,folder):
        self.folderList.append(folder)
        #self.setup(self.folderList)
        #self.pictures = cycle(ImageTk.PhotoImage(image) for image in self.image_files)
        
    def setup(self,folderList):
        width,height=self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        self.image_files=[]
        for folder in folderList:
            #folder="Youssef"
            #path and image folder name
            path=os.getcwd()+"/"+folder
            if not os.path.exists(path):
                continue
            #getting the list of file in current directory
            imgFileExtension=("gif","jpg","png","jpeg")
            #imglist=[]
            imgNameList=[files for roots,dirs,files in os.walk(path, topdown=True)][0]
            print("File list: ",imgNameList)

            #check which one is an image
            #imgchecker={file: any(file.lower().endswith(ext) for ext in imgFileExtension) for file in os.listdir()}
            imgchecker={file: file.lower().endswith(imgFileExtension) for file in imgNameList}
            print(imgchecker)
            #add the images to a list
            for file_name in imgchecker:
                if imgchecker[file_name]:
                    subpath=path+"/"+file_name
                    
                    raw_image=Image.open(subpath)
                    iwidth,iheight=raw_image.size
                    scalew=height/iheight
                    #scale the image along the height of the monitor
                    iheight=height
                    iwidth=int(iwidth*scalew)
                    #resizing the image to current resolution
                    self.image_files.append(raw_image.resize((iwidth,iheight), Image.BILINEAR))

#getting current display resolution (Windows)
#user32 = ctypes.windll.user32
#width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

#print(os.listdir())
if __name__ == "__main__":
    # set milliseconds time between slides
    delay = 3000
    print(os.name)
    lock=Lock()
    # upper left corner coordinates of app window
    #x = 100
    #y = 50
    #put the desired image folder in 'alldir' list
    """
    alldir=[]
    for i in os.listdir():
         if os.path.isdir(os.getcwd()+ "/" +i):
             alldir.append(i)
    print(alldir)
    """
    #app = SlideShowApp(["Duy Tang","Youssef"], delay)
    app = SlideShowApp([], delay, lock)
    #app.stop()
    #app.show_slides()
    #app.run()
    run_face_rec(app,delay)#running face recognition will populate the lis of recognizable persons
    app.start()
