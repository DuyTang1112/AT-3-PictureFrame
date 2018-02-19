from PIL import Image
import os, sys
def convert_bytes(num):
     for x in ['bytes','KB','MB','GB','TB']:
          if num<1024.0:
               return num ,x
          num/=1024
#default size=(1024,768)
#resize every images in ../users folder and set the filename to begin like _name
def resizeImage(path=os.getcwd()+"/users", size=(640,480)):
     for f in os.listdir(path):
          if f[0]!="_":
             try :
               filepath=path+"/"+f
               im = Image.open(filepath)
               im.thumbnail(size, Image.ANTIALIAS)
               im.save(path+"/_"+f)
               #num,t= convert_bytes(os.stat(filepath).st_size)
               #im = Image.open(path+"/"+f)
               #im.thumbnail(size, Image.ANTIALIAS)
               #im.save(path+"/__"+f,"JPEG")
               os.remove(filepath)
             except IOError as err:
                 print ("cannot reduce image for ", infile)
                 print(err)


if __name__=="__main__":
    resizeImage()
