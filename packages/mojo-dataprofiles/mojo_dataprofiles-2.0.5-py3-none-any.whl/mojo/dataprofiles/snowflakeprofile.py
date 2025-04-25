
from typing import Dict, Union

from mojo.dataprofiles.basedataprofile import BaseDataProfile

class SnowflakeProfile(BaseDataProfile):

    category = "snowflake"

    def __init__(self, identifier: str, *, category: str, account: str, warehouse: str, database: str, schema: str = None, parameters: Dict[str, str] = None, credential: str = None):
        super().__init__(identifier, category=category, credential=credential)
        
        self._account = account
        self._warehouse = warehouse
        self._database = database
        self._schema = schema
        self._parameters = parameters

        return
    
    @property
    def account(self) -> str:
        return self._account
    
    @property
    def database(self) -> str:
        return self._database
    
    @property
    def parameters(self) -> Dict[str, str]:
        return self._parameters
    
    @property
    def schema(self) -> Union[str, None]:
        return self._schema
    
    @property
    def warehouse(self) -> str:
        return self._warehouse

    @classmethod
    def validate(cls, profile_info: Dict[str, str]):
        """
            dataprofiles:
            -   identifier: snowflake-example
                category: snowflake
                account: some-account 
                warehouse: some-warehouse
                database: some-database
                schema: some-schema
                parameters: 
                    SOME_CONNECTION_PARAMETER: SOMEVALUE
                credential: dbadmin
        """
        
        errors = []
        warns = []

        if "account" not in profile_info:
            errmsg = f"The 'snowflake' profile must have an 'account' field."
            errors.append(errmsg)
        
        if "warehouse" not in profile_info:
            errmsg = f"The 'snowflake' profile must have an 'warehouse' field."
            errors.append(errmsg)
        
        if "database" not in profile_info:
            errmsg = f"The 'snowflake' profile must have an 'database' field."
            errors.append(errmsg)
        
        if "schema" not in profile_info:
            errmsg = f"The 'snowflake' profile must have an 'schema' field."
            errors.append(errmsg)
        
        if "credential" not in profile_info:
            errmsg = f"The 'snowflake' profile must have an 'credential' field."
            errors.append(errmsg)
        

        return errors, warns
