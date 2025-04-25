
from typing import Dict

from mojo.dataprofiles.basedataprofile import BaseDataProfile
from mojo.interfaces.ibasiccredential import IBasicCredential

class CouchDbProfile(BaseDataProfile):

    category = "couchdb"

    def __init__(self, identifier: str, *, category: str, host: str, port: int, scheme: str = "http", dbname: str = None, credential: str = None):
        super().__init__(identifier, category=category, credential=credential)
        
        self._host = host
        self._port = port
        self._scheme = scheme
        self._dbname = dbname

        return
    
    @property
    def dbname(self) -> str:
        return self._dbname
    
    @property
    def host(self) -> str:
        return self._host
    
    @property
    def port(self) -> int:
        return self._port

    def connection_string(self, credobj: IBasicCredential) -> str:
        connstr = f"{self._scheme}://{credobj.username}:{credobj.password}@{self._host}:{self._port}"
        return connstr

    @classmethod
    def validate(cls, profile_info: Dict[str, str]):
        """
            -   identifier: couchdb-example
                category: couchdb
                dbname: testdb
                host: somedb.somecompany.com
                port: 8888
                credential: dbadmin
        """

        errors = []
        warns = []

        if "credential" not in profile_info:
            errmsg = f"The 'couchdb' profile must have an 'credential' field."
            errors.append(errmsg)
        
        if "dbname" not in profile_info:
            errmsg = f"The 'couchdb' profile must have an 'dbname' field."
            errors.append(errmsg)
        
        if "host" not in profile_info:
            errmsg = f"The 'couchdb' profile must have an 'host' field."
            errors.append(errmsg)
        
        if "port" not in profile_info:
            errmsg = f"The 'couchdb' profile must have an 'port' field."
            errors.append(errmsg)

        return errors, warns