
from typing import Dict, List, Optional, Tuple, Union

import logging
import os

from mojo.errors.exceptions import ConfigurationError

from mojo.dataprofiles.basedataprofile import BaseDataProfile
from mojo.dataprofiles.databasebasicprofile import DatabaseBasicProfile
from mojo.dataprofiles.databasebasictcpprofile import DatabaseBasicTcpProfile
from mojo.dataprofiles.couchdbprofile import CouchDbProfile
from mojo.dataprofiles.mongodbatlasprofile import MongoDBAtlasProfile
from mojo.dataprofiles.snowflakeprofile import SnowflakeProfile

logger = logging.getLogger()

class DataProfileManager:
    """
    """

    def __init__(self):

        self._profiles = {}
        self._source_uris = []

        return
    
    @property
    def profiles(self):
        return self._profiles
    
    def lookup_profile(self, profkey: str) -> Union[DatabaseBasicProfile, DatabaseBasicTcpProfile]:
        """
            Lookup a data source profile by key.
        """
        
        if profkey not in self._profiles:
            errmsg_lines = [
                f"Error missing data source profile '{profkey}'."
            ]
        
            if len(self._source_uris) > 0:
                errmsg_lines.append("PROFILES URIS:")

                for cfile in self._source_uris:
                    errmsg_lines.append(f"    {cfile}")

            errmsg = os.linesep.join(errmsg_lines)

            raise ConfigurationError(errmsg)

        profile = self._profiles[profkey]

        return profile
    
    def load_datasource_profiles(self, configuration_info: dict, source_uris: Optional[List[str]] = None):
        
        if source_uris != None:
            self._source_uris.extend(source_uris)


        if configuration_info is not None and len(configuration_info) > 0:
            try:
                profiles_list = configuration_info["dataprofiles"]
                errors, warnings = self._validate_datasource_profiles(profiles_list)

                if len(errors) == 0:
                    for profile in profiles_list:
                        # Copy the credential so if we modify it, we dont modify the
                        # original declaration.
                        profile = profile.copy()

                        if "identifier" not in profile:
                            errmsg = "Datasource profile items in 'datasources' must have an 'identifier' member."
                            raise ConfigurationError(errmsg)
                        ident = profile["identifier"]

                        if "category" not in profile:
                            errmsg = "Credential items in 'environment/credentials' must have an 'category'."
                            raise ConfigurationError(errmsg)

                        category = profile['category']

                        if category == DatabaseBasicTcpProfile.category:
                            credobj = DatabaseBasicTcpProfile(**profile)
                            self._profiles[ident] = credobj
                        elif category == CouchDbProfile.category:
                            credobj = CouchDbProfile(**profile)
                            self._profiles[ident] = credobj
                        elif category == MongoDBAtlasProfile.category:
                            credobj = MongoDBAtlasProfile(**profile)
                            self._profiles[ident] = credobj
                        elif category == SnowflakeProfile.category:
                            credobj = SnowflakeProfile(**profile)
                            self._profiles[ident] = credobj
                        else:
                            warnmsg = f"Unknown category '{category}' found in database profile '{ident}'"
                            logger.warn(warnmsg)

                else:
                    errmsg_lines = [
                        f"Errors found in credentials.",
                        "ERRORS:"
                    ]
                    for err in errors:
                        errmsg_lines.append(f"    {err}")

                    errmsg_lines.append("WARNINGS:")
                    for warn in warnings:
                        errmsg_lines.append(f"    {warn}")

                    errmsg_lines.append("SOURCE_URIS:")
                    for suri in self._source_uris:
                        errmsg_lines.append(f"    {suri}")

                    errmsg = os.linesep.join(errmsg_lines)
                    raise ConfigurationError(errmsg)

            except KeyError as kerr:
                errmsg = f"No 'dataprofiles' field found."
                raise ConfigurationError(errmsg)
        return
    
    def _validate_datasource_profiles(self, profiles_list: List[Dict[str, str]]) -> Tuple[List[str], List[str]]:

        errors = []
        warns = []

        for profile in profiles_list:

            base_errors, base_warns = BaseDataProfile.validate(profile)

            errors.extend(base_errors)
            warns.extend(base_warns)

            if len(base_errors) == 0:

                category = profile['category']
                
                if category == DatabaseBasicTcpProfile.category:
                    prof_errors, prof_warns = DatabaseBasicTcpProfile.validate(profile)
                    errors.extend(prof_errors)
                    warns.extend(prof_warns)
                elif category == CouchDbProfile.category:
                    prof_errors, prof_warns = CouchDbProfile.validate(profile)
                    errors.extend(prof_errors)
                    warns.extend(prof_warns)
                elif category == MongoDBAtlasProfile.category:
                    prof_errors, prof_warns = MongoDBAtlasProfile.validate(profile)
                    errors.extend(prof_errors)
                    warns.extend(prof_warns)
                elif category == SnowflakeProfile.category:
                    prof_errors, prof_warns = SnowflakeProfile.validate(profile)
                    errors.extend(prof_errors)
                    warns.extend(prof_warns)
                else:
                    ident = profile["identifier"]
                    warnmsg = f"Unknown category '{category}' found in database profile '{ident}'"
                    logger.warn(warnmsg)

                
        return errors, warns