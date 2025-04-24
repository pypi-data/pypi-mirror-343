from mitm_tooling.representation import Header
from .asset_bundles.asset_bundles import SupersetDatasourceBundle, \
    SupersetMitMDatasetBundle
from .asset_bundles.identifier import MitMDatasetIdentifierBundle, DatasourceIdentifierBundle
from .common import DBConnectionInfo, MitMDatasetInfo


def header_into_superset_datasource_bundle(header: Header,
                                           db_conn_info: DBConnectionInfo,
                                           identifiers: DatasourceIdentifierBundle | None = None) -> SupersetDatasourceBundle:
    from ..sql.from_intermediate import header_into_db_meta
    from .from_sql import db_meta_into_superset_datasource_bundle
    db_meta = header_into_db_meta(header, override_schema=db_conn_info.schema_name)
    return db_meta_into_superset_datasource_bundle(db_meta,
                                                   db_conn_info,
                                                   identifiers)


def header_into_mitm_dataset_bundle(header: Header,
                                    db_conn_info: DBConnectionInfo,
                                    dataset_name: str,
                                    identifiers: MitMDatasetIdentifierBundle | None = None) -> SupersetMitMDatasetBundle:
    from ..sql.from_intermediate import header_into_db_meta
    from .from_sql import db_meta_into_mitm_dataset_bundle
    db_meta = header_into_db_meta(header, override_schema=db_conn_info.schema_name)
    info = MitMDatasetInfo(dataset_name=dataset_name, mitm=header.mitm)
    return db_meta_into_mitm_dataset_bundle(db_meta,
                                            db_conn_info,
                                            info,
                                            identifiers)
