#!/usr/bin/env python
# encoding: utf-8

import os
import paramiko
from config import config as conn

class SysCommandor():

    def __init__(self):
        self.conObj = conn.ConfigInspector()

    #Create the system connection Object
    def ConEStablisher(self,sysip=None, syspass=None, sysusername=None):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            client.connect(sysip, username=sysusername, password=syspass)
            if client:
                return True,client
            else:
                return False,False
        except paramiko.ssh_exception.NoValidConnectionsError:
            return False,self.conObj.ReturnIPErr
        except paramiko.AuthenticationException:
            return False,self.conObj.ReturnPassErr
        except paramiko.ssh_exception.SSHException:
            return False,self.conObj.ReturnSSHErr

    #Execute the Command by using the system connection Object
    def ComExecutor(self, command=None, conobj=None, syspass=None):
        status_chk = []
        try:
            if conobj:
                stdin, stdout, stderr = conobj.exec_command(command, get_pty=True)
                stdin.write(syspass + '\n')
                stdin.flush()
                for out in stdout:
                    status_chk.append(out)
                if status_chk:
                    return True,status_chk
                else:
                    return False,False
        except paramiko.ssh_exception.NoValidConnectionsError:
            return False,self.conObj.ReturnIPErr
        except paramiko.AuthenticationException:
            return False,self.conObj.ReturnPassErr
        except paramiko.ssh_exception.SSHException:
            return False,self.conObj.ReturnSSHErr

    #File Transfer Method
    def FileTransfer(self,conObj=None ,types=None, local_dir=None, remote_dir=None):
        try:
            if conObj:
                sftp_obj = conObj.open_sftp()
                if types == "GET":
                    sftp_obj.get(remote_dir, local_dir)
                elif types == "POST":
                    print(local_dir, remote_dir)
                    sftp_obj.put(local_dir, remote_dir)
                sftp_obj.close()
                return True,True
        except paramiko.ssh_exception.NoValidConnectionsError:
            return False, self.conObj.ReturnIPErr
        except paramiko.AuthenticationException:
            return False, self.conObj.ReturnPassErr
        except paramiko.ssh_exception.SSHException:
            return False, self.conObj.ReturnSSHErr


    
        
