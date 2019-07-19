# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 08:37:03 2018

@author: TonyY
"""

import googledrive
import dbapi
import onedrive_operation as onedrive
import splitfile

import os
import time
from datetime import timedelta

from tkinter import Tk
from tkinter.filedialog import askopenfilename


def main():
    
    googledrive.buildService()
    dbapi.Login()
    od = onedrive.str_operation()
    
    root = Tk()
    root.withdraw
    filepath = askopenfilename(initialdir = 'upload/')
    root.destroy()
    filename = os.path.basename(filepath)
    
    timings={"Upload Time":[],"Download Time":[],"Splitting Time":[],"Joining Time":[]}
    
    for i in range(5):    
        
        #Split
        start_time = time.monotonic()
        tempfilepaths = splitfile.splitFile(filepath)
        end_time = time.monotonic()
        timings["Splitting Time"].append(str(timedelta(seconds=end_time - start_time)))
             
        #Upload
        start_time = time.monotonic()
        
        googledrive.uploadFile(tempfilepaths[0])
        dbapi.UploadFile(file=tempfilepaths[1])
        od.upload(tempfilepaths[2])
            
        end_time = time.monotonic()
        timings["Upload Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        for tempfilepath in tempfilepaths:
            os.remove(tempfilepath)
        
        #Download
        start_time = time.monotonic()
        
        tempfilepaths =[]
        tempfilepaths.append(googledrive.downloadFile(filename+'.000'))
        tempfilepaths.append(dbapi.DownloadFile(file=filename+'.001'))
        tempfilepaths.append(od.download(filename+'.002'))
        
        end_time = time.monotonic()
        timings["Download Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        #Join
        start_time = time.monotonic()
        splitfile.joinFiles(tempfilepaths)
        end_time = time.monotonic()
        timings["Joining Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        for tempfilepath in tempfilepaths:
            os.remove(tempfilepath)
            
        googledrive.deleteFile(filename+'.000')
        dbapi.DeleteFile(file=filename+'.001')
        od.delete(filename+'.002')
    
    print(str(timings))
    
if __name__ == '__main__':
    main()