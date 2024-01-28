from curses import OK
from http import HTTPStatus
from http.client import BAD_REQUEST, NOT_FOUND
from http.server import BaseHTTPRequestHandler
import json 
import logging
import uuid

from scoring_api.store import Store

from .constants import ERRORS, INTERNAL_ERROR
from .scoring import get_interests, get_score
from .auth import check_auth
from .data import ClientsInterestsData, MethodData, OnlineScoreData


def method_handler(request: dict, context: dict, store) -> tuple[dict | str, int]:
    method_data = MethodData(**request['body'])
    if not check_auth(method_data):
        return 'Forbidden', HTTPStatus.FORBIDDEN
    if method_data.is_admin:
        return {'score': 42}, HTTPStatus.OK
    if method_data.method == 'online_score':
        try:
            data = OnlineScoreData(**method_data.arguments)
        except ValueError as exception:
            return str(exception), HTTPStatus.UNPROCESSABLE_ENTITY
        score = get_score(store, data.phone, data.email, data.birthday, data.gender, data.first_name, data.last_name)
        context['has'] = data.has
        return {'score': score}, HTTPStatus.OK
    elif method_data.method == 'clients_interests':
        try:
            data = ClientsInterestsData(**method_data.arguments)
        except ValueError as exception:
            return str(exception), HTTPStatus.UNPROCESSABLE_ENTITY
        interests = {client_id: get_interests(client_id, store) for client_id in data.client_ids}
        context['nclients'] = data.clients
        return interests, HTTPStatus.OK
    else:
        return f'Method {method_data.method} not found', HTTPStatus.NOT_FOUND


class MainHTTPHandler(BaseHTTPRequestHandler):

    router = {
        "method": method_handler
    }

    def get_request_id(self, headers):
        return headers.get('HTTP_X_REQUEST_ID', uuid.uuid4().hex)

    def do_POST(self):
        response, code = {}, OK
        context = {"request_id": self.get_request_id(self.headers)}
        request = None
        try:
            data_string = self.rfile.read(int(self.headers['Content-Length']))
            request = json.loads(data_string)
        except:
            code = BAD_REQUEST

        if request:
            path = self.path.strip("/")
            logging.info("%s: %s %s" % (self.path, data_string, context["request_id"]))
            if path in self.router:
                try:
                    response, code = self.router[path]({"body": request, "headers": self.headers}, context, self.store)
                except Exception as e:
                    logging.exception("Unexpected error: %s" % e)
                    code = INTERNAL_ERROR
            else:
                code = NOT_FOUND

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        if code not in ERRORS:
            r = {"response": response, "code": code}
        else:
            r = {"error": response or ERRORS.get(code, "Unknown Error"), "code": code}
        context.update(r)
        logging.info(context)
        self.wfile.write(json.dumps(r).encode())
        return
