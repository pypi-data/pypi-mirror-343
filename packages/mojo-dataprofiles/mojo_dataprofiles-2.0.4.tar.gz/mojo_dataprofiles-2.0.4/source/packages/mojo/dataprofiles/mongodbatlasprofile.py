
from typing import Dict

from mojo.dataprofiles.basedataprofile import BaseDataProfile
from mojo.interfaces.ibasiccredential import IBasicCredential

class MongoDBAtlasProfile(BaseDataProfile):

    category = "mongodb-atlas"

    def __init__(self, identifier: str, *, category: str, connection: str, credential: str = None):
        super().__init__(identifier, category=category, credential=credential)
        
        self._connection = connection
        return
    
    @property
    def connection(self) -> str:
        return self._connection

    def connection_string(self, credobj: IBasicCredential) -> str:
        connstr = self._connection.replace("<username>", credobj.username).replace("<password>", credobj.password)
        return connstr

    @classmethod
    def validate(cls, profile_info: Dict[str, str]):
        """
            dataprofiles:
            -   identifier: mongodb-example
                category: mongodb-atlas
                connection: mongodb+srv://<username>:<password>@automation-mojo-db.q0jpg0g.mongodb.net/
        """
        
        errors = []
        warns = []

        if "credential" not in profile_info:
            errmsg = f"The 'mongodb-atlas' profile must have an 'credential' field."
            errors.append(errmsg)
        
        if "connection" not in profile_info:
            errmsg = f"The 'mongodb-atlas' profile must have an 'credential' field."
            errors.append(errmsg)

        return errors, warns
