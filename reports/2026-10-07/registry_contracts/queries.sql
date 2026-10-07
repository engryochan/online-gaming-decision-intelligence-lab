PRAGMA query_only=ON;
SELECT * FROM v_country_evidence_coverage ORDER BY iso_alpha2;
SELECT claim_id,entity_id,evidence_state,verification_scope FROM v_claims_with_source WHERE source_id='';
SELECT metric_id,display_name,metric_name,numeric_value,unit,statistic,conditions,verification_scope FROM v_metrics_with_context;
SELECT * FROM v_neuro_bandwidth_missing;
