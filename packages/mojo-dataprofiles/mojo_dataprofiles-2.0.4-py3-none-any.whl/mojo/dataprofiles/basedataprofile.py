
from typing import Dict, List, Optional, Tuple, Union

class BaseDataProfile:
    """
        The :class:`BaseDataProfiles` object serves as a base class for data source profile objects.
    """
    def __init__(self, identifier: str, *, category: str, credential: Optional[str] = None):
        self._identifier = identifier
        self._category = category
        self._credential = credential
        return

    @property
    def credential(self) -> Union[str, None]:
        return self._credential

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def category(self) -> str:
        return self._category
    
    @classmethod
    def validate(cls, profile_info: Dict[str, str]) -> Tuple[List[str], List[str]]:
        """
            Validates that a data profile has the minimum required fields of a data profile.
        """
        errors = []
        warns = []

        identifier = "Unknown"

        if "identifier" not in profile_info:
            errmsg = "Profile is missing the mandatory 'identifier' field."
            errors.append(errmsg)
        else:
            identifier = profile_info["identifier"]

        if "category" not in profile_info:
            errmsg = f"The '{identifier}' profile is missing the mandatory 'category' field."
            errors.append(errmsg)

        return errors, warns
