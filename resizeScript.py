from PIL import Image
import os, sys

def resizeImage(path=os.getcwd()+"/users", size=(1024,768)):
     for f in os.listdir(path):
          if f[0]!="_":
             try :
                 im = Image.open(path+"/"+f)
                 im.thumbnail(size, Image.ANTIALIAS)
                 im.save(path+"/_"+f,"JPEG")
             except IOError as err:
                 print ("cannot reduce image for ", infile)
                 print(err)


if __name__=="__main__":
    resizeImage()
