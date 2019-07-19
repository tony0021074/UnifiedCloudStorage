# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 11:37:25 2018

@author: TonyY
"""

from __future__ import print_function
import io
import os

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors
from apiclient.http import MediaFileUpload, MediaIoBaseDownload

TEMP_PATH = 'temp/'
DOWNLOAD_PATH = 'download/'

IDEOGRAPHIC_SPACE = 0x3000

def buildService():
    
    google_scopes = 'https://www.googleapis.com/auth/drive.appfolder'
    google_crendentials_file = 'google_credentials.json'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(google_crendentials_file, google_scopes)
        creds = tools.run_flow(flow, store)
    global service
    service = build('drive', 'v3', http=creds.authorize(Http()))
    print('Google Drive service built')
    return service

def listFiles(size=20):
    
    try:
        response = service.files().list(spaces='appDataFolder',
                                          fields='nextPageToken, files(id, name, modifiedTime)',
                                          pageSize=40).execute()
        
        items = response.get('files', [])
        if not items:
            print('No files found.')
        else:
            print('Files:')
            length1, length2 = 40, 22
            template = "{fileName:"+str(length1)+"}{lastModified:"+str(length2)+"}"
            print(template.format(fileName="File Name", lastModified="Last Modified"))
            for item in items:
                i=0
                for char in item['name']:
                    if ord(char) > 10000:
                        i += 1
                name = item['name'][:-4]
                modifiedtime=item['modifiedTime'][:10]+" "+item['modifiedTime'][11:-5]
                template = "{fileName:"+str(length1-i)+"}{lastModified:"+str(length2)+"}"
                print(template.format(fileName=name, 
                                      lastModified=modifiedtime))
                
    except errors.HttpError as err:
        print (f'An error occurred: {err}')
            
def uploadFile(tempfilepath):
    
    filepath = tempfilepath
    filename = os.path.basename(filepath)
    
    file_metadata = {'name': filename,
                     'parents': ['appDataFolder']}
    
    media = MediaFileUpload(filepath,
                            resumable=True)
    
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    # print('File ID: %s' % file.get('id'))
    # print('Google Drive Upload done')

def downloadFile(filename):
    
    items = searchFiles(filename, size=1)
    if items:
        file_id = items[0]['id']
     
        file = service.files().get(fileId=file_id).execute()
        filename = file['name']
        
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            #print ("Download %d%%." % int(status.progress() * 100))
        with io.open(TEMP_PATH + filename,'wb') as f:
            fh.seek(0)
            f.write(fh.read())
        # print('Google Drive Download done')
        return f.name

def updateFile(filepath, new_revision = True):
    
    filename = os.path.basename(filepath)

    items = searchFiles(filename, size=1)
    if items:
        file_id = items[0]['id']
        
        try:
            # File's new content.
            media_body = MediaFileUpload(
                    filepath, resumable=True)
        
            # Send the request to the API.
            updated_file = service.files().update(
                    fileId=file_id,
                    media_body=media_body).execute()
            # print('File ID: %s' % updated_file.get('id'))
            # print('Google Drive Update done')
        except errors.HttpError as err:
            print (f'An error occurred: {err}')
    
def deleteFile(filename):
    
    items = searchFiles(filename, size=1)
    if items:
        file_id = items[0]['id']
        try:
            service.files().delete(fileId=file_id).execute()
            # print('Google Drive Delete done')
        except errors.HttpError as err:
            print (f'An error occurred: {err}')
        
def searchFiles(filename, size=40, mode = '='):
    
    query = "name " + mode + " '" + filename + "'"
    
    try:
        results = service.files().list(spaces='appDataFolder',
        pageSize=size,fields="nextPageToken, files(id, name, modifiedTime)",q=query).execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
            return None
        else:
            if mode == '=':
                return items
            elif mode == 'contains':
                print('Files:')
                length1, length2 = 40, 22
                template = "{fileName:"+str(length1)+"}{lastModified:"+str(length2)+"}"
                print(template.format(fileName="File Name", lastModified="Last Modified"))
                for item in items:
                    i=0
                    for char in item['name']:
                        if ord(char) > 10000:
                            i += 1
                    name = item['name'][:-4]
                    modifiedtime=item['modifiedTime'][:10]+" "+item['modifiedTime'][11:-5]
                    template = "{fileName:"+str(length1-i)+"}{lastModified:"+str(length2)+"}"
                    print(template.format(fileName=name, 
                                          lastModified=modifiedtime))
                return items
            
    except errors.HttpError as err:
        print (f'An error occurred: {err}')
        return None
    
def quota():
  """Print information about the user along with the Drive API settings.

  Args:
    service: Drive API service instance.
  """
  try:
    about = service.about().get(fields="storageQuota").execute()
    
    return about["limit"], about["usage"]
  except errors.HttpError as err:
    print('An error occurred: %s' % err)
    return None