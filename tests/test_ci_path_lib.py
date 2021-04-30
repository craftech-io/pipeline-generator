import os
import pickle
from pathlib import Path
from typing import List

import pytest

from pipeline_generator.libs.ci_path_lib import get_env_list, get_ci_path_list, get_account_list
from pipeline_generator.models.ci_path import CiPath

package_directory = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def path_list() -> List[Path]:
    with open(os.path.join(package_directory, 'pickles/path_list_01.pickle'), 'rb') as f:
        return pickle.load(f)


@pytest.fixture
def ci_path_list(path_list) -> List[CiPath]:
    return get_ci_path_list(path_list)


def test_get_env_list(ci_path_list):
    env_list = get_env_list(ci_path_list)
    print(env_list)
    assert ['dev', 'mgt', 'prd'] == env_list


def test_get_account_list(ci_path_list):
    account_list = get_account_list(ci_path_list)
    assert ['dev', 'prd'] == account_list
