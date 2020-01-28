# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import User, UserStat
from datetime import datetime
import requests, pytz


def index(request):
    return render(request, 'scraper/poll.html')
    
def scrape(request):
    wg_id = request.POST['wg_id']
    response = requests.post(
        'https://api.worldofwarships.com/wows/ships/stats/',
        { 
            'application_id': '1df834dca65ba41ccb2844c0f47328f1',
            'account_id': wg_id,
            'fields': 'ship_id, pvp.wins, pvp.losses'
        }
    )
    if response.status_code == 200:
        for id, user_data in response.json()['data'].items():
            user, created = User.objects.get_or_create(wg_user = id)
            
            # only update if the last updated was less than an hour ago
            if created is False and (datetime.now(tz = pytz.utc) - user.updated_at).seconds < 3600:
                continue
            breakpoint()
            # for the first iteration we bulk create all to save db statements
            if created:
                UserStat.objects.bulk_create
            else:
                for ship in user_data:
                    if ship['pvp']['wins'] or ship['pvp']['losses']:
                        UserStat.objects.create(
                            wg_user_id = id,
                            ship_id = ship['ship_id'],
                            wins = ship['pvp']['wins'],
                            losses = ship['pvp']['losses']
                        )
                
    return HttpResponse('Done')