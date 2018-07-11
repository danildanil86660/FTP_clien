import ftplib
import json


class FtpClient:
    """
    Class for interaction with FTP server
    """
    _host = ""
    _login = ""
    _password = ""
    ftp_client = ""

    def __init__(self, host, login, password):
        self._host = host
        self._login = login
        self._password = password

    def authorization(self):
        try:
            self.ftp_client = ftplib.FTP(self._host, self._login, self._password)
            print(self.ftp_client.getwelcome())
        except ftplib.error_perm:
            print("Error")

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
        for k in self._my_json_file:
            self.key_list.append(k)

    def get_key_value(self, key):
        return self._my_json_file[key]


"""
host = '93.189.41.9'
ftp_user = 'user54015'
ftp_password = 'EZjb3lRIo1Av'

ftp = FtpClient(host, ftp_user, ftp_password)
ftp.authorization()
ftp.test()

JF = JsonRead("config.json")
a = JF.key_list
print(JF.get_key_value(a[0]))
"""
