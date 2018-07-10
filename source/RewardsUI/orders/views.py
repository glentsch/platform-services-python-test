import logging
import requests
import json
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from .forms import Order_Form
from conf import SERVER_URL

class Orders_View(TemplateView):
    template_name = 'orders.html'
    orders_url = '{}orders'.format(SERVER_URL)
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger  

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print(context)
        form = Order_Form()
        response = requests.get(Orders_View.orders_url)
        context['orders_data'] = response.json()
        context['form'] = form
        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = Order_Form(request.POST)
        if form.is_valid():
            f = form.process()
            payload = {'email':f['email'], 'total': f['total']}
            response = requests.post(Orders_View.orders_url, data=json.dumps(payload))
            response = response.json()
            response['tier_name'] = response['tier name']
            response['n_tier_name'] = response['next tier']
            response['n_tier_reward'] = response['next tier name']
            response['n_tier_progress'] = int(response['next tier progress'] * 100)
            context['order'] = response
        return self.get(request, order=response)

