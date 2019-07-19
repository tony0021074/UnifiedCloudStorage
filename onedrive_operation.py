import onedrive_core as odc
import os

class str_operation:

    def __init__(self):
        od = odc.onedrive()
        od.login()
        self.client = od.client
        self.current_location = ['root', 'root']
        self.collection = self.client.item(drive='me', id=self.current_location[-1]).children.get()
        self.dick ={}
        for i in self.client.item(drive='me', id=self.current_location[-1]).children.get():
            self.dick.update({i.name:i.id})

    def get_item(self):
        self.collection = self.client.item(drive='me', id=self.current_location[-1]).children.get()
        self.dick = {}
        for i in self.collection:
            self.dick.update({i.name:i.id})

    def search_all(self):
        print("\n-------------------------------------------------------------------------------------------------------------------------")
        if not self.collection:
            print("No record was found")
        for i in range(len(self.collection)):
            print("index %-2d    %-40s" % (i, self.collection[i].name), end='')
            if self.collection[i].folder is None:
                if self.collection[i].file is not None:
                    print("%-40s   %-5s kb" % (
                    "Type: " + self.collection[i].file.mime_type, self.collection[i].size / 1000))
                else:
                    print("%-15s " % ("Type: Other file"))
            else:
                print("%-15s         Number of files:%-5d " % ("Type: Folder", self.collection[i].folder.child_count))
        print("-------------------------------------------------------------------------------------------------------------------------")


    def upload(self,local_path):
        try:
            name = os.path.basename(local_path)
            self.client.item(drive='me',id=self.current_location[-1]).children[name].upload(local_path)
            # print( self.client.item(drive='me',id=self.current_location[-1]))
        except Exception:
            print("Onedrive: Something wrong with your input. Plz try again.   ")
        else:
            # print("Onedrive upload Completed~")
            self.get_item()

    def download(self,name):
        file_id = self.seach_path(name)
        id_of_file = file_id
        name_of_file = name
        self.client.item(drive='me', id=id_of_file).download('temp/'+name_of_file)
        return 'temp/'+name_of_file

    def seach_path(self,name):
        return self.dick[name]      ##return file id

    def delete(self,name):
        file_id = self.seach_path(name)
        self.client.item(drive='me', id=file_id).delete()
        # print(" onedrive delete completed")
        self.get_item()


    def update(self,local_path):
        name = os.path.basename(local_path)
        file_id = self.seach_path(name)
        self.client.item(drive='me', id=file_id).delete()
        self.upload(local_path)
        # print("Onedirve update successfully")


    def help(self):
        print("___________________________________________________________________________________________________________________")
        print("Commend:\nhelp-----show all commend\nsf-------show files\ngo-------go to other file address\ngb-------go back last file\ndl-------download\ndel------delete\nupl------upload\naf-------add new folder\nrn-------rename file")
        print("mov------move file\ncopy-----copy file\nupd-------update a file")
        print("___________________________________________________________________________________________________________________")



