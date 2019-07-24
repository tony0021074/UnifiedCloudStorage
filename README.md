# Unified Cloud Storage (School group project)

*not runnable

Group project aims to create an application to store file in 3 cloud locations. Only googledrive.py, splitfile.py & main.py is written by me. Others are written by teammates.

The file is split into 3 parts. They are sent to google drive, OneDrive and Dropbox.


The programe shall not work now. There are some problems in the coding.

The authorization system of the program is not complete.

For Google drive service, it support log in and out. After log in, a token.json is generated. if you want to log out, delete the token.json file.

For one drive, a client_id(in onedrive_core.py) and a file session.pickle is required.

For Dropbox, a token as string (in dbapi.py) is required. The token can be achieved from user's Dropbox account thought Dropbox official website.
