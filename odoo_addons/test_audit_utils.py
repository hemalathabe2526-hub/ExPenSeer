from expense_seer_core.utils.audit_utils import compute_audit_hash


def test_audit_hash_stability():
    h1 = compute_audit_hash('CLAIM-001', 12, '2025-10-04T12:00:00', 'approved', 'OK')
    h2 = compute_audit_hash('CLAIM-001', 12, '2025-10-04T12:00:00', 'approved', 'OK')
    assert h1 == h2


def test_audit_hash_difference():
    h1 = compute_audit_hash('CLAIM-001', 12, '2025-10-04T12:00:00', 'approved', 'OK')
    h2 = compute_audit_hash('CLAIM-002', 12, '2025-10-04T12:00:00', 'approved', 'OK')
    assert h1 != h2
