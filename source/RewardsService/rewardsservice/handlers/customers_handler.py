import json
import tornado.web

from tornado.gen import coroutine
from tornado.escape import json_decode

from validator import Validator
from orchestration.customer_orchestrator import Customer_Orchestrator

class CustomersHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self, email=None):
        orchestrator = Customer_Orchestrator.get_instance()
        customer = yield orchestrator.get(email)
        if customer:
            self.write(json.dumps(customer))
        else:
            self.write_error(404)
