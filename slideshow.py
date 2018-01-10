from itertools import cycle
from PIL import Image, ImageTk
import os
import ctypes
import time

try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
class SlideShowApp(tk.Tk):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, folderList, delay):
        # the root will be self
        tk.Tk.__init__(self)
        # set x, y position only
        #self.geometry('+{}+{}'.format(x, y))
        self.attributes("-fullscreen", True)
        self.delay = delay
        self.setup(folderList)
        # allows repeat cycling through the pictures
        self.pictures = cycle(ImageTk.PhotoImage(image) for image in self.image_files)
        self.picture_display = tk.Label(self)
        self.picture_display.pack()
        self.configure(background='black')
        print("resolution:",(self.winfo_screenwidth(),self.winfo_screenheight()))
    def show_slides(self):
        '''cycle through the images and show them'''
        # next works with Python26 or higher
        img_object= next(self.pictures)
        self.picture_display.config(image=img_object)
        self.after(self.delay, self.show_slides)
    def run(self):
        self.mainloop()

    def setup(self,folderList):
        width,height=self.winfo_screenwidth(),self.winfo_screenheight()
        self.image_files=[]
        for folder in folderList:
            #folder="Youssef"
            #path and image folder name
            path=''
            if os.name=="nt":
                path=os.getcwd()+"\\"+folder
            elif os.name=='posix':
                path=os.getcwd()+"/"+folder

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
                    subpath=''
                    if os.name=='nt':
                        subpath=path+"\\"+file_name
                    elif os.name=='posix':
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
    # upper left corner coordinates of app window
    #x = 100
    #y = 50
    #put the desired image folder in 'alldir' list
    alldir=[]
    for i in os.listdir():
         if os.path.isdir(os.getcwd()+"\\"+i):
             alldir.append(i)
    print(alldir)
    #app = SlideShowApp(["Duy Tang","Youssef"], delay)
    app = SlideShowApp(alldir, delay)
    app.show_slides()
    app.run()
