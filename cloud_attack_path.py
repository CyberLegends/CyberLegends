"""CL-RT-04: evidence-linked paths through a supplied cloud relationship graph."""
from collections import deque
from common import cli, require

DEMO = {'nodes': ['internet', 'web', 'service-role', 'data-store'], 'start': 'internet', 'targets': ['data-store'],
        'edges': [{'id': 'e1', 'source': 'internet', 'target': 'web', 'evidence': 'fixture/security-group-1'},
                  {'id': 'e2', 'source': 'web', 'target': 'service-role', 'evidence': 'fixture/role-binding'},
                  {'id': 'e3', 'source': 'service-role', 'target': 'data-store', 'evidence': 'fixture/data-policy'}],
        'remove_edges': ['e3']}


def paths(data, removed):
    nodes = set(data['nodes'])
    require(data['start'] in nodes and set(data['targets']) <= nodes, 'Unknown start or target')
    require(len(nodes) <= 1000 and len(data['edges']) <= 5000, 'Graph too large')
    graph = {n: [] for n in nodes}
    for edge in data['edges']:
        require(edge['source'] in nodes and edge['target'] in nodes, 'Unknown edge node')
        require(bool(edge.get('evidence')), 'Each edge needs evidence')
        if edge['id'] not in removed and not edge.get('denied', False):
            graph[edge['source']].append(edge)
    queue = deque([(data['start'], [])])
    visited, found = {data['start']}, []
    while queue:
        node, path = queue.popleft()
        if node in data['targets']:
            found.append({'target': node, 'edges': [e['id'] for e in path],
                          'evidence': [e['evidence'] for e in path]})
        for edge in graph[node]:
            if edge['target'] not in visited:
                visited.add(edge['target'])
                queue.append((edge['target'], path + [edge]))
    return found


def run(data):
    ids = {e['id'] for e in data['edges']}
    require(len(ids) == len(data['edges']), 'Duplicate edge IDs')
    removed = set(data.get('remove_edges', []))
    require(removed <= ids, 'Unknown remediation edge')
    return {'before': paths(data, set()), 'after': paths(data, removed),
            'limitation': 'One shortest path per target in supplied graph; not a cloud IAM policy interpreter or proof of exploitability.'}

if __name__ == '__main__':
    cli(run, DEMO)
