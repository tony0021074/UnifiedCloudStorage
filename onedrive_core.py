import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer


class onedrive:

    def __init__(self):
        self.client_id = '' #user's onedrive id
        self.client_secret = 'ybrqeYJVS547%^efEGT63@?' #Application secret
        self.scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
        self.api_base_url = 'https://api.onedrive.com/v1.0/'
        self.redirect_uri = 'http://localhost:8000/tutorial/callback'
        self.code = 'cb115df3-9e62-4cb3-8181-f17afcac737d'
        self.client = None                                  #操作對象（實例）
        # self.current_location = ['root','root']


    def login(self):
        http_provider = onedrivesdk.HttpProvider()
        client = onedrivesdk.get_default_client(
            client_id=self.client_id, scopes=self.scopes)

        auth_provider = onedrivesdk.AuthProvider(
            http_provider=http_provider,
            client_id=self.client_id,
            scopes=self.scopes)

        if client is not None:
            auth_provider.load_session()
            auth_provider.refresh_token()
            client = onedrivesdk.OneDriveClient(self.api_base_url, auth_provider, http_provider)
            self.client = client

        else:
            auth_url = client.auth_provider.get_auth_url(self.redirect_uri)
            code = GetAuthCodeServer.get_auth_code(auth_url, self.redirect_uri)
            auth_provider.authenticate(code, self.redirect_uri, self.client_secret)
            # Save the session for later
            auth_provider.save_session()
            client = onedrivesdk.OneDriveClient(self.api_base_url, auth_provider, http_provider)
            self.client = client
            
        print("OneDrive service built")



