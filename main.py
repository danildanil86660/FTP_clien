import ftplib


class FtpClient:
    _host = ""
    _login = ""
    _password = ""
    ftp_client = ""

    def __init__(self, host, login, password):
        self._host = host
        self._login = login
        self._password = password

    def authorization(self):
        self.ftp_client = ftplib.FTP(self._host, self._login, self._password)
        print(self.ftp_client.getwelcome())


host = '93.189.41.9'
ftp_user = 'user54015'
ftp_password = 'EZjb3lRIo1Av'

FtpClient(host, ftp_user, ftp_password).authorization()


