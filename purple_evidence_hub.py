"""CL-RT-06: correlate synthetic run IDs, alerts and escalation with coverage limits."""
from common import cli, require

DEMO = {'runs': [{'id': 'r1', 'start': 100, 'end': 130, 'executed': True, 'telemetry_complete': True},
                 {'id': 'r2', 'start': 200, 'end': 230, 'executed': True, 'telemetry_complete': True},
                 {'id': 'r3', 'start': 300, 'end': 330, 'executed': True, 'telemetry_complete': False}],
        'alerts': [{'id': 'a1', 'run': 'r1', 'timestamp': 105, 'escalated': True},
                   {'id': 'a1', 'run': 'r1', 'timestamp': 105, 'escalated': True}]}


def run(data):
    require(len({r['id'] for r in data['runs']}) == len(data['runs']), 'Duplicate run IDs')
    results, eligible, detected = [], 0, 0
    for case in data['runs']:
        require(case['end'] >= case['start'], 'Invalid run window')
        if not case['executed'] or not case['telemetry_complete']:
            results.append({'id': case['id'], 'status': 'not-evaluable'})
            continue
        eligible += 1
        matches = {a['id']: a for a in data['alerts'] if a['run'] == case['id'] and case['start'] <= a['timestamp'] <= case['end']}
        if matches:
            detected += 1
        results.append({'id': case['id'], 'status': 'detected' if matches else 'missed',
                        'alert_ids': sorted(matches),
                        'latency': min(a['timestamp'] - case['start'] for a in matches.values()) if matches else None,
                        'escalated': any(a.get('escalated', False) for a in matches.values())})
    return {'runs': results, 'eligible_runs': eligible, 'coverage': detected / eligible if eligible else None,
            'limitation': 'Caller-supplied run IDs and synchronized timestamps are assumed; excluded runs are not successes.'}

if __name__ == '__main__':
    cli(run, DEMO)
