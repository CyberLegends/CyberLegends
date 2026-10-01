"""Offline security regression tests. Run: python -m unittest -v test_projects.py"""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import redops_copilot as redops
import llm_assurance_lab as llm
import agent_boundary_guard as agent
import cloud_attack_path as cloud
import identity_resilience as identity
import purple_evidence_hub as purple
import rag_trust_lab as rag
import ai_supply_chain as supply
import industrial_cyber_range as ot
import geotrust_lab as geo


class LabTests(unittest.TestCase):
    def test_redops_scope_binding(self):
        verdict = redops.run(redops.DEMO)['decisions']
        self.assertTrue(verdict[0]['allowed'])
        self.assertIn('approval-scope-mismatch', verdict[1]['reasons'])

    def test_expired_and_revoked_approval(self):
        data = copy.deepcopy(redops.DEMO)
        data['approvals'][0].update(expires=data['now'], revoked=True)
        reasons = redops.run(data)['decisions'][0]['reasons']
        self.assertIn('revoked-approval', reasons)
        self.assertIn('invalid-or-expired-approval', reasons)

    def test_ambiguous_approval_denied(self):
        data = copy.deepcopy(redops.DEMO)
        data['approvals'] *= 2
        with self.assertRaises(ValueError):
            redops.run(data)

    def test_canary_and_benign_metrics_separate(self):
        result = llm.run(llm.DEMO)
        self.assertEqual(result['security_failure_rate'], 0.5)
        self.assertEqual(result['benign_completion_rate'], 1)

    def test_empty_security_marker_rejected(self):
        data = {'cases': [{'id': 'x', 'kind': 'security', 'response': '', 'forbidden': ['']}]}
        with self.assertRaises(ValueError):
            llm.run(data)

    def test_live_model_adapter_uses_real_response(self):
        with patch('llm_assurance_lab.local_model', return_value='CANARY-LAB-17'):
            result = llm.live({'cases': [llm.DEMO['cases'][0]]}, 'mock-test-only')
        self.assertEqual(result['security_failure_rate'], 1)
        self.assertIn('response_source', result)

    def test_agent_cross_tenant_and_replay(self):
        result = agent.run(agent.DEMO)
        self.assertFalse(result['decisions'][1]['allowed'])
        self.assertIn('approval-replay', result['decisions'][3]['reasons'])
        self.assertEqual(result['mock_state']['doc-a'], 'demo')

    def test_agent_untrusted_arguments_cannot_grant_permission(self):
        data = copy.deepcopy(agent.DEMO)
        data['requests'] = [{'id': 'x', 'action': 'write', 'resource': 'doc-a', 'value': 'x', 'approved': True}]
        result = agent.run(data)
        self.assertFalse(result['decisions'][0]['allowed'])
        self.assertEqual(result['mock_state'], {})

    def test_agent_expiry_exact_boundary(self):
        data = copy.deepcopy(agent.DEMO)
        data['now'] = 150
        self.assertFalse(agent.run(data)['decisions'][2]['allowed'])

    def test_cloud_remediation_removes_path(self):
        result = cloud.run(cloud.DEMO)
        self.assertEqual(result['before'][0]['edges'], ['e1', 'e2', 'e3'])
        self.assertEqual(result['after'], [])

    def test_cloud_deny_and_cycle(self):
        data = copy.deepcopy(cloud.DEMO)
        data['edges'][1]['denied'] = True
        data['edges'].append({'id': 'cycle', 'source': 'web', 'target': 'internet', 'evidence': 'fixture'})
        self.assertEqual(cloud.run(data)['before'], [])

    def test_cloud_missing_evidence(self):
        data = copy.deepcopy(cloud.DEMO)
        data['edges'][0]['evidence'] = ''
        with self.assertRaises(ValueError):
            cloud.run(data)

    def test_identity_control_and_logging_gap(self):
        result = identity.run(identity.DEMO)
        self.assertEqual(result['control_failures'], 1)
        self.assertFalse(result['scenarios'][1]['audit_pass'])
        self.assertTrue(result['baseline_unchanged'])

    def test_identity_unknown_user(self):
        data = copy.deepcopy(identity.DEMO)
        data['scenarios'][0]['user'] = 'unknown'
        with self.assertRaises(ValueError):
            identity.run(data)

    def test_purple_incomplete_run_not_success(self):
        result = purple.run(purple.DEMO)
        self.assertEqual(result['coverage'], 0.5)
        self.assertEqual(result['eligible_runs'], 2)
        self.assertEqual(result['runs'][0]['alert_ids'], ['a1'])
        self.assertEqual(result['runs'][0]['latency'], 5)

    def test_purple_outside_window_does_not_count(self):
        data = copy.deepcopy(purple.DEMO)
        for alert in data['alerts']:
            alert['timestamp'] = 99
        self.assertEqual(purple.run(data)['coverage'], 0)

    def test_purple_no_evaluable_data_is_unknown(self):
        self.assertIsNone(purple.run({'runs': [], 'alerts': []})['coverage'])

    def test_rag_tenant_and_role_isolation(self):
        result = rag.run(rag.DEMO)
        self.assertTrue(all(q['isolation_pass'] for q in result['queries']))
        self.assertNotIn('a', result['queries'][1]['retrieved_ids'])

    def test_rag_delete_or_revoke_takes_effect(self):
        data = copy.deepcopy(rag.DEMO)
        data['documents'][1]['deleted'] = True
        self.assertNotIn('a', rag.run(data)['queries'][0]['retrieved_ids'])
        data['documents'][1]['deleted'] = False
        data['documents'][1]['roles'] = ['admin']
        self.assertNotIn('a', rag.run(data)['queries'][0]['retrieved_ids'])

    def test_supply_tampering(self):
        result = supply.run(supply.DEMO)['artifacts']
        self.assertTrue(result[0]['accepted'])
        self.assertEqual(set(result[1]['reasons']), {'hash-mismatch', 'unapproved-source', 'missing-provenance-label'})

    def test_supply_path_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            data = {'root': directory, 'approved_sources': [], 'artifacts': [{'id': 'x', 'path': '../outside', 'sha256': '', 'source': ''}]}
            with self.assertRaises(ValueError):
                supply.run(data)

    def test_supply_file_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, 'safe.txt').write_text('abc')
            artifact = {k: v for k, v in supply.DEMO['artifacts'][0].items() if k != 'content'}
            artifact['path'] = 'safe.txt'
            result = supply.run({'root': directory, 'approved_sources': ['internal-lab'], 'artifacts': [artifact]})
            self.assertTrue(result['artifacts'][0]['accepted'])

    def test_ot_stop_latches_until_reset(self):
        result = ot.run(ot.DEMO)
        self.assertFalse(result['it_can_reach_ot'])
        self.assertEqual([x['stopped'] for x in result['process_events']], [False, True, True, False])

    def test_ot_production_rejected(self):
        data = copy.deepcopy(ot.DEMO)
        data['production_attached'] = True
        with self.assertRaises(ValueError):
            ot.run(data)

    def test_ot_indirect_path_detected(self):
        data = copy.deepcopy(ot.DEMO)
        data['connections'].append(['dmz', 'ot'])
        self.assertTrue(ot.run(data)['it_can_reach_ot'])

    def test_geo_entry_and_deduplication(self):
        result = geo.run(geo.DEMO)['messages']
        self.assertEqual(result[1]['event'], 'entry')
        self.assertEqual(result[2]['reason'], 'duplicate-message')

    def test_geo_stale_and_future(self):
        data = copy.deepcopy(geo.DEMO)
        data['messages'][0]['timestamp'] = 899
        data['messages'][1]['timestamp'] = 1006
        result = geo.run(data)['messages']
        self.assertEqual(result[0]['reason'], 'stale-or-future')
        self.assertEqual(result[1]['reason'], 'stale-or-future')

    def test_geo_implausible_jump_does_not_change_state(self):
        data = copy.deepcopy(geo.DEMO)
        data['messages'][1]['timestamp'] = 911
        self.assertEqual(geo.run(data)['messages'][1]['reason'], 'implausible-speed')

    def test_geo_nonfinite_coordinates_rejected(self):
        data = copy.deepcopy(geo.DEMO)
        data['messages'][0]['lat'] = float('nan')
        with self.assertRaises(ValueError):
            geo.run(data)

    def test_geo_boundary_uncertainty_keeps_state(self):
        data = copy.deepcopy(geo.DEMO)
        data['radius_m'] = geo.distance((31.51, 74.3), data['center'])
        result = geo.run(data)['messages'][0]
        self.assertEqual(result['state'], 'unknown')
        self.assertIsNone(result['event'])

if __name__ == '__main__':
    unittest.main()
