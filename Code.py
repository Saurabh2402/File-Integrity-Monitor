import glob
import hashlib
import os
import tkinter as tk
import customtkinter as ctk
from tkinter.filedialog import askdirectory


baselines = r"C:\Users\DELL\Desktop\Baselines"#Baseline.txt will be at this specified path
secure_path = ""

name_hash=""
baseline_path=""

#Calculate hash of a file 
def CalculateSha512Hash(file_name):
    # BUF_SIZE is totally arbitrary, change as per your requirement
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha = hashlib.sha512()
    
    with open(file_name,'rb') as file:
        while True:
            data = file.read(BUF_SIZE)
            if not data:
                break
            sha.update(data)
            # print("SHA: {0}".format(sha.hexdigest()))
        return sha.hexdigest()
    
def CalculateNameHash(filename):
    md5 = hashlib.md5()
    md5.update(filename.encode())
    return md5.hexdigest()

def UpdateBaseline(dir,mode):
    if dir=="":
        print("Folder not selected")
        label3.configure(text="Error : Folder not selected")

    elif os.path.isdir(baselines)==False:
        print("Baselines Folder doesn't exists,so creating it")
        label3.configure(text="Message : Baselines Folder doesn't exists, so creating it")
        os.makedirs(baselines)
        print("Updating Baseline...")
        label3.configure(text="Message : Updating Baseline...")
        UpdateBaselineHelper(dir,mode)
        print("Updated Baseline Successfully")
        label3.configure(text="Message : Updated Baseline Successfully")
        
    

    else:
        print("Updating Baseline...")
        label3.configure(text="Message : Updating Baseline...")
        UpdateBaselineHelper(dir,mode)
        print("Updated Baseline Successfully")
        label3.configure(text="Message : Updated Baseline Successfully")


#Update Baseline Helper for [files in a folder] and [files in subfolders]
def UpdateBaselineHelper(dir,mode):
    
    global name_hash,baseline_path
    if(mode=='w'):
        name_hash = CalculateNameHash(dir)
        #print("Update:namehash:*"+name_hash+"*")
        baseline_path = os.path.join(baselines,(name_hash+'.txt'))
    
    #print("path: ",baseline_path)
    files = [os.path.abspath(f) for f in glob.glob(os.path.join(dir,'*')) if os.path.isfile(f)]
    with open(baseline_path,mode) as baseline:
        for f in files:
            hash = CalculateSha512Hash(os.path.join(dir,f))
            baseline.write(f)
            baseline.write("=")
            baseline.write(str(hash))
            baseline.write("\n")
        # print("Updated Baseline")
    
    directories = [d for d in glob.glob(os.path.join(dir,'*')) if os.path.isdir(d)]
    for d in directories:
        UpdateBaselineHelper(d,'a')
        
#Returns dictionary containing keys as file name and values as their hashes
def getKeyHashesFromBaseline():
    global name_hash,baseline_path
    dict = {}

    try:
        with open(baseline_path,'r') as baseline:
            for line in baseline:
                key,value = line.split('=')
                dict[key] = value[:-1]
    except IOError:
        print('Baseline file not present for getting hashes')
    return dict

#Calculates hashes and Checks with the baseline
def CheckIntegrity(dir,number):
    if dir=="":
        print("Folder not selected")
        label3.configure(text="Error : Folder not selected")

    else:
        CheckIntegrityHelper(dir,number)

def CheckIntegrityHelper(dir,number):
    global name_hash,baseline_path

    if(number):
        name_hash = CalculateNameHash(dir)
        #print("*Integrity:namehash:"+name_hash+'*')
        baseline_path = os.path.join(baselines,(name_hash+'.txt'))
        try:
            with open(baseline_path,'r') as baseline:
                random=99
        except IOError:
            print('Baseline file for specified folder not present')
            label3.configure(text='Error : Baseline file for specified folder not present')
            return
        print("Files changed : ")
        label3.configure(text='Files Changed : ')
    
    files = [os.path.abspath(f) for f in glob.glob(os.path.join(dir,'*')) if os.path.isfile(f)]
    dict = getKeyHashesFromBaseline()
    #print(dict)
    #print(files)
    
    for f in files:
        temp_hash = CalculateSha512Hash(os.path.join(dir,f))
        if(temp_hash!=dict[f]):
            label3.configure(text= label3.text+"\n"+os.path.abspath(f).replace(os.path.abspath(folder),"."))

    directories = [d for d in glob.glob(os.path.join(dir,'*')) if os.path.isdir(d)]
    for d in directories:
        CheckIntegrity(d,0)



ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

