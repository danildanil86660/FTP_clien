import ftplib
import json


class FtpClient:
    """
    Class for interaction with FTP server
    """
    _host = ""
    _login = ""
    _password = ""
    _jf = ""
    ftp_client = ""

    def __init__(self):
        self._jf = JsonRead("config.json")
        self._host = self._jf.get_key_value(self._jf.key_list[0])
        self._login = self._jf.get_key_value(self._jf.key_list[1])
        self._password = self._jf.get_key_value(self._jf.key_list[2])
        self.__authorization__()

    def __authorization__(self):
        try:
            self.ftp_client = ftplib.FTP(self._host, self._login, self._password)
            print(self.ftp_client.getwelcome())
        except ftplib.error_perm:
            print("Error")

    def disconnect(self):
        self.ftp_client.close()

    def get_list_directory(self):
        self.ftp_client.dir()

    def write_file_on_server(self, local_directory, server_directory):
        pass

    def ftp_upload(self, path, type = 'txt'):
        my_file = open(path, 'rb')
        name = path.split('/')[-1]
        if type == 'txt':
            self.ftp_client.storlines('STOR ' + name, my_file)
        else:
            self.ftp_client.storbinary('STOR ' + name, my_file)

    def test(self):
        print(self.ftp_client.sendcmd("PWD"))


class JsonRead:
    """
    Class for interacting with JSON files
    """
    _my_json_file = ""
    key_list = []

    def __init__(self, file_name):
        self._my_json_file = open(file_name)
        self._my_json_file = json.load(self._my_json_file)
        self.__get_key_list__()

    def __get_key_list__(self):
        """
        Getting the keys of a JSON file
        """
        for k in self._my_json_file:
            self.key_list.append(k)

    def get_key_value(self, key):
        """
        Return value by key
        """
        return self._my_json_file[key]


ftp = FtpClient()
ftp.ftp_upload("C:/Temp/test1.txt")
ftp.disconnect()
