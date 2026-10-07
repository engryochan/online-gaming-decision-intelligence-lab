-- Source records, not unique legal entities.
SELECT * FROM market_listing_counts ORDER BY market_iso_alpha2;

-- Preserve each source's issuer identifier without merging by name.
SELECT json_extract(fields_json, '$.exchange') AS exchange,
       json_extract(fields_json, '$.source_issuer_id') AS source_issuer_id,
       json_extract(fields_json, '$.issuer_name') AS source_name
FROM raw_records
WHERE namespace='FINANCIAL_B05' AND source_table='registry_tmx_issuer_records';

-- Source-level count discrepancy remains visible.
SELECT fields_json FROM raw_records
WHERE namespace='FINANCIAL_B05' AND source_table='nzx_count_reconciliation';

-- Currency and regulatory records retained from previous batches.
SELECT COUNT(*) AS currency_source_entries FROM currency_entries;
SELECT COUNT(*) AS fsa_registered_firms FROM fsa_firms;
