from tornado.gen import coroutine
from pymongo import ReturnDocument
from orchestration.rewards_orchestrator import Rewards_Orchestrator
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
    def get(self, email=None):
        if email:
            rewards_orchestrator = Rewards_Orchestrator.get_instance()
            customer = yield self.db.customers.find_one({'email':email}, projection={'_id':False})
            if customer:
                reward = yield rewards_orchestrator.get_reward(points=customer['points'])
                next_reward = yield rewards_orchestrator.get_reward(points=customer['points'], order=1)
                nr = {
                    'nRewardName' : next_reward['rewardName'],
                    'nTier' : next_reward['tier'],
                    'progress' : (next_reward['points'] - customer['points']) / next_reward['points']
                }
                customer.update(reward)
                customer.update(nr)
            return customer
        else:
            return (yield self.get_all())

    @coroutine
    def update(self, user):
        customer = yield self.db.customers.find_one_and_update({'email': user['email']}, {'$inc' : {'points':user['points']}}, upsert=True, return_document=ReturnDocument.AFTER, projection={'_id':False})
        return customer


    @coroutine
    def get_all(self):
        rewards_orchestrator = Rewards_Orchestrator.get_instance()
        cursor = self.db.customers.find({}, projection={'_id':False})
        customers = yield cursor.to_list(length=None)
        for customer in customers:
            reward = yield rewards_orchestrator.get_reward(points=customer['points'])
            next_reward = yield rewards_orchestrator.get_reward(points=customer['points'], order=1)
            nr = {
                'nRewardName' : next_reward['rewardName'],
                'nTier' : next_reward['tier'],
                'progress' : (next_reward['points'] - customer['points']) / next_reward['points']
            }
            customer.update(reward)
            customer.update(nr)
        return customers