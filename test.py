
#file chooser GUI
def chooseFile():
    import tkinter
    from tkinter.filedialog import askopenfilename

    tkinter.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filepath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filepath)

if __name__=="__main__":
    #chooseFile()
    sendmsg('Hello')
