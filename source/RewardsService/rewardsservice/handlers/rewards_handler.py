import json
import tornado.web

from tornado.gen import coroutine
from orchestration.rewards_orchestrator import Rewards_Orchestrator

class RewardsHandler(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        rewards = yield Rewards_Orchestrator.get_instance().get_reward()
        self.write(json.dumps(rewards))
        self.finish()
