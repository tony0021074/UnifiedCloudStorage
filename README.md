The authorization system of the program is not complete.

For Google drive service, it support log in and out. After log in, a token.json is generated. if you want to log out, delete the token.json file.

For one drive, a client_id(in onedrive_core.py) and a file session.pickle is required.

For Dropbox, a token as string (in dbapi.py) is required. The token can be achieved from user's Dropbox account thought Dropbox official website.