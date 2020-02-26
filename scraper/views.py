# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import User, UserStat
from datetime import datetime
import requests, pytz, os, sys


def index(request):
    return render(request, 'scraper/poll.html')


def parse(wg_id, username = None):
    wg_id = str(wg_id)
    # get username info if it isn't known yet
    if username == None:
        username_data = requests.post(
            'https://api.worldofwarships.com/wows/account/info/',
            { 
                'application_id': os.environ['APP_ID'],
                'account_id': wg_id,
                'fields': 'nickname'
            }
        ).json()['data'][wg_id]

        if username_data == None:
            return "User does not exist"
        else:
            username = username_data['nickname']

    response = requests.post(
        'https://api.worldofwarships.com/wows/ships/stats/',
        { 
            'application_id': os.environ['APP_ID'],
            'account_id': wg_id,
            'fields': 'ship_id, pvp.wins, pvp.losses'
        }
    )
    if response.status_code == 200:
        try:
            user_data = response.json()['data'][wg_id]
        except KeyError:
            return 'Sorry, account is marked as private'
        
        user, created = User.objects.get_or_create(wg_user = wg_id, name = username)
        
        # only update if the last updated was less than an hour ago
        if created is False and (datetime.now(tz = pytz.utc) - user.updated_at).seconds < 3600:
            return 'Sorry, wait at least 1 hour before requesting a refresh'
        

        # stop if no user found or has no PVP stats
        if user_data is None:
            return 'Sorry, user has not played any games'
            

        # if it turns out they only have ships for coops, delete from db
        if len(user_data) < 20:
            user.delete()
            return 'Sorry, user has not played enough different ships'

        ships = []
        for ship in user_data:
            if ship['pvp']['wins'] or ship['pvp']['losses']:
                ships.append(
                    UserStat(
                        wg_user_id = wg_id,
                        ship_id = ship['ship_id'],
                        wins = ship['pvp']['wins'],
                        losses = ship['pvp']['losses']
                    )
                )
                
        

        UserStat.objects.bulk_create(ships)
        return 'Done, updated ' + str(len(ships)) + ' rows'
    else:
        return 'Something went wrong with the server'


def scrape(request):
    wg_id = request.POST['wg_id']
    return HttpResponse(parse(wg_id))

def scrapestart(request):
    return render(request, 'scraper/scrapestart.html')

def nextname(name):
    character_set = 'abcdefghijklmnopqrstuvwxyz0123456789_'
    for idx, char in enumerate(name[::-1], start = 1):
        if char != '_':
             break
    next_name = name[:-idx] + character_set[character_set.find(name[-idx]) + 1]
    return next_name.ljust(3,'a')


def scrapeall(request):
    name_start = request.POST['name_start']

    while name_start != '________________':
        name_data = requests.post(
            'https://api.worldofwarships.com/wows/account/list/',
            {
                'application_id': os.environ['APP_ID'],
                'search': name_start
            }
        ).json()['data']
        
        # if no names are found, move onto the next character
        if name_data == None:
            name_start = nextname(name_start)
            continue
        # if 100 names are found (max returned by wg), increase specificity 
        if len(name_data) == 100:
            name_start = name_start + 'a'
        # if less than 100 names are found, move onto the next character
        else:
            name_start = nextname(name_start)
            
        # iterate through the names found
        for name in name_data:
            print("Account: " + name['nickname'] + " Result:" + parse(name['account_id'], name['nickname']), file = sys.stderr)
            
    return HttpResponse("Placeholder")
    
    