#Some Variables
font_data = ("Raleway",16)
label_text_clr = "#FFCF00"
btn_fg_clr = "#27ab55"
btn_text_clr = "#000000"
btn_hover_clr = "#148f3f"
error_label_clr = "#E94F37"

folder=""

#initialising root window
root = ctk.CTk()
root.title("  File Integrity Monitor")
root.geometry("600x500")
# root.geometry("")
root.resizable(False,True)
root.wm_iconphoto(False,tk.PhotoImage(file="images/windowicon1.png"))

#label1 : Monitor folder 
label1 = ctk.CTkLabel(master=root,
                      text="Select a Folder",
                      text_font=font_data,
                      text_color=label_text_clr)
label1.place(relx=0.35,rely=0.15,anchor=tk.CENTER)

#browse button


def open_file():
    label3.configure(text="Message : ")
    label2.configure(text="(Selected Folder path will appear here)")
    global folder
    folder = askdirectory(parent=root, title="Choose a folder")
    if folder:
        label3.configure(text="Message : Folder Selected Successfully")
        label2.config(text=folder)

browse_btn = ctk.CTkButton( master=root,
                            text="Browse",
                            image=tk.PhotoImage(file="images/browse.png").subsample(8,8), 
                            compound=ctk.RIGHT,
                            command=open_file,
                            fg_color=btn_fg_clr,
                            text_color=btn_text_clr,
                            text_font=font_data,
                            hover_color=btn_hover_clr,
                            height=40,
                            width=125 )
browse_btn.place(relx=0.7,rely=0.15, anchor=tk.CENTER)

#Label2 : Selected Folder Path
label2 = ctk.CTkLabel(master=root,
                      text="(Selected Folder path will appear here)",
                      wraplength=500,
                      text_font=font_data,
                      text_color=label_text_clr)
# label2.configure(text="Select a folder")
label2.place(relx=0.5,rely=0.37,anchor=tk.CENTER)


#Button : Update Baseline
update_baseline_btn = ctk.CTkButton( master=root,
                                     text="Update Baseline ", 
                                     image=tk.PhotoImage(file="images/updatebaseline.png").subsample(15,15), 
                                     compound=ctk.RIGHT,
                                     command=lambda:UpdateBaseline(folder,'w'),
                                     fg_color=btn_fg_clr,
                                     text_color=btn_text_clr,
                                     text_font=font_data,
                                     hover_color=btn_hover_clr,
                                     height=40,
                                     width=150 )
update_baseline_btn.place(relx=0.5, rely=0.57, anchor=tk.CENTER)


#Button : Check Integrity
check_integrity_btn = ctk.CTkButton( master=root,
                                     text="Check Integrity", 
                                     image=tk.PhotoImage(file="images/checkintegrity.png").subsample(7,7), 
                                     compound=ctk.RIGHT,
                                     command=lambda:CheckIntegrity(folder,1),
                                     fg_color=btn_fg_clr,
                                     text_color=btn_text_clr,
                                     text_font=font_data,
                                     hover_color=btn_hover_clr,
                                     height=40,
                                     width=125 )
check_integrity_btn.place(relx=0.5, rely=0.75, anchor=tk.CENTER)


#label3 : Message Label
label3 = ctk.CTkLabel( master=root,
                       text="Message : ",
                       text_font=font_data,
                       text_color=error_label_clr)
# label3.configure(text="Error : "+"No error") #configure is used to change text and other attributes
label3.pack(fill="both", expand=True)
label3.place(relx=0.5,rely=0.90,anchor=tk.CENTER)


root.mainloop()
