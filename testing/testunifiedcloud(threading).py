# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 08:27:04 2018

@author: TonyY
"""

import googledrive
import dbapi
import onedrive_operation as onedrive
import splitfile

import os
import time
from datetime import timedelta
import queue
from threading import Thread

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
        
        threads = []
        threads.append(Thread(googledrive.uploadFile(tempfilepaths[0])))
        threads.append(Thread(dbapi.UploadFile(file=tempfilepaths[1])))
        threads.append(Thread(od.upload(tempfilepaths[2])))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
            
        end_time = time.monotonic()
        timings["Upload Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        for tempfilepath in tempfilepaths:
            os.remove(tempfilepath)
        
        #Download
        
        start_time = time.monotonic()
        
        que = queue.Queue()
        threads = []
        threads.append(Thread(target=lambda q: q.put(googledrive.downloadFile(filename+'.000')),args=(que,)))
        threads.append(Thread(target=lambda q: q.put(dbapi.DownloadFile(file=filename+'.001')),args=(que,)))
        threads.append(Thread(target=lambda q: q.put(od.download(filename+'.002')),args=(que,)))
        for thread in threads:
            thread.start() 
        for thread in threads:
            thread.join()
            
        end_time = time.monotonic()
        timings["Download Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        tempfilepaths =[]
        while not que.empty():
            tempfilepaths.append(que.get())
            
        #Join
        start_time = time.monotonic()
        splitfile.joinFiles(tempfilepaths)
        end_time = time.monotonic()
        timings["Joining Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        with que.mutex:
            que.queue.clear()
        for tempfilepath in tempfilepaths:
            os.remove(tempfilepath)
            
        threads = []
        threads.append(Thread(googledrive.deleteFile(filename+'.000')))
        threads.append(Thread(dbapi.DeleteFile(file=filename+'.001')))
        threads.append(Thread(od.delete(filename+'.002')))
        for thread in threads:
            thread.start() 
        for thread in threads:
            thread.join()
    
    print(str(timings))
    
if __name__ == '__main__':
    main()