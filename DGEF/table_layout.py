"""One shared export classification for migration and subsequent builds."""
def table_category(name):
    if name in {'registry_country_area','registry_admin_unit','registry_settlement','registry_infrastructure'}:
        return '03_geography_infrastructure'
    if name in {'registry_legal_entity','registry_public_body','registry_research_org','registry_public_facility','registry_person_public_role'}:
        return '04_organizations_public_roles'
    if name in {'registry_celestial_object','registry_astrobiology_evidence'} or name.startswith('registry_space_') or name == 'registry_ground_facility_public':
        return '05_space_science'
    if name in {'registry_entity_location','registry_spatial_frame','registry_ephemeris_solution'}:
        return '06_spacetime'
    if name in {'registry_virtual_world','registry_virtual_entity','registry_simulation_run','registry_synthetic_population'}:
        return '07_simulation_virtual'
    if name == 'staging_service_catalogue':
        return '08_service_staging'
    if name in {'registry_source','registry_dataset','registry_claim','registry_observation','registry_evidence_link','registry_ingest_record'}:
        return '02_sources_evidence'
    if name in {'registry_license_policy','registry_coverage','registry_adapter_contract','registry_schema_version'}:
        return '09_governance_coverage'
    return '01_identity_relations'
