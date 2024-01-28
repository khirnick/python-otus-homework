import datetime
import hashlib
import pytest
from scoring_api.constants import ADMIN_LOGIN, ADMIN_SALT, SALT
from scoring_api.server import method_handler


def set_valid_auth(request):
    if request.get("login") == ADMIN_LOGIN:
        date_for_hash = datetime.datetime(1970, 1, 1)
        request["token"] = hashlib.sha512((date_for_hash.strftime("%Y%m%d%H") + ADMIN_SALT).encode()).hexdigest()
    else:
        msg = (request.get("account", "") + request.get("login", "") + SALT).encode()
        request["token"] = hashlib.sha512(msg).hexdigest()


@pytest.mark.parametrize(
    'arguments',
    [
        ({"gender": 1, "birthday": "01.01.2000", "first_name": "a", "last_name": "b"}),
        ({"gender": 0, "birthday": "01.01.2000"}),
        ({"gender": 2, "birthday": "01.01.2000"}),
        ({"first_name": "a", "last_name": "b"}),
        ({"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000",
         "first_name": "a", "last_name": "b"}),
    ]
)
def test_online_scores__ok(mocker, arguments):
    mocked_store = mocker.Mock()
    mocked_store.cache_get.return_value = 200
    req = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
    set_valid_auth(req)
    result, code = method_handler({'body': req}, {}, mocked_store)
    assert result['score'] >= 0, result
    assert code == 200


@pytest.mark.parametrize(
    'arguments',
    [
        ({}),
        ({"phone": "79175002040"}),
        ({"phone": "89175002040", "email": "stupnikov@otus.ru"}),
        ({"phone": "79175002040", "email": "stupnikovotus.ru"}),
        ({"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": -1}),
        ({"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": "1"}),
        ({"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.1890"}),
        ({"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "XXX"}),
        ({"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000", "first_name": 1}),
        ({"phone": "79175002040", "email": "stupnikov@otus.ru", "gender": 1, "birthday": "01.01.2000",
         "first_name": "s", "last_name": 2}),
        ({"phone": "79175002040", "birthday": "01.01.2000", "first_name": "s"}),
        ({"email": "stupnikov@otus.ru", "gender": 1, "last_name": 2}),
    ]
)
def test_online_scores__bad(mocker, arguments):
    mocked_store = mocker.Mock()
    req = {"account": "horns&hoofs", "login": "h&f", "method": "online_score", "arguments": arguments}
    set_valid_auth(req)
    _, code = method_handler({'body': req}, {}, mocked_store)
    assert code == 422, (arguments)



def test_onlince_scores__ok_admin():
    arguments = {"phone": "79175002040", "email": "stupnikov@otus.ru"}
    request = {"account": "horns&hoofs", "login": "admin", "method": "online_score", "arguments": arguments}
    set_valid_auth(request)
    result, code = method_handler({'body': request}, {}, None)
    assert result['score'] == 42, result
    assert code == 200



@pytest.mark.parametrize(
    'arguments',
    [
        ({"client_ids": [1, 2, 3], "date": datetime.datetime.today().strftime("%d.%m.%Y")}),
        ({"client_ids": [1, 2], "date": "19.07.2017"}),
        ({"client_ids": [0]}),
    ]
)
def test_client_interests__ok(mocker, arguments):
    mocked_store = mocker.Mock()
    mocked_store.get.return_value = ['1', '2']
    req = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
    set_valid_auth(req)
    result, code = method_handler({'body': req}, {}, mocked_store)
    mocked_store.get.assert_called_once
    assert code == 200


@pytest.mark.parametrize(
    'arguments',
    (
        ({}),
        ({"date": "20.07.2017"}),
        ({"client_ids": {1: 2}, "date": "20.07.2017"}),
        ({"client_ids": ["1", "2"], "date": "20.07.2017"}),
        ({"client_ids": [1, 2], "date": "XXX"}),
    )
)
def test_client_interests__bad(mocker, arguments):
    req = {"account": "horns&hoofs", "login": "h&f", "method": "clients_interests", "arguments": arguments}
    set_valid_auth(req)
    result, code = method_handler({'body': req}, {}, None)
    assert code == 422