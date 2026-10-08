-- listing_sources
SELECT namespace,COUNT(*) FROM listing_records GROUP BY namespace;
-- members
SELECT COUNT(*) FROM euronext_trading_members;
-- historical_features
SELECT source_type,COUNT(*) FROM historical_feature_snapshots GROUP BY source_type;
-- historical_relationships
SELECT COUNT(*) FROM historical_source_relationships;
-- historical_gaps
SELECT COUNT(*) FROM historical_interval_gaps;
-- currency_chronology
SELECT COUNT(*) FROM historical_currency_withdrawal_dates;
-- country_tasks
SELECT stream,COUNT(*) FROM country_workstreams GROUP BY stream;
