-- Read only. Keep scopes separate; never infer a country capability from these counts.
SELECT * FROM claim_scope_counts ORDER BY batch,evidence_state,verification_scope;
SELECT * FROM entity_evidence_counts WHERE entity_id IN ('FRO0021','FRO0022','FRO0054','FRO0123','FRO0132','FRO0195','FRO0196');
SELECT batch,claim_id,entity_id,verification_scope,claim FROM claims WHERE entity_id='FRO0132';
SELECT c.batch,c.claim_id,c.claim,s.payload AS source_metadata FROM claims c LEFT JOIN source_records s ON s.batch=c.batch AND s.source_id=c.source_id WHERE c.entity_id='FRO0123';
