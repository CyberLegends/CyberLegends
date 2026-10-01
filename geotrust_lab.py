"""CL-RT-10: circular geofence state machine with replay/staleness/accuracy controls."""
import math
from common import cli, require

DEMO = {'now': 1000, 'max_age': 100, 'future_tolerance': 5, 'center': [31.5, 74.3],
        'radius_m': 500, 'hysteresis_m': 20, 'max_accuracy_m': 50, 'max_speed_mps': 100,
        'registered_devices': ['virtual-truck'], 'messages': [
            {'id': 'm1', 'device': 'virtual-truck', 'timestamp': 910, 'lat': 31.51, 'lon': 74.3, 'accuracy_m': 5},
            {'id': 'm2', 'device': 'virtual-truck', 'timestamp': 970, 'lat': 31.5, 'lon': 74.3, 'accuracy_m': 5},
            {'id': 'm2', 'device': 'virtual-truck', 'timestamp': 970, 'lat': 31.5, 'lon': 74.3, 'accuracy_m': 5}]}


def distance(a, b):
    lat1, lat2 = math.radians(a[0]), math.radians(b[0])
    dlat, dlon = lat2 - lat1, math.radians(b[1] - a[1])
    v = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return 6371000 * 2 * math.asin(min(1, math.sqrt(v)))


def run(data):
    require(0 <= data['hysteresis_m'] < data['radius_m'], 'Invalid radius or hysteresis')
    seen, last, states, results = set(), {}, {}, []
    for message in data['messages']:
        key = (message['device'], message['id'])
        timestamp = message['timestamp']
        point = (message['lat'], message['lon'])
        accuracy = message['accuracy_m']
        require(all(isinstance(x, (int, float)) and math.isfinite(x) for x in (*point, accuracy, timestamp)), 'Nonfinite telemetry')
        require(-90 <= point[0] <= 90 and -180 <= point[1] <= 180 and accuracy >= 0, 'Invalid coordinates or accuracy')
        reason = None
        if message['device'] not in data['registered_devices']:
            reason = 'unregistered-device'
        elif key in seen:
            reason = 'duplicate-message'
        elif not data['now'] - data['max_age'] <= timestamp <= data['now'] + data.get('future_tolerance', 0):
            reason = 'stale-or-future'
        elif accuracy > data['max_accuracy_m']:
            reason = 'uncertain-location'
        previous = last.get(message['device'])
        if not reason and previous:
            if timestamp <= previous['timestamp']:
                reason = 'out-of-order'
            elif distance(point, (previous['lat'], previous['lon'])) / (timestamp - previous['timestamp']) > data['max_speed_mps']:
                reason = 'implausible-speed'
        if reason:
            results.append({'id': message['id'], 'accepted': False, 'reason': reason})
            continue
        seen.add(key)
        last[message['device']] = message
        d = distance(point, data['center'])
        before = states.get(message['device'], 'unknown')
        after = before
        if d + accuracy < data['radius_m'] - data['hysteresis_m']:
            after = 'inside'
        elif d - accuracy > data['radius_m'] + data['hysteresis_m']:
            after = 'outside'
        event = None if before == after or before == 'unknown' else ('entry' if after == 'inside' else 'exit')
        states[message['device']] = after
        results.append({'id': message['id'], 'accepted': True, 'state': after, 'event': event, 'distance_m': round(d, 2)})
    return {'messages': results, 'limitation': 'Device registration is simulated, not authentication. In-memory replay state and circular fences only; no real asset tracking.'}

if __name__ == '__main__':
    cli(run, DEMO)
