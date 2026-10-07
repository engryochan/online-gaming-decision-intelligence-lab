-- entities_at_1800
SELECT name,source_type,from_year,to_year FROM historical_features WHERE from_year<=1800 AND to_year>=1800 ORDER BY name;
-- source_type_counts
SELECT source_type,COUNT(*) FROM historical_features GROUP BY source_type;
-- financial_tasks
SELECT stream,COUNT(*) FROM financial_workstreams GROUP BY stream;
-- source_cow_counts
SELECT source,COUNT(*) FROM source_records GROUP BY source;
-- live_country_union
SELECT COUNT(*) FROM current_country_checks;
