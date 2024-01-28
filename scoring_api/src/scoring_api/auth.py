import datetime
import hashlib

from .constants import (
    ADMIN_SALT,
    SALT,
)


def check_auth(request):
    if request.is_admin:
        date_for_hash = datetime.datetime(1970, 1, 1)
        digest = hashlib.sha512((date_for_hash.strftime("%Y%m%d%H") + ADMIN_SALT).encode()).hexdigest()
    else:
        digest = hashlib.sha512((request.account + request.login + SALT).encode()).hexdigest()
    print(digest)
    if digest == request.token:
        return True
    return False
