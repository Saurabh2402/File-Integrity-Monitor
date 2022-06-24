# HashLine - A File Integrity Monitor
![This is an image](https://github.com/Saurabh2402/File-Integrity-Monitor/blob/master/Project%20Images/3_Integrity_Checked_Results.png)


A File Integrity Monitor is a software that performs the act of validating the integrity of operating system and application software files using a verification method between the current file state and a known good state also called `Baseline`.

I have developed a File Integrity Monitoring Solution named - **`HashLine - A File Integrity Monitor`**

HashLine can be used to **detect whether tampering is done with a directory and files inside**.

HashLine is developed in Python and is only suited for Windows Operating System.

### Modules Used in Implementation : 
- `OS module` : This module is used for interacting with the file system tree.
- `Hashlib module` : SHA512 function is used from this module.
- `tkinter module` : This module helped in making the GUI more presentable.



## HashLine performs 3 functions : 

1. **`Browsing a Directory`** :  When clicked on the 'Browse' button, HashLine prompts a window that allows the users to select a directory.

2. **`Updating Baseline`** : When clicked on the 'Update Baseline', 
                          HashLine first checks whether a directory was selected through the 'Browse' button, 
                          if not then a message saying - "Directory not selected" is prompted, 
                          else a baseline file is created/updated for the browsed directory. Baseline stores paths of all the files in the directory and 
                          calculates SHA512 hash from the respective files contents and stores in the following format :

      - FilePath1 = Hash1
  
      - FilePath2 = Hash2
  
      - FilePath3 = Hash3
      
 Example -
  ```
   C:\Users\DELL\Desktop\Files\document1.docx = cbe4dc256c176d915eb037936863a841675f93225c279fad6954cd0d72f5d279c66fcbcd314e9e5dc90cdbcb131d92bce78ae7dfa2160f8920d0b967af2b7030
  ```
  
 3. **`Checking Integrity`** : When clicked on the 'Check Integrity' button,
                         HashLine first checks whether a directory was selected through the Browse button, 
                         if not then a message saying - "Directory not selected" is prompted,
                         But if selection was done, 
                          then, it checks whether baseline for selected directory exists or not. 
                          If baseline exists, it then cross checks with the baseline and tells the files in which data was changed. It also tells which files were added and removed after the last update of baseline.
                          But if baseline doesn't exists, then it displays an error message saying- "Baseline file not present".
                          (NOTE : Baseline file is necessary for comparison of file's present content to a known trusted state.)
 
 ## Key Features about HashLine : 
 
 - HashLine uses the idea of comparing the file’s current state hash with the hash stored in the established baseline. 
 - HashLine is capable of monitoring all types of files viz. .doc, .txt, .rtf, .ppt, .xlxs
 - When a directory is being monitored, HashLine works fine with subdirectories i.e.
    -  It updates baseline with files in subdirectories.
    -  Also checks integrity of files in subdirectories.
 - HashLine can also check integrity of different directories, as separate baseline is maintained for each directory.
