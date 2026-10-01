"""CL-RT-08: non-executing SHA-256 artifact integrity and allowlist checks."""
import hashlib
from pathlib import Path
from common import cli, require

DEMO = {'approved_sources': ['internal-lab'], 'artifacts': [
    {'id': 'good', 'source': 'internal-lab', 'content': 'abc', 'sha256': 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad', 'provenance': 'lab-build-1'},
    {'id': 'tampered', 'source': 'unknown', 'content': 'altered', 'sha256': 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad', 'provenance': ''}]}


def run(data):
    root = Path(data.get('root', '.')).resolve()
    results = []
    for artifact in data['artifacts']:
        reasons = []
        require(('content' in artifact) != ('path' in artifact), 'Provide exactly one of content or path')
        if 'path' in artifact:
            path = (root / artifact['path']).resolve()
            require(path.is_relative_to(root), 'Artifact path escapes root')
            require(path.is_file() and path.stat().st_size <= 20_000_000, 'Missing or oversized artifact')
            raw = path.read_bytes()
        else:
            raw = artifact['content'].encode('utf-8')
        actual = hashlib.sha256(raw).hexdigest()
        if actual != artifact['sha256'].lower():
            reasons.append('hash-mismatch')
        if artifact['source'] not in data['approved_sources']:
            reasons.append('unapproved-source')
        if not artifact.get('provenance'):
            reasons.append('missing-provenance-label')
        results.append({'id': artifact['id'], 'accepted': not reasons, 'sha256': actual, 'reasons': reasons})
    return {'artifacts': results, 'limitation': 'Provenance labels are not cryptographically verified. Trusted manifests must be managed separately. No artifact is imported or executed.'}

if __name__ == '__main__':
    cli(run, DEMO)
