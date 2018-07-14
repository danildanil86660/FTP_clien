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
            print("Вы авторизованы", self._login)
        except ftplib.error_perm:
            print("Error")

    def disconnect(self):
        try:
            self.ftp_client.close()
        except:
            print('Error disconnect')

    def get_list_directory(self):
        self.ftp_client.dir()

    def __ftp_upload__(self, path):
        name = path.split('/')[-1]
        type = name.split('.')[-1]
        try:
            my_file = open(path, 'rb')
        except FileNotFoundError:
            print("File ", name, " not found")
            exit()

        if type == 'txt':
            self.ftp_client.storlines('STOR ' + name, my_file)
        else:
            self.ftp_client.storbinary('STOR ' + name, my_file)

    def __check_directory_on_server__(self, patch):
        """
        Verification is in progress. Are there necessary directories
        :param patch -> str:
        """
        flagA = 0
        dir_list = patch.split('/')
        for my_dir in dir_list:
            old_dir_list = self.ftp_client.nlst()
            for old in old_dir_list:
                if old == my_dir:
                    self.ftp_client.sendcmd('CWD ' + my_dir)
                    flagA = 1
                    break
            if flagA == 0:
                self.ftp_client.mkd(my_dir)
                self.ftp_client.sendcmd('CWD ' + my_dir)
            flagA = 0

    def write_file_on_server(self, local_directory, server_directory):
        self.__check_directory_on_server__(server_directory)
        self.__ftp_upload__(local_directory)
        self.ftp_client.sendcmd('CWD ~')

    def upload_file_of_config(self):
        for key in self._jf.key_list[3:]:
            try:
                l_dir = self._jf.get_key_value(key)[0]
                s_dir = self._jf.get_key_value(key)[1]
                self.write_file_on_server(l_dir, s_dir)
            except IndexError:
                print('Index Error')
                exit()
            print("Файл ", l_dir, ' загружен на сервер')


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
ftp.upload_file_of_config()
ftp.disconnect()
print('Вы отключены от сервера')
