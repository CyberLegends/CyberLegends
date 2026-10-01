"""CL-RT-03: mock tool gateway with tenant, argument, approval and replay checks."""
from common import cli, require

DEMO = {'now': 100, 'tenant': 'tenant-a', 'allowed_actions': ['read', 'write'],
        'resources': {'doc-a': 'tenant-a', 'doc-b': 'tenant-b'},
        'approvals': {'ok': {'tenant': 'tenant-a', 'resource': 'doc-a', 'action': 'write', 'expires': 150}},
        'requests': [{'id': '1', 'action': 'read', 'resource': 'doc-a'},
                     {'id': '2', 'action': 'read', 'resource': 'doc-b'},
                     {'id': '3', 'action': 'write', 'resource': 'doc-a', 'approval': 'ok', 'value': 'demo'},
                     {'id': '4', 'action': 'write', 'resource': 'doc-a', 'approval': 'ok', 'value': 'replay'}]}


def run(data):
    seen, used_approvals, state, decisions = set(), set(), {}, []
    for req in data['requests']:
        reasons = []
        request_id = req['id']
        if request_id in seen:
            reasons.append('duplicate-request')
        seen.add(request_id)
        action, resource = req['action'], req['resource']
        if action not in ('read', 'write') or action not in data['allowed_actions']:
            reasons.append('action-denied')
        if data['resources'].get(resource) != data['tenant']:
            reasons.append('tenant-or-resource-denied')
        if set(req) - {'id', 'action', 'resource', 'approval', 'value'}:
            reasons.append('unexpected-arguments')
        if action == 'write':
            if not isinstance(req.get('value'), str) or len(req['value']) > 1000:
                reasons.append('invalid-value')
            approval_id = req.get('approval')
            approval = data['approvals'].get(approval_id, {})
            expected = (data['tenant'], resource, action)
            actual = (approval.get('tenant'), approval.get('resource'), approval.get('action'))
            if actual != expected or approval.get('expires', 0) <= data['now'] or approval.get('revoked'):
                reasons.append('approval-denied')
            if approval_id in used_approvals:
                reasons.append('approval-replay')
        if not reasons and action == 'write':
            used_approvals.add(req['approval'])
            state[resource] = req['value']
        decisions.append({'id': request_id, 'allowed': not reasons, 'reasons': reasons})
    return {'decisions': decisions, 'mock_state': state, 'external_actions': 0,
            'limitation': 'Replay state is in-memory within this run; production needs durable atomic storage.'}

if __name__ == '__main__':
    cli(run, DEMO)
