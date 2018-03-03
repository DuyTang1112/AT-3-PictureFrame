from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton
import shutil
import os, sys
from resizeScript import *
from multiprocessing import Process, Lock, Queue
class At3(QWidget):
    
    def __init__(self):
        super(At3, self).__init__()
        self.initUI()
        self.encodings=None
        
        
    def initUI(self):
        self.setGeometry(10, 10, 800, 400)
        self.setWindowTitle('AT3') 
        

        
        btnAdd = QPushButton('Add ID photos', self)
        btnAdd.resize(btnAdd.sizeHint())
        btnAdd.clicked.connect(self.AddImageID)
        btnAdd.move(300, 50)  

        btnSave = QPushButton('Save', self)
        btnSave.resize(btnSave.sizeHint())
        btnSave.clicked.connect(self.saveFileDialog)
        btnSave.move(300, 200)

        btnRun= QPushButton('Start Slideshow', self)
        btnRun.resize(btnRun.sizeHint())
        btnRun.clicked.connect(self.slideshow)
        btnRun.move(300, 100)  
        
        btnExit = QPushButton('Exit', self)
        btnExit.resize(btnExit.sizeHint())
        btnExit.clicked.connect(self.Exit)
        btnExit.move(300, 300)  

       
        

        self.show()

    def Exit(self):
        exit()

    def slideshow(self):
        if self.encodings==None:
            from slideshow import SlideShowApp
        app = SlideShowApp()
        app.newPerson=Queue()
        app.exitQueue=Queue()
        app.start()
        #from customFaceRec import RecognizeScript
        #s=RecognizeScript(app)
        #s.start()
        #s.join()
        if self.encodings==None:
            import customFaceRec
        p=Process(target=customFaceRec.run_face_rec, args=(app,self.encodings))
        p.start()
        p.join()
        
        #run_face_rec(app) #running face recognition will populate the lis of recognizable persons
        app.join()
        
        #slideshow.main()
        pass
    def AddImageID(self):
        filename,_filter = QFileDialog.getOpenFileNames(self, 'Select image',
                                                       "/media/pi",
                                                      '(*.jpeg *.jpg *.png *.bmp)')
        for filePath in filename:
            #save the file
            dest=os.getcwd()+"/users"
            shutil.copy2(filePath,dest)
        # resize images in ~/users folder    
        resizeImage()

    def saveFileDialog(self):    
        filePaths = QFileDialog.getSaveFileName(self, 'Save File',
                                                       "",
                                                      '*.jpg')
        for filePath in filePaths:
            print('filePath',filePath, '\n')

            file = open(filePath, 'w')
            file.write("~/Desktop/")

    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = At3()
    sys.exit(app.exec_())
