from curses import OK
from http.client import BAD_REQUEST, NOT_FOUND
from http.server import BaseHTTPRequestHandler
import json 
import logging
import uuid

from constants import ERRORS, INTERNAL_ERROR
from requests import MethodRequest, OnlineScoreRequest
from scoring import get_interests, get_score
from auth import check_auth
from requests import ClientsInterestsRequest


def method_handler(request, ctx, store):
    body = request['body']
    method_request = MethodRequest(**body)
    #if not check_auth(method_request):
    #    return "Forbidden", 403
    if method_request.is_admin:
        response, code = {'score': 42}, 200
    if method_request.method == 'online_score':
        r = OnlineScoreRequest(**method_request.arguments)
        try:
            score = get_score(r.phone, r.email, r.birthday, r.gender, r.first_name, r.last_name)
        except ValueError as e:
            response, code = {'error': str(e)}, 422
        response, code = {'score': score}, 200
    elif method_request.method == 'clients_interests':
        r = ClientsInterestsRequest(**method_request.arguments)
        interests = {}
        try:
            for client_id in r.client_ids:
                interests[client_id] = get_interests()
        except ValueError as e:
            response, code = {'error': str(e)}, 422
        response, code = interests, 200
    return response, code


class MainHTTPHandler(BaseHTTPRequestHandler):

    router = {
        "method": method_handler
    }
    store = None

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
