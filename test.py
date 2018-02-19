import os
#file chooser GUI. Point to external device directory and ask to inport an image
def chooseFile(multi=True):
    import tkinter
    from tkinter.filedialog import askopenfilenames,askopenfilename
    print(os.getcwd())
    path="/media/pi";
    root=tkinter.Tk() # we don't want a full GUI, so keep the root window from appearing
    root.withdraw()
    # show an "Open" dialog box and return the path to the selected file
    if multi:
        filepath = askopenfilenames(parent=root,initialdir=path,title="Select Images",filetypes=(("Image Files","*.jpeg;*.png"), ("All",".")) )
    else:
        filepath = askopenfilename(parent=root,initialdir=path,title="Select Images",filetypes=(("Image Files","*.jpeg;*.png"), ("All",".")) )
    filepath=root.tk.splitlist(filepath)
    return filepath

if __name__=="__main__":
    #chooseFile()
    print(chooseFile())
