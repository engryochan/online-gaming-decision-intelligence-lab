SELECT * FROM market_listing_counts;
SELECT COUNT(*) FROM fsa_firms;
SELECT COUNT(*) FROM currency_entries;
SELECT namespace,source_table,COUNT(*) FROM raw_records GROUP BY namespace,source_table;
SELECT listing_code,source_name FROM listing_records WHERE market_iso_alpha2='AU' ORDER BY listing_code;
