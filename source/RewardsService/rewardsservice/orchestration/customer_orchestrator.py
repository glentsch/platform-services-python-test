from tornado.gen import coroutine
from pymongo import ReturnDocument

class Customer_Orchestrator:
    __instance = None
    def __init__(self, db):
        if Customer_Orchestrator.__instance is None:  
            Customer_Orchestrator.__instance = self
        self.db = db

    @staticmethod
    def get_instance():
        return Customer_Orchestrator.__instance

    @coroutine
    def get(self, email):
        print(email)
        if email:
            customer = yield self.db.customers.find_one({'email':email}, projection={'_id':False})
            return customer
        else:
            return (yield self.get_all())

    @coroutine
    def update(self, user):
        customer = yield self.db.customers.find_one_and_update({'email': user['email']}, {'$inc' : {'points':user['points']}}, upsert=True, return_document=ReturnDocument.AFTER, projection={'_id':False})
        return customer


    @coroutine
    def get_all(self):
        cursor = self.db.customers.find({}, projection={'_id':False})
        return (yield cursor.to_list(length=None))