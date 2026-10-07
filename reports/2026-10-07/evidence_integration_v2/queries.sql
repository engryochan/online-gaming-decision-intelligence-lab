-- Read-only snapshot queries. Evidence scopes and units are not interchangeable.
SELECT * FROM claim_scope_counts ORDER BY batch,evidence_state,verification_scope;
SELECT batch,claim_id,entity_id,verification_scope,claim FROM regulatory_claims;
SELECT batch,metric_id,entity_id,metric_name,value,unit,statistic,conditions,verification_scope FROM study_metrics WHERE batch IN ('EVIDENCE_B06','EVIDENCE_B07');
SELECT * FROM publication_correction_records;
SELECT * FROM entity_evidence_counts WHERE entity_id IN ('FRO0132','GTO0033','GTO0034','GTO0035','GTO0044','OEB07E01');
-- Inspect all source metadata for a scoped claim.
SELECT c.batch,c.claim_id,c.claim,c.verification_scope,s.payload FROM claims c LEFT JOIN sources s ON c.batch=s.batch AND c.source_id=s.source_id WHERE c.entity_id='GTO0044';
