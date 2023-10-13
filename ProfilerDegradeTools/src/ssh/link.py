import paramiko


class LinkSSH(object):
    def __init__(self, hostname, username, password, retry):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = hostname
        self.username = username
        self.password = password
        self.retry_password = retry
        self.authentic_password = ""

    def connect(self):
        try:
            self.ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
            self.authentic_password = self.password
        except Exception as e:
            print("米玛错误")
            self.ssh.connect(hostname=self.hostname, username=self.username, password=self.retry_password)
            self.authentic_password = self.retry_password

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command, get_pty=True)
        stdin.write(self.authentic_password + '\n')
        return stdout.read().decode('utf-8')

    def update_file(self, windows_file_path, linux_file_path):
        sftp = self.ssh.open_sftp()
        sftp.put(windows_file_path, linux_file_path)
        sftp.close()

    def is_connected(self):
        try:
            response = self.__execute_command('echo MechEye has been connected!')
            print(response)
            if 'connected' in response:
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def __del__(self):
        self.ssh.close()


if __name__ == "__main__":
    link = LinkSSH()
    link.__connect()
    link.__is_connected()