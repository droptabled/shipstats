from django.shortcuts import render
from django.http import JsonResponse
from . import models
from scraper import models as sm
# Create your views here.

def relations(request):
    nations = sm.Nation.objects.all();
    types = sm.ShipType.objects.all();
    return render(request, 'popularity/allrelations.html', {'range': range(1,11), 'nations': nations, 'types': types})
    
def graphdata(request):
    request_ships = sm.Ship.objects.all()
    if request.GET['type'] and request.GET['type'] != '':
        request_ships = request_ships.filter(type__in = request.GET['type'].split(','))
    if request.GET['nation'] and request.GET['nation'] != '':
        request_ships = request_ships.filter(nation__in = request.GET['nation'].split(','))
    if request.GET['tier'] and request.GET['tier'] != '':
        request_ships = request_ships.filter(tier__in = request.GET['tier'].split(','))
    if request.GET['premium'] and request.GET['premium'] != "0":
        request_ships = request_ships.filter(economy_type=int(request.GET['premium']))

    return JsonResponse(generate_graph(request_ships))

def get_or_create_edge(ship1, ship2):
    edges = models.ShipRelation.objects.filter(ship_primary__in = [ship1, ship2], ship_secondary__in = [ship1, ship2])
    if len(edges) == 0:
        edge = models.ShipRelation.objects.create(ship_primary = ship1, ship_secondary = ship2, playercount = 0)
        edge.update_edge()
    elif len(edges) == 1:
        edge = edges[0]
    else:
        raise ValueError('Mismatched data, extra edges between '+ship1.name+' and '+ship2.name)
    return edge.get_edge()
    
def generate_graph(ships):
    nodes = []
    edges = []
    max_node_size = 0;
    max_edge_strength = 0;
    for index, ship1 in enumerate(ships):
        node = ship1.get_node()
        nodes.append(node)
        if node['playercount'] > max_node_size:
            max_node_size = node['playercount']
        
        for index2, ship2 in enumerate(ships[index+1:]):
            edge = get_or_create_edge(ship1, ship2)
            edge['source'] = index
            edge['target'] = index + index2 + 1
            edges.append(edge)
            if edge['playercount'] > max_edge_strength:
                max_edge_strength = edge['playercount']
    
    #reiterate over nodes and edges to add the relative values
    for node in nodes:
        node['relative_size'] = node['playercount']/max_node_size
    for edge in edges:
        edge['relative_strength'] = edge['playercount']/max_edge_strength
    return { 'nodes': nodes, 'edges': edges }
