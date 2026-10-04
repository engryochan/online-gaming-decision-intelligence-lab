-- 书同文：按ISO外号桥接，不以公司或用户所在地限制全集。
-- Supply :country_iso as a parameter; NULL enumerates every country/area.
SELECT c.iso_alpha2, c.iso_alpha3, a.subdivision_code, a.name, a.evidence_state
FROM registry_country_area AS c
LEFT JOIN registry_admin_unit AS a ON a.country_entity_id=c.entity_id
WHERE :country_iso IS NULL OR c.iso_alpha2=:country_iso
ORDER BY c.iso_alpha2, a.subdivision_code;

-- 知未详：分母未知时不造覆盖率。
SELECT c.iso_alpha2, g.layer, g.status, g.numerator, g.denominator,
       CASE WHEN g.denominator>0 AND g.numerator IS NOT NULL
            THEN 1.0*g.numerator/g.denominator ELSE NULL END AS coverage_ratio
FROM registry_coverage AS g
JOIN registry_country_area AS c ON c.entity_id=g.country_entity_id;

-- 模型无户籍权：待消歧供应商目录与实体正籍分开。
SELECT catalogue_id,name,verification_status,verified_scope,resolution_status
FROM staging_service_catalogue
WHERE resolution_status='PENDING';

-- 有据而后用数：只读已通过必要闸门的接口；本轮零行是正确结果。
SELECT * FROM v_model_features_approved;
