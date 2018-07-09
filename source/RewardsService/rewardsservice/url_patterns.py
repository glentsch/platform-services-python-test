from handlers.rewards_handler import RewardsHandler
from handlers.orders_handler import OrdersHandler
from handlers.customers_handler import CustomersHandler

from orchestration import *
url_patterns = [
    (r'/rewards/', RewardsHandler),
    (r'/orders/', OrdersHandler),
    (r'/customer/(.*?)', CustomersHandler),
]

orchestrators = [
    orders_orchestrator.Orders_Orchestrator,
    rewards_orchestrator.Rewards_Orchestrator,
    customer_orchestrator.Customer_Orchestrator,
]
