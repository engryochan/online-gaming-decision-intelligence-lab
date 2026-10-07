-- Counts represent source records, not unique legal companies.
SELECT * FROM market_listing_counts ORDER BY market_iso_alpha2;
SELECT status,COUNT(*) FROM mic_registry GROUP BY status ORDER BY status;
SELECT COUNT(*) AS missing_operating_mic
FROM mic_registry child LEFT JOIN mic_registry parent
ON child.operating_MIC=parent.MIC WHERE parent.MIC IS NULL;
SELECT source_row,fields_json FROM raw_records
WHERE namespace='FINANCIAL_B06' AND source_table='registry_tw_broker_source_profiles';
SELECT source_row,fields_json FROM raw_records
WHERE namespace='FINANCIAL_B06' AND source_table='broker_company_identifier_links';
SELECT COUNT(*) FROM fsa_firms;
SELECT COUNT(*) FROM currency_entries;
