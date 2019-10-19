#!/usr/bin/env python
# encoding: utf-8

from config import config as con
from config import sysparameter as sys_p
from config import file_config as fileC
from logexposer import logSysncronizer as log
from filehandlers import fileparser as file_h
from systemhandlers import sysexecutor as sysExec
import os


class SlaveConfiger:
    def __init__(self):
        self._file_parser = file_h.FileHandler()
        self._sys_Exec = sysExec.SysCommandor()
        self._slave_postgres_version = None
        self._master_ip = None 
        self._rep_user = None   
        self._rep_user_pass = None 

    @property
    def getmaster_IP(self):
        return self._master_ip

    @getmaster_IP.setter 
    def setmaster_IP(self, ip):
        self._master_ip = ip 

    @property 
    def getmasrepuser(self):
        return self._rep_user

    @getmasrepuser.setter 
    def setmasrepuser(self, repU):
        self._rep_user = repU 

    @property 
    def getmasrepuserpass(self):
        return self._rep_user_pass 

    @getmasrepuserpass.setter 
    def setmasrepuserpass(self, pasw):
        self._rep_user_pass = pasw

    @property
    def GetSlavePostgresVersion(self):
        return self._slave_postgres_version

    @GetSlavePostgresVersion.setter
    def setSlavePostgresVersion(self, postgres_v):
        self._slave_postgres_version = postgres_v

    #Change the postgresql.conf file access permission
    def ChangepostgresqlPermit(self, postgres_v):
        dir_c = "../../etc/postgresql/{x}/main/{y}".format(x=postgres_v, y=fileC.File_Config().PSQL_confRoot())
        change_pc = "sudo chmod 777 {y}".format(y=dir_c)
        return change_pc


    #Make the postgresql.conf Protected
    def MakePostgresql_confPermit(self, postgres_v):
        dir_c = "../../etc/postgresql/{x}/main/{y}".format( x=postgres_v, y=fileC.File_Config().PSQL_confRoot())
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
            if '#hot_standby = on' in line:
                print("LOP-1")
                self._file_parser.ConfigLineAppender("hot_standby = on                      # 'on' allows queries during recovery", files)
            else:
                self._file_parser.ConfigLineAppender(line, files)
        return True

    #Get config file from slave
    def GetPostgresql_confile(self, postgres_conf_dir, conObj):
        res = self._sys_Exec.FileTransfer(conObj, "GET", "./confiles/{x}".format(x=fileC.File_Config().PSQL_confRoot()), postgres_conf_dir)
        if res[0]:
            if os.path.exists("./confiles/{x}".format(x=fileC.File_Config().PSQL_confRoot())):
                return True
            return False

    
    #Copy & transfer the  recovery conf file
    def TransferRecoveryConf_Q(self, postgres_v):
        make_Q = "sudo cp -avr ../../usr/share/postgresql/{x}/recovery.conf.sample /../../usr/share/postgresql/{x}/recovery.conf".format(
                x = postgres_v
                )
        return make_Q

    
    #Get the Recovery conf file Query
    def RecoveryConfDir(self, postgres_v):
        dir_Q = "../../usr/share/postgresql/{x}/recovery.conf".format(
            x=postgres_v)
        return dir_Q

    #Get the recovery conf file
    def GetRecovery_confile(self, recovery_conf_dir, conObj):
        res = self._sys_Exec.FileTransfer(conObj, "GET", "./confiles/{x}".format(x=fileC.File_Config().PSQL_RecoveryRoot()), recovery_conf_dir)
        if res[0]:
            if os.path.exists("./confiles/{x}".format(x=fileC.File_Config().PSQL_RecoveryRoot())):
                return True
            return False

    # GET THE LOCAL DIR OR RECOVERY FILE
    def LocalRecoveryDIR(self):
        dir_c = './confiles/{y}'.format(y=fileC.File_Config().PSQL_RecoveryRoot())
        return dir_c

    def RecoveryF_DesDIR(self, postgres_v):
        dir_Q = "../../usr/share/postgresql/{x}/recovery.conf".format(x = postgres_v)
        print(dir_Q)
        return dir_Q



    # RECOVERY FILE FEEDER
    def RecFeeder(self, LineList, files):
        for line in LineList:
            if  '#standby_mode = off' in line:
                self._file_parser.ConfigLineAppender("standby_mode = on", files)
            elif "#primary_conninfo = ''" in line:
                Q_ = "primary_conninfo = '{x}'".format(x='host = {m} port=5432 user={y} password={z}'.format(m = self._master_ip, y=self._rep_user, z=self._rep_user_pass))
                self._file_parser.ConfigLineAppender(Q_, files)
            elif "#trigger_file = ''" in line:
                Z_ = "trigger_file = '/tmp/postgresql.trigger.5432'"
                self._file_parser.ConfigLineAppender(Z_, files)
            else:
                self._file_parser.ConfigLineAppender(line, files)
        return True

    #Change the recovery.conf file access permission
    def ChangepostgresqlRecoveryPermit(self, postgres_v):
        dir_c = "../../usr/share/postgresql/{x}/{y}".format(x=postgres_v, y=fileC.File_Config().PSQL_RecoveryRoot())
        change_pc = "sudo chmod 777 {y}".format(y=dir_c)
        return change_pc


    #Make the recovery.conf Protected
    def MakePostgresql_RecoveryPermit(self, postgres_v):
        dir_c = "../../usr/share/postgresql/{x}/{y}".format(x=postgres_v, y=fileC.File_Config().PSQL_RecoveryRoot())
        permit_Q = 'sudo chmod -v 644 {y}'.format(y=dir_c)
        return permit_Q

    #MOVE RECOVERY FILE TO DESTINATION
    def MoveRecovery_Dest(self, postgres_v):
        dir_c = "sudo cp -avr ../../usr/share/postgresql/{x}/recovery.conf.sample /../../var/lib/postgresql/{x}/main/recovery.conf".format(
            x = postgres_v, y= fileC.File_Config().PSQL_RecoveryRoot()
        )
        print(dir_c)
        return dir_c

    #Backup main rename query
    def Rename_DB_Source_Q_(self, postgres_v):
        Q_ = "sudo mv ../../var/lib/postgresql/{x}/main ../../var/lib/postgresql/{x}/main_old".format(x = postgres_v)
        return Q_


    #Backup the Master Source
    def PGBackup_Q(self, postgres_v, mas_host, mas_repUser, mas_rep_pass):
        pg_Q_ = "sudo PGPASSWORD={rep_pass} pg_basebackup -h {h} -D /var/lib/postgresql/{v}/main -U {rep_user} -v -P -X stream".format(
            rep_pass = mas_rep_pass, h=mas_host, v=postgres_v, rep_user=mas_repUser
        )
        return pg_Q_
