-- Read-only candidate filter; not training authorization. Bind observation_id.
SELECT o.observation_id FROM registry_observation o
 JOIN registry_entity e USING(entity_id)
 JOIN registry_source s ON s.source_id=o.source_id
 JOIN registry_license_policy p ON p.policy_id=s.policy_id
 JOIN registry_claim c ON c.claim_id=o.claim_id
 WHERE e.world_domain='REAL-TWIN' AND o.evidence_state IN ('VERIFIED','OBSERVED')
 AND o.value IS NOT NULL AND trim(o.unit)<>''
 AND trim(o.method_id)<>'' AND upper(trim(o.method_id))<>'UNKNOWN'
 AND p.ml_training_allowed=1 AND s.access_class='PUBLIC'
 AND c.claim_status IN ('VERIFIED','OBSERVED')
 AND c.evidence_state IN ('VERIFIED','OBSERVED')
 AND c.subject_entity_id=o.entity_id AND c.source_id=o.source_id
 AND o.observation_id=?;
