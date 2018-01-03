import tkinter
from PIL import Image, ImageTk
import os
import ctypes
import time
#getting current display resolution (Windows)
user32 = ctypes.windll.user32
width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

#getting the list of file in current directory
imgFileExtension={"gif","jpg","png"}
imglist=[]
#check which one is an image
imgchecker={file: any(file.lower().endswith(ext) for ext in imgFileExtension) for file in os.listdir()}
print(imgchecker)
#add the images to a list
for file_name in imgchecker:
    if imgchecker[file_name]:
        path=os.getcwd()+"\\"+file_name
        raw_image=Image.open(path)
        #resizing the image to current resolution
        imglist.append(raw_image.resize((width, height), Image.BILINEAR))


root = tkinter.Tk()
root.attributes("-fullscreen", True)
i=0

#convert to a gif
img = ImageTk.PhotoImage(imglist[0])
panel = tkinter.Label(root, image = img)
panel.pack(side = "bottom", fill = tkinter.BOTH, expand = 1)
def showSlides():
    global i
    global panel
    i=(i+1)%len(imglist)
    img = ImageTk.PhotoImage(imglist[i])
    panel.config(image=img)
root.after(3000,showSlides)

root.mainloop()
