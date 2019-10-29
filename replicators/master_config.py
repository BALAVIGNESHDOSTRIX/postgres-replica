#!/usr/bin/env python
# encoding: utf-8

from config import config as con
from config import sysparameter as sys_p 
from config import file_config as fileC
from logexposer import logSysncronizer as log
from filehandlers import fileparser as file_h
from systemhandlers import sysexecutor as sysExec 
import os 


class MasterConfigMaster:

    def __init__(self):
        self._host_database_username = None 
        self._host_database_us_password = None 
        self._replica_user_name = None 
        self._replica_slave_count = None
        self._replica_user_password = None  
        self._replica_archiveDir = None 
        self._replica_maxwal_sender_c = None  
        self._master_postgres_version = None
        self._file_parser = file_h.FileHandler()
        self._sys_Exec = sysExec.SysCommandor()
        self._stand_by_ip = None 

    @property
    def GetDBUsername(self):
        return self._host_database_username

    @GetDBUsername.setter 
    def setDBUsername(self, username):
        self._host_database_username = username 

    @property 
    def GetDBUserPassword(self):
        return self._host_database_us_password
    
    @GetDBUserPassword.setter 
    def setDBUserPassword(self, userpass):
        self._host_database_us_password = userpass 
        
    @property
    def GetStandByMachineIP(self):
        return self._stand_by_ip

    @GetStandByMachineIP.setter 
    def setStandByMachineIP(self, slav_ip):
        self._stand_by_ip = slav_ip

    @property
    def GetMasterPostgresVersion(self):
        return self._master_postgres_version

    @GetMasterPostgresVersion.setter 
    def setMasterPostgresVersion(self, postgres_v):
        self._master_postgres_version = postgres_v

    @property
    def GetArchiveDir(self):
        return self._replica_archiveDir
    
    @GetArchiveDir.setter 
    def setReplicaArchiveDir(self, archive_dir):
        self._replica_archiveDir = archive_dir

    
    @property 
    def GetMaxWalSender(self):
        return self._replica_maxwal_sender_c

    @GetMaxWalSender.setter 
    def setMaxWalSender(self, max_wal_c):
        self._replica_maxwal_sender_c = max_wal_c 


    @classmethod
    def MasSysVersionQuery(self):
        command = "cat {x}".format(x=sys_p.SystemParameters().getOS_RELEASE_Q())
        return command

    @classmethod 
    def MasSysPostgresql_VQuery(self):
        command = "psql -V"
        return command

    @classmethod
    def MasPostgresServiceStopQuery(self):
        command = "sudo service postgresql stop"
        return command 
    
    @classmethod
    def MasPostgresServiceStartQuery(self):
        command = "sudo service postgresql start"
        return command

    @classmethod
    def MasPostgresServiceRestatQuery(self):
        command = "sudo service postgresql restart"
        return command

    @property
    def GetReplicationUserN(self):
        return self._replica_user_name

    @GetReplicationUserN.setter
    def setReplicaUserName(self, rep_n):
        self._replica_user_name = rep_n

    @property
    def GetReplicaSlaveCount(self):
        return self._replica_slave_count
    
    @GetReplicaSlaveCount.setter 
    def setReplicaSaleveCount(self, rep_c):
        self._replica_slave_count = rep_c

    @property
    def GetReplicaUserPassword(self):
        return self._replica_user_password

    @GetReplicaUserPassword.setter
    def setReplicaUserPassword(self, replic_pass):
        self._replica_user_password = replic_pass


    #Generate the Repication User Query
    def MakeReplicaUserQuery(self, replica_user, replica_slave_c):
        command = "sudo -u postgres createuser -U postgres {z} -c {x} --replication".format(z=replica_user,x=replica_slave_c)
        return command

    
    #Get the Replica Archive Directory Path
    def MakeReplicaDIRQuery(self, dir=None):
        command = "sudo mkdir -p {dir}".format(dir=dir)
        return command 

    #Check the Replication Directory is Available or not
    def CheckReplicaDirIsAvail(self, dir=None):
        command = 'sudo [ -d "{x}" ] && echo "{y}"'.format(x=dir,y="True")
        return command

    #Change the postgresql.conf file access permission 
    def ChangepostgresqlPermit(self, postgres_v):
        dir_c = "../../etc/postgresql/{x}/main/{y}".format(x=postgres_v, y=fileC.File_Config().PSQL_confRoot())
        change_pc = "sudo chmod 777 {y}".format(y=dir_c)
        return change_pc

    #Make the postgresql.conf Protected
    def MakePostgresql_confPermit(self, postgres_v):
        dir_c = "../../etc/postgresql/{x}/main/{y}".format(x=postgres_v, y=fileC.File_Config().PSQL_confRoot())
        permit_Q = 'sudo chmod -v 644 {y}'.format(y=dir_c)
        return permit_Q

    #Return the postgresql.conf file dir
    def PostgresqlDIR(self, postgres_v):
        dir_c = "../../etc/postgresql/{x}/main/{y}".format(x=postgres_v, y=fileC.File_Config().PSQL_confRoot())
        return dir_c

    #GET Local postgresql_conf file dir
    def LocalPostgresqlDIR(self):
        dir_c = './confiles/{y}'.format(y=fileC.File_Config().PSQL_confRoot())
        return dir_c

    #ConfigLines Replacer
    def ConfigLineFeeder(self, LineList, files):
        for line in LineList:
            if '#wal_level' in line:
                self._file_parser.ConfigLineAppender("wal_level = hot_standby        # minimal, replica, or logical", files)
            elif '#archive_mode' in line:
                self._file_parser.ConfigLineAppender("archive_mode = on              # enables archiving; off, on, or always", files)
            elif '#archive_command' in line:
                self._file_parser.ConfigLineAppender("archive_command='test ! -f mnt/server/archivedir/%f && cp %p mnt/server/archivedir/%f'", files)
            elif '#max_wal_senders' in line:
                self._file_parser.ConfigLineAppender('max_wal_senders = {x}            # max number of walsender processes'.format(x=self.GetMaxWalSender), files)
            else:
                self._file_parser.ConfigLineAppender(line, files)
        return True

    #Get config file from slave
    def GetPostgresql_confile(self, postgres_conf_dir, conObj):
        res = self._sys_Exec.FileTransfer(conObj, "GET", "./confiles/{x}".format(x=fileC.File_Config().PSQL_confRoot()), postgres_conf_dir)
        if res[0]:
            if os.path.exists("./confiles/{x}".format(x=fileC.File_Config().PSQL_confRoot())):
                return True 
            else:
                return False

    #GET hba_file Dir
    def GetHbaFileDIR(self, postgres_v):
        dir_c = "../../etc/postgresql/{x}/main/{y}".format(x=postgres_v, y=fileC.File_Config().PGHBA_confRoot())
        return dir_c

    #Get replication entry Line
    def GetReplicaEntryLine(self, repuser, slave_ip):
        line_Q = '"host     replication     {c}         {z}/32        md5"'.format(c=repuser, z=slave_ip)
        return line_Q


    #Return the Host Replication Entry in pg_hba query
    def PGHBA_EntryMaker(self, pg_hba_dir, slave_ip, repuser):
        line_Q = self.GetReplicaEntryLine(repuser, slave_ip)
        entry_query = "sudo /bin/sh -c 'echo {entry} >>  {pghba_dir}'".format(entry='{x}'.format(x=line_Q), pghba_dir=pg_hba_dir)
        return entry_query 

    #def PGHBA_Entry_checker
    def PGHBA_Entry_Checker(self, pattern, pg_hba_dir):
        checker_query = "sudo grep -q {x} {y} && echo $?".format(x=pattern, y=pg_hba_dir)
        return checker_query
