
class VaultAuthMethod:
    """This class represents a vault authentication method"""

    def __init__(self, name: str, command: str):
        """
        :param name: authentication method name
        :param command: command to authenticate to the vault server
        """
        self.name = name
        self.command = command
