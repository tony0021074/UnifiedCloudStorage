# -*- coding: utf-8 -*-
import dropbox
import os

#log in to the dropbox
#parameter    dbx:  used to use other function below
def Login():
    MYACCESSTOKEN='' #user's Dropbox token
    global dbx
    dbx = dropbox.Dropbox(MYACCESSTOKEN)
    print('Dropbox service built')
    return dbx

#show file in the folder	
def ShowFiles(path='/unified/'):
	try:
		for entry in dbx.files_list_folder(path).entries:
			print(entry.name)
	except dropbox.exceptions.ApiError:
		print('Dropbox Search failed!')

#upload file depening on filename		
def UploadFile(file,path='/unified/'):
	try:
		with open(file, 'rb') as rawfile:
			s=rawfile.read();
		dbx.files_upload(s,path+os.path.basename(file),mode=dropbox.files.WriteMode('overwrite',None),autorename=True)
	except dropbox.exceptions.ApiError:
		print('Dropbox Upload failed!')

#download file depening on filename
def DownloadFile(file,path='/unified/'):
	try:
		dbx.files_download_to_file('temp/'+file, path+file, rev=None)
		return 'temp/'+file
	except dropbox.exceptions.ApiError:
		print('Dropbox Download failed!')

#delete file depening on filename	
def DeleteFile(file,path='/unified/'):
	try:
		dbx.files_delete(path+file)
	except dropbox.exceptions.ApiError:
		print('Dropbox Delete failed!')

#search file depending on filename	
def SearchFile(file,path='/unified/'):
	try:
		files=[]
		for i in dbx.files_search(path,file).matches:
			files.append(i.metadata.path_display);
#		print(files)
		return(files)
	except dropbox.exceptions.ApiError:
		print('Dropbox Search failed!')
		
#show the memmory dropbox allocated
def ShowStorage():
	return dbx.users_get_space_usage().allocation.get_individual().allocated

#show the memory cloud has used	
def ShowUsage():
	return dbx.users_get_space_usage().used

