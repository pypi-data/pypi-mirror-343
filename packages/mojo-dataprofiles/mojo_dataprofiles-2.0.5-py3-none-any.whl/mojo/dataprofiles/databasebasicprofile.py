
from typing import Dict

from mojo.dataprofiles.basedataprofile import BaseDataProfile

class DatabaseBasicProfile(BaseDataProfile):

    def __init__(self, identifier: str, *, category: str, dbtype: str, dbname: str = None, credential: str = None):
        super().__init__(identifier, category=category, credential=credential)
        
        self._dbtype = dbtype
        self._dbname = dbname

        return
    
    @property
    def dbname(self) -> str:
        return self._dbname
    
    @property
    def dbtype(self) -> str:
        return self._dbtype

    @classmethod
    def validate(cls, profile_info: Dict[str, str]):
        
        errors = []
        warns = []

        if "credential" not in profile_info:
            errmsg = f"The 'basic-profile' profile must have an 'credential' field."
            errors.append(errmsg)
        
        if "dbname" not in profile_info:
            errmsg = f"The 'basic-profile' profile must have an 'dbname' field."
            errors.append(errmsg)
        
        if "dbtype" not in profile_info:
            errmsg = f"The 'basic-profile' profile must have an 'dbtype' field."
            errors.append(errmsg)

        return errors, warns