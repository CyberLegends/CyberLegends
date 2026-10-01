"""CL-RT-07: ACL-filtered lexical retrieval with tenant, role and deletion fixtures."""
import re
from common import cli, require

DEMO = {'documents': [{'id': 'public', 'tenant': '*', 'roles': [], 'text': 'Appointment opening hours are nine to five.'},
                      {'id': 'a', 'tenant': 'clinic-a', 'roles': ['doctor'], 'text': 'Appointment note CANARY-A synthetic record.'},
                      {'id': 'b', 'tenant': 'clinic-b', 'roles': ['doctor'], 'text': 'Appointment note CANARY-B synthetic record.'}],
        'queries': [{'tenant': 'clinic-a', 'roles': ['doctor'], 'query': 'appointment', 'forbidden': ['CANARY-B']},
                    {'tenant': 'clinic-a', 'roles': ['visitor'], 'query': 'appointment', 'forbidden': ['CANARY-A', 'CANARY-B']}]}


def retrieve(documents, tenant, roles, query):
    words = set(re.findall(r'\w+', query.casefold()))
    matches = []
    for doc in documents:
        if doc.get('deleted') or doc['tenant'] not in ('*', tenant):
            continue
        if doc['roles'] and not set(roles).intersection(doc['roles']):
            continue
        score = len(words.intersection(re.findall(r'\w+', doc['text'].casefold())))
        if score:
            matches.append({'id': doc['id'], 'score': score, 'text': doc['text']})
    return sorted(matches, key=lambda d: (-d['score'], d['id']))[:5]


def run(data):
    require(len({d['id'] for d in data['documents']}) == len(data['documents']), 'Duplicate document IDs')
    results = []
    for query in data['queries']:
        matches = retrieve(data['documents'], query['tenant'], query['roles'], query['query'])
        context = '\n'.join(m['text'] for m in matches)
        results.append({'tenant': query['tenant'], 'retrieved_ids': [m['id'] for m in matches],
                        'context': context,
                        'isolation_pass': not any(x.casefold() in context.casefold() for x in query.get('forbidden', []))})
    return {'queries': results, 'limitation': 'Synthetic lexical retriever, not vector RAG. ACL checked on every query; no cache or answer generation.'}

if __name__ == '__main__':
    cli(run, DEMO)
