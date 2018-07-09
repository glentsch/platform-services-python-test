import json
import tornado.web

from tornado.gen import coroutine
from tornado.escape import json_decode

from validator import Validator
from orchestration.orders_orchestrator import Orders_Orchestrator

class OrdersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        pass
    @coroutine
    def post(self):
        def validate(obj):
            schema = {"email": "str", "total":"float"}
            return Validator.validate(schema, obj)
        data = json_decode(self.request.body)
        if not validate(data): self.send_error(error_code=422); return
        data = yield Orders_Orchestrator.get_instance().create_one(data)
        self.write(json.dumps(data))
        
        