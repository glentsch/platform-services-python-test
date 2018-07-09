from tornado.gen import coroutine

class Rewards_Orchestrator:
    __instance = None
    def __init__(self, db):
        if Rewards_Orchestrator.__instance is None:
            Rewards_Orchestrator.__instance = self
        self.db = db

    @staticmethod
    def get_instance():
        return Rewards_Orchestrator.__instance

    @coroutine
    def get_all(self):
        cursor = self.db.rewards.find({}, projection={'_id':False})
        return (yield cursor.to_list(length=None))
        
    @coroutine
    def get_reward(self, points=None, order=-1):
        func = "$lte" if order == -1 else "$gt"
        if points is not None:
            cursor = self.db.rewards.find({"points": {func : int(points)}}, projection={'_id':False}).sort("points",order).limit(1)
            while ( yield cursor.fetch_next):
                return cursor.next_object()
            else:
                return None
        else:
            return (yield self.get_all())