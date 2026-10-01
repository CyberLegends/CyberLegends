"""CL-RT-09: abstract IT/OT zone and safe-process simulation, without network access."""
from common import cli, require

DEMO = {'zones': ['it', 'dmz', 'ot', 'historian'], 'connections': [['it', 'dmz'], ['ot', 'historian']],
        'production_attached': False, 'events': [{'kind': 'observe', 'value': 40},
                                               {'kind': 'observe', 'value': 110},
                                               {'kind': 'observe', 'value': 30}, {'kind': 'reset'}],
        'safe_min': 0, 'safe_max': 100}


def reachable(graph, start, target):
    todo, seen = [start], set()
    while todo:
        node = todo.pop()
        if node == target:
            return True
        if node in seen:
            continue
        seen.add(node)
        todo.extend(graph.get(node, []))
    return False


def run(data):
    require(data.get('production_attached') is False, 'Lab must declare no production attachment')
    zones = set(data['zones'])
    require({'it', 'ot'} <= zones, 'it and ot zones required')
    require(data['safe_min'] < data['safe_max'], 'Invalid process safety range')
    graph = {z: [] for z in zones}
    for source, target in data['connections']:
        require(source in zones and target in zones, 'Unknown zone')
        graph[source].append(target)
    stopped, log = False, []
    for event in data['events']:
        kind = event['kind']
        require(kind in ('observe', 'stop', 'reset'), 'Unknown event')
        if kind == 'reset':
            stopped = False
        elif kind == 'stop':
            stopped = True
        elif not data['safe_min'] <= event['value'] <= data['safe_max']:
            stopped = True
        log.append({'event': kind, 'stopped': stopped})
    return {'it_can_reach_ot': reachable(graph, 'it', 'ot'), 'process_events': log,
            'limitation': 'In-memory topology and process model only; not a PLC emulator, packet filter or plant safety validation.'}

if __name__ == '__main__':
    cli(run, DEMO)
