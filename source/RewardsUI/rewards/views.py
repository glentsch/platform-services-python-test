import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from conf import SERVER_URL
from .forms import Rewards_Form

class RewardsView(TemplateView):
    template_name = 'rewards.html'
    rewards_url = '{}rewards'.format(SERVER_URL)
    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = Rewards_Form()
        response = requests.get(RewardsView.rewards_url)
        context['rewards_data'] = response.json()
        if not 'customers' in context:
            response = requests.get('{}customers/'.format(SERVER_URL))
            context['customers'] = response.json()
        return TemplateResponse(
            request,
            self.template_name,
            context
        )
    
    def post(self, request, *args, **kwargs):
        form = Rewards_Form(request.POST)
        user_reward = None
        if form.is_valid():
            f = form.process()
            print(f['email'])
            response = requests.get('{}customers/{}/'.format(SERVER_URL, f['email']))
            user_reward = response.json() #TODO: should handle other than 200
            user_reward['progress'] *= 100
        return self.get(request, customers=[user_reward])
