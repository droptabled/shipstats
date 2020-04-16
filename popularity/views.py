from django.shortcuts import render
from django.http import JsonResponse
from . import models
from scraper import models as sm
# Create your views here.

def relations(request):
    return render(request, 'popularity/allrelations.html')
    
def graphdata(request):
    request_ships = sm.Ship.objects.all()
    if request.GET['type']:
        request_ships = request_ships.filter(type__i_exact = request.GET['type'])
    if request.GET['nation']:
        request_ships = request_ships.filter(nation = request.GET['nation'])
    if request.GET['tier']:
        request_ships = request_ships.filter(tier = request.GET['tier'])
    
    return JsonResponse(generate_graph(request_ships))

def get_or_create_edge(ship1, ship2):
    edges = ShipRelation.objects.filter(ship1_in = [ship1, ship2], ship2_in = [ship1, ship2])
    if len(edges) == 0:
        edge = ShipRelation.objects.create(ship1 = ship1, ship2 = ship2)
    elif len(edge) == 1:
        edge = edges[0]
    else:
        raise ValueError('Mismatched data, extra edges between '+ship1.name+' and '+ship2.name)
    return edge.get_edge()
    
def generate_graph(ships):
    graph = { "nodes":[], "edges":[] }
    for index, ship1 in enumerate(ships):
        nodes += ship1.get_node()
        for ship2 in ships[index+1:]:
            edges += get_or_create_edge(ship1, ship2)
            
        
    return graph
