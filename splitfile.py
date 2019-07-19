# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 13:48:53 2018

@author: TonyY
"""

import os

TEMP_PATH = 'temp/'
DOWNLOAD_PATH = 'download/'

class BreakLoop(Exception):
    pass

def splitFile(filepath, fileno=3):
    
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
    
    filename = os.path.basename(filepath)
    tempfilepath = TEMP_PATH + filename
    
    with open(filepath, 'rb') as rawfile:
        try:
            files = [open(tempfilepath +'.00%d' % i, 'wb') for i in range(fileno)]
            for i, line in enumerate(rawfile):
                files[i % fileno].write(line)
            return [file.name for file in files]
        except IOError:
            print("Unable to create file on disk.")
        finally:
            for f in files:
                f.close()
            
def joinFiles(tempfilepaths):
    
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    
    tempfilepaths.sort()
    filename = os.path.basename(tempfilepaths[0])[0:-4]
    
    with open(DOWNLOAD_PATH + filename, 'wb') as rawfile:
        try:
            files = [open(tempfilepath, 'rb') for tempfilepath in tempfilepaths]
            try:
                while True:
                    for file in files:
                        line = file.readline()
                        if not line:
                            raise BreakLoop()
                        rawfile.write(line)
            except BreakLoop:
                pass
        except IOError:
            print("Unable to create file on disk.")
        finally:
            for file in files:
                file.close()