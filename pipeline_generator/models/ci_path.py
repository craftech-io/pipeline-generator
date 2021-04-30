import pathlib


class CiPath:
    def __init__(self, _path: pathlib.Path, account: str, env: str = '', region: str = ''):
        self.path = _path
        self.account = account
        self.envirnonment = env
        self.region = region

    @property
    def is_account_global(self) -> bool:
        """Return true if the resource y global in the account"""
        return (not self.envirnonment) and (not self.region)

    @property
    def is_region_global(self) -> bool:
        """Return true if the resource y global in the region"""
        return (not self.envirnonment) and self.region
