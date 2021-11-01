from pipeline_generator.config.vault import VAULT_AUTH_METHODS
from pipeline_generator.models.vault_auth_method import VaultAuthMethod
from typing import Mapping


def get_vault_auth_method_dict() -> Mapping[str, VaultAuthMethod]:
    vault_auth_method_dict = {}
    for vault_auth_method_name, vault_auth_method_properties in VAULT_AUTH_METHODS.items():
        vault_auth_method_dict[vault_auth_method_name] = VaultAuthMethod(
            name=vault_auth_method_name,
            command=vault_auth_method_properties['command'])
    return vault_auth_method_dict
