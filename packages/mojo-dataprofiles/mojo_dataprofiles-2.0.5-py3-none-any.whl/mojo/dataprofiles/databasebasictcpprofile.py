
from typing import Dict

from mojo.dataprofiles.basedataprofile import BaseDataProfile

class DatabaseBasicTcpProfile(BaseDataProfile):

    category = "basic-tcp"

    def __init__(self, identifier: str, *, category: str, host: str, port: int, dbtype: str, dbname: str = None, credential: str = None):
        super().__init__(identifier, category=category, credential=credential)
        
        self._host = host
        self._port = port
        self._dbtype = dbtype
        self._dbname = dbname

        return
    
    @property
    def dbname(self) -> str:
        return self._dbname
    
    @property
    def dbtype(self) -> str:
        return self._dbtype
    
    @property
    def host(self) -> str:
        return self._host
    
    @property
    def port(self) -> int:
        return self._port

    @classmethod
    def validate(cls, profile_info: Dict[str, str]):
        """
            dataprofiles:
            -   identifier: basic-database
                category: basic-tcp
                dbtype: postgres
                dbname: testdb
                host: somedb.somecompany.com
                port: 8888
                credential: dbadmin
        """
        
        errors = []
        warns = []

        if "credential" not in profile_info:
            errmsg = f"The 'basic-tcp' profile must have an 'credential' field."
            errors.append(errmsg)
        
        if "dbtype" not in profile_info:
            errmsg = f"The 'basic-tcp' profile must have an 'dbtype' field."
            errors.append(errmsg)
        
        if "host" not in profile_info:
            errmsg = f"The 'basic-tcp' profile must have an 'host' field."
            errors.append(errmsg)
        
        if "port" not in profile_info:
            errmsg = f"The 'basic-tcp' profile must have an 'port' field."
            errors.append(errmsg)
        

        return errors, warns