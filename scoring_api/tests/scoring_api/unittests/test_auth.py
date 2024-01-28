from collections import namedtuple
import datetime
import pytest

from scoring_api.auth import check_auth


Request = namedtuple('Request', ['is_admin', 'account', 'login', 'token'])


@pytest.mark.parametrize(
    'passed_request,expected',
    [
        (Request(True, 'some account', 'some login', 'dc96a2ce7ee635b389a18cdbd2ae291482d2a75caec67e8b6f66ddb8f59512abcac0ae44e90c549223b56f1f24fbf781567747e810a03afffd2236049612ce21'), True),
        (Request(True, 'some account', 'some login', 'some bad token'), False),
        (Request(False, 'some account', 'some login', 'd554aa40fc77a64de238f104dc009bfea863ba7be8ef10ecf619106467f0b20beb3d4e387a2443fe8b7e4b40b6a04454ec6af0983d7d386786fdd8e9c0382359'), True),
        (Request(False, 'some account', 'some login', 'some bad token'), False),
    ]
)
def test_check_auth(passed_request, expected):
    # act & assert
    print(passed_request)
    assert check_auth(passed_request) == expected
