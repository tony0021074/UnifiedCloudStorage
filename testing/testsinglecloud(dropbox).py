# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 08:37:03 2018

@author: TonyY
"""

import dbapi

import os
import time
from datetime import timedelta

from tkinter import Tk
from tkinter.filedialog import askopenfilename


def main():
    
    dbapi.Login()
    
    root = Tk()
    root.withdraw
    filepath = askopenfilename(initialdir = 'upload/')
    root.destroy()
    filename = os.path.basename(filepath)
    
    timings={"Upload Time":[],"Download Time":[]}
    
    for i in range(5):
        #Upload
        
        start_time = time.monotonic()
        
        dbapi.UploadFile(filepath)
            
        end_time = time.monotonic()
        timings["Upload Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        
        #Download
        
        start_time = time.monotonic()
        
        dbapi.DownloadFile(file=filename)
        
        end_time = time.monotonic()
        timings["Download Time"].append(str(timedelta(seconds=end_time - start_time)))
        
        dbapi.DeleteFile(file=filename)
        
    print(str(timings))
    
if __name__ == '__main__':
    main()