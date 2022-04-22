import spurplus
import pathlib
import os

class SSH:
    def __init__(self, hostname, username):
        self.hostname = hostname
        self.username = username
        self.private_key_file = None
        self.password = None
        self.shell = None
        self.sftp = None
        self.cwd = pathlib.Path("/")
        self.connected = False

    def connect_whit_private_key(self, private_key_file, with_sftp=False):
        self.private_key_file = private_key_file
        self.shell = spurplus.connect_with_retries(hostname=self.hostname, username=self.username, private_key_file=self.private_key_file)
        if with_sftp:
            self.sftp = self.shell.open_sftp()
        self.connected = True

    def connect_with_password(self, password, with_sftp=False):
        self.password = password
        self.shell = spurplus.connect_with_retries(hostname=self.hostname, username=self.username, password=self.password)
        if with_sftp:
            self.sftp = self.shell.open_sftp()
        self.connected = True

    def create_folder(self, path, parents=True, exist_ok=True):
        remote_path = pathlib.Path(path)
        if not self.connected:
            self.connect()
        self.shell.mkdir(remote_path=remote_path, parents=parents, exist_ok=exist_ok)

    def write_text_file(self, path, text):
        remote_path = pathlib.Path(path)
        if not self.connected:
            self.connect()
        self.shell.write_text(remote_path=remote_path, text=text)

    def read_text_file(self, path):
        remote_path = pathlib.Path(path)
        if not self.connected:
            self.connect()
        return self.shell.read_text(remote_path=remote_path)

    def disconnect(self):
        if self.connected:
            self.shell.close()
            self.connected = False

    def cd(self, path):
        if not self.connected:
            self.connect()
        
        for p in path.replace(os.sep, "/").split("/"):
            if p == "":
                continue
            if p == "..":
                self.cwd = pathlib.Path(self.cwd).parent
                continue
            print(self.cwd)
            self.cwd = self.cwd / pathlib.Path(p)

    def run(self, command, *args, **kwargs):
        if not self.connected:
            self.connect()

        # if not "cwd" in kwargs:
        #     kwargs["cwd"] = self.cwd
        return self.shell.run(command, *args, **kwargs)

    def __getattribute__(self, __name: str):
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            if self.connected:
                return getattr(self.shell, __name)
            else:
                raise AttributeError(f"{__name} is not a valid attribute")


if __name__ == "__main__":
    # hostname = input("hostname: ")
    hostname = "45.79.42.243"
    username = "root"
    # private_key_file = input("private_key_file: ")
    private_key_file = "C:/Users/Caleb/.ssh/id_rsa.pub"

    ssh = SSH(hostname, username, private_key_file)
    ssh.connect()
    # ssh.cd("/var/www/html")

    res = ssh.run(["ls"])
    print(res.output)
    ssh.cd("..")
    print(ssh.cwd)
    res = ssh.run(["ls"])
    print("-----------------")
    print(res.output)
    # ssh.cd("html")
    print(ssh.cwd)
    res = ssh.run(["ls"])
    print("-----------------")
    print(res.output)