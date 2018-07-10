from orchestration.rewards_orchestrator import Rewards_Orchestrator
from orchestration.customer_orchestrator import Customer_Orchestrator
from tornado.gen import coroutine

class Orders_Orchestrator:
    __instance = None
    def __init__(self, db):
        if Orders_Orchestrator.__instance is None:  
            Orders_Orchestrator.__instance = self
        self.db = db

    @staticmethod
    def get_instance():
        return Orders_Orchestrator.__instance

    @coroutine
    def create_one(self, order):
        #get points, to make any deductions
        rewards_orchestrator = Rewards_Orchestrator.get_instance()
        customer_orchestrator = Customer_Orchestrator.get_instance()
        customer = {"email": order["email"], "points": int(order["total"])}
        customer = yield customer_orchestrator.update(customer)
        reward = yield rewards_orchestrator.get_reward(customer['points'])
        next_reward = yield rewards_orchestrator.get_reward(customer['points'], order=1)
        if reward is not None:
            order['total'] *= (1 - reward['deduction'])
            order['total'] = round(order['total'], 2)
        else:
            reward = {'points':0, 'tier':None, 'rewardName':None}
        self.db.orders.insert_one(order)
        progress = (next_reward['points'] - customer['points']) / next_reward['points']
        response_dict = { \
            "email": order['email'], \
            "points": customer['points'], \
            "reward": reward['points'],\
            "tier": reward['tier'], \
            "tier name": reward['rewardName'], \
            "next tier": next_reward['tier'], \
            "next tier name" : next_reward['rewardName'], \
            'next tier progress' : progress \
            }
        return response_dict
    @coroutine
    def get_all(self):
        cursor = self.db.orders.find({}, projection={'_id':False})
        return (yield cursor.to_list(length=None))
    @coroutine
    def get(self, email=None):
        if email:
            cursor = self.db.orders.find({'email':email}, projection={'_id':False})
            return (yield cursor.to_list(length=None))
        else:
            return (yield self.get_all())
