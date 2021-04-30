from pathlib import Path
from typing import List

import pkg_resources

from pipeline_generator.config.constants import TERRAGRUNT_RE_LIST
from pipeline_generator.models.ci_path import CiPath


def get_path_list(base_path, file_pattern) -> List[Path]:
    p = Path(base_path)
    return list(p.glob(file_pattern))


def get_template_dict() -> dict:
    """
    Search for jinja template files(j2 extension) on templates directory and returns a dictionary with
    key=filena_name (without extension) and value=template_full_path
    :return: dictionary with the form: {'git_prvider': template_path}
    """
    templates_path = Path(pkg_resources.resource_filename('pipeline_generator', 'templates'))
    template_path_list = list(templates_path.glob('*.j2'))
    templates_dict = {}
    for template_path in template_path_list:
        templates_dict[template_path.stem] = template_path
    return templates_dict


def get_ci_path_list(_path_list: List[Path]) -> List[CiPath]:
    """
    Search for matches in _path_list with regex in TERRAGRUNT_RE_LIST. If there is a match, a CiPath object is created
    and appended to a list with attributes equals to captured groups in the regular expression.

    :param _path_list: List of Paths
    :return: List of CiPath
    """
    ci_path_list = []
    for _path in _path_list:
        for regex_path in TERRAGRUNT_RE_LIST:
            m = regex_path.match(str(_path))
            if m:
                ci_path_list.append(CiPath(_path, **m.groupdict()))  # named groups as keyword arguments
                break
    return ci_path_list


def get_env_list(_ci_path_list: List[CiPath]) -> List[str]:
    """Return an ordered list with the environments"""
    return sorted(set(ci_path.envirnonment for ci_path in _ci_path_list if ci_path.envirnonment))


def get_account_list(_ci_path_list: List[CiPath]) -> List[str]:
    """Return an ordered list with the accounts"""
    return sorted(set(ci_path.account for ci_path in _ci_path_list))
