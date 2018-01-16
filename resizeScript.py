from PIL import Image
import os, sys

def resizeImage(inpath,infile, output_dir="", size=(1024,768)):
     outfile = os.path.splitext(infile)[0]+"_resized"
     extension = os.path.splitext(infile)[1]
     print(path+"/"+infile)
     if (not extension.lower().endswith(('.jpg','.png','.jpeg')) ):
        return

     if infile != outfile:
        try :
            im = Image.open(path+"/"+infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(output_dir+"/"+outfile+extension,"JPEG")
        except IOError as err:
            print ("cannot reduce image for ", infile)
            print(err)


if __name__=="__main__":
    output_dir = "resized"
    path = os.getcwd()+"/users"

    if not os.path.exists(os.path.join(os.getcwd(),output_dir)):
        os.mkdir(output_dir)

    for f in os.listdir(path):
        resizeImage(path,f,output_dir)
