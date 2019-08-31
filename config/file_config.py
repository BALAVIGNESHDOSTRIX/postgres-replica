#!/usr/bin/env python
# encoding: utf-8


class File_Config:

    _file_config = ["postgresql.conf", "pg_hba.conf", "../../var/lib/postgresql/mnt/server/archivedir", "recovery.conf"]

    @classmethod
    def PSQL_confRoot(self):
        return self._file_config[0]

    @classmethod
    def PGHBA_confRoot(self):
        return self._file_config[1]
    
    @classmethod
    def PSQLArchiveDir(self):
        return self._file_config[2]

    @classmethod
    def PSQL_RecoveryRoot(self):
        return self._file_config[3]
