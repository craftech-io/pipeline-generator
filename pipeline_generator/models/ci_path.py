import pathlib


class CiPath:
    def __init__(self, _path: pathlib.Path, account: str, env: str = '', region: str = ''):
        self.path = _path
        self.account = account
        self.environment = env
        self.region = region

    @property
    def is_account_global(self) -> bool:
        """Return true if the resource y global in the account"""
        return (not self.environment) and (not self.region)

    @property
    def is_region_global(self) -> bool:
        """Return true if the resource y global in the region"""
        return (not self.environment) and self.region

    def __repr__(self):
        return f"{self.path}"
