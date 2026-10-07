-- esma_status
SELECT source_status,COUNT(*) FROM esma_entities GROUP BY source_status;
-- esma_office
SELECT office_type,COUNT(*) FROM esma_entities GROUP BY office_type;
-- workstreams
SELECT stream,COUNT(*) FROM country_workstreams GROUP BY stream;
-- missing_activity_parent
SELECT COUNT(*) FROM esma_activities a LEFT JOIN esma_entities e ON a.parent_record_id=e.record_id WHERE e.record_id IS NULL;
-- activity_types
SELECT record_type,COUNT(*) FROM esma_activities GROUP BY record_type;
-- listing_count
SELECT COUNT(*) FROM listing_records;
-- raw_count
SELECT COUNT(*) FROM raw_records;
-- currency_count
SELECT COUNT(*) FROM currency_entries;
-- fsa_count
SELECT COUNT(*) FROM fsa_firms;
