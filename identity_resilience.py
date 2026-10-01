"""CL-RT-05: synthetic role transition and expected-audit-event validation."""
from common import cli, require

DEMO = {'users': {'alice': 'user', 'sam': 'service'},
        'allowed_transitions': [['user', 'reader'], ['service', 'service']],
        'scenarios': [{'id': 's1', 'user': 'alice', 'to_role': 'reader', 'observed_allowed': True, 'audit_events': ['identity.transition.allowed']},
                      {'id': 's2', 'user': 'sam', 'to_role': 'admin', 'observed_allowed': True, 'audit_events': []}]}


def run(data):
    baseline = dict(data['users'])
    permitted = {tuple(pair) for pair in data['allowed_transitions']}
    results = []
    for case in data['scenarios']:
        require(case['user'] in baseline, 'Unknown synthetic identity')
        require(isinstance(case['observed_allowed'], bool), 'observed_allowed must be boolean')
        expected = (baseline[case['user']], case['to_role']) in permitted
        event = 'identity.transition.allowed' if expected else 'identity.transition.denied'
        results.append({'scenario': case['id'], 'expected_allowed': expected,
                        'control_pass': expected == case['observed_allowed'],
                        'expected_event': event, 'audit_pass': event in case['audit_events']})
    # All scenarios use baseline identities: no directory or production state is modified.
    return {'scenarios': results, 'baseline_unchanged': baseline == data['users'],
            'control_failures': sum(not r['control_pass'] for r in results),
            'limitation': 'Validates supplied observations and role rules; no live directory integration.'}

if __name__ == '__main__':
    cli(run, DEMO)
