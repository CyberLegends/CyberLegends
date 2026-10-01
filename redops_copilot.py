"""CL-RT-01: deterministic scope/approval validator, with optional AI explanation."""
from common import cli, require

DEMO = {'now': 1000, 'allowed_assets': ['lab-web'], 'allowed_actions': ['simulate-login'],
        'approvals': [{'id': 'a1', 'reviewer': 'reviewer-1', 'asset': 'lab-web',
                       'action': 'simulate-login', 'expires': 1100, 'revoked': False}],
        'jobs': [{'id': 'j1', 'asset': 'lab-web', 'action': 'simulate-login', 'approval': 'a1'},
                 {'id': 'j2', 'asset': 'external-host', 'action': 'simulate-login', 'approval': 'a1'}]}


def run(data):
    now = data['now']
    approvals = data['approvals']
    require(len({a['id'] for a in approvals}) == len(approvals), 'Duplicate approval IDs')
    require(len({j['id'] for j in data['jobs']}) == len(data['jobs']), 'Duplicate job IDs')
    by_id = {a['id']: a for a in approvals}
    decisions = []
    for job in data['jobs']:
        reasons = []
        if job['asset'] not in data['allowed_assets']:
            reasons.append('asset-out-of-scope')
        if job['action'] not in data['allowed_actions']:
            reasons.append('action-out-of-scope')
        approval = by_id.get(job.get('approval'))
        if not approval:
            reasons.append('missing-approval')
        else:
            if approval.get('revoked'):
                reasons.append('revoked-approval')
            if not approval.get('reviewer') or approval['expires'] <= now:
                reasons.append('invalid-or-expired-approval')
            if (approval['asset'], approval['action']) != (job['asset'], job['action']):
                reasons.append('approval-scope-mismatch')
        decisions.append({'job': job['id'], 'allowed': not reasons, 'reasons': reasons})
    return {'decisions': decisions, 'execution': 'planning-only; no jobs executed'}

if __name__ == '__main__':
    cli(run, DEMO)
