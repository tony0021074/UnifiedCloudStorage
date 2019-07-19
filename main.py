# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 21:52:40 2018

@author: TonyY
"""

import googledrive
import dbapi
import onedrive_operation as onedrive
import splitfile

import os
import queue
from threading import Thread

from tkinter import Tk
from tkinter.filedialog import askopenfilename

def main():
    
    googledrive.buildService()
    dbapi.Login()
    od = onedrive.str_operation()
    isRunning = True
    try:
        while isRunning:
            
                action = input('list, search, upload, ' + 
                               'download, update, delete, exit: ')
            
                if action == 'list':
                    
                    googledrive.listFiles()  
                    #dbapi.ShowFiles()
                    #od.search_all()
                    
                elif action == 'search':
    
                    filename = input('enter file name: ')
                    
                    if filename == '':
                        print('please enter a file name')
                        continue
                    
                    googledrive.searchFiles(filename=filename, mode = 'contains')
                    #dbapi.SearchFile(file=filename)
                    
                elif action == 'upload':
                    try:
                        root = Tk()
                        root.withdraw
                        filepath = askopenfilename(initialdir = 'upload/')
                        filename = os.path.basename(filepath)
                        root.destroy()
                        
                        if filepath == '':
                            continue
                        
                        tempfilepaths = splitfile.splitFile(filepath)
                        
                        threads = []
                        threads.append(Thread(googledrive.uploadFile(tempfilepaths[0])))
                        threads.append(Thread(dbapi.UploadFile(file=tempfilepaths[1])))
                        threads.append(Thread(od.upload(tempfilepaths[2])))
                        for thread in threads:
                            thread.start()
                        for thread in threads:
                            thread.join()
                        print("Upload " + filename +" successfully")
                        
                        for tempfilepath in tempfilepaths:
                            os.remove(tempfilepath)
                    except:
                        print ('Upload Failed.')
                                    
                elif action == 'download':
                    try:
                        filename = input('enter file name: ')
                        
                        que = queue.Queue()
                        threads = []
                        threads.append(Thread(target=lambda q: q.put(googledrive.downloadFile(filename+'.000')),args=(que,)))
                        threads.append(Thread(target=lambda q: q.put(dbapi.DownloadFile(file=filename+'.001')),args=(que,)))
                        threads.append(Thread(target=lambda q: q.put(od.download(filename+'.002')),args=(que,)))
                        for thread in threads:
                            thread.start() 
                        for thread in threads:
                            thread.join()
                        print("Download " + filename +" successfully")
                        tempfilepaths =[]
                        while not que.empty():
                            tempfilepaths.append(que.get())
                        splitfile.joinFiles(tempfilepaths)
                        
                        with que.mutex:
                            que.queue.clear()
                        for tempfilepath in tempfilepaths:
                            os.remove(tempfilepath)
                    except:
                        print ('Download Failed.')
                    
                elif action == 'delete':
                    
                    filename = input('enter file name: ')
                    
                    threads = []
                    threads.append(Thread(googledrive.deleteFile(filename+'.000')))
                    threads.append(Thread(dbapi.DeleteFile(file=filename+'.001')))
                    threads.append(Thread(od.delete(filename+'.002')))
                    for thread in threads:
                        thread.start() 
                    for thread in threads:
                        thread.join()
                    print("Delete " + filename + " successfully")
                
                elif action == 'update':
                    
                    root = Tk()
                    root.withdraw
                    filepath = askopenfilename(initialdir = 'upload/')
                    filename = os.path.basename(filepath)
                    root.destroy()
                    
                    if not filepath:
                        continue
                    
                    tempfilepaths = splitfile.splitFile(filepath)
                    
                    threads = []
                    threads.append(Thread(googledrive.updateFile(filepath = tempfilepaths[0])))
                    threads.append(Thread(dbapi.UploadFile(file=tempfilepaths[1])))
                    threads.append(Thread(od.update(tempfilepaths[2])))
                    for thread in threads:
                        thread.start() 
                    for thread in threads:
                        thread.join()
                    print("Update " + filename + " successfully")
                    
                    for tempfilepath in tempfilepaths:
                            os.remove(tempfilepath)
                
                elif action == 'exit':
                    print ('Exiting the program')
                    isRunning = False
                
                else:
                    
                    print('ONLY support list, search, upload,' + 
                               'download, update, delete& exit')
    except:
        print ('An error occured.')
    
if __name__ == '__main__':
    main()