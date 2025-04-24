from typing import Self
from uuid import UUID

import pydantic

from mitm_tooling.transformation.superset.definitions import DatasetIdentifierMap, \
    DatabaseIdentifier, MitMDatasetIdentifier, BaseSupersetDefinition, DashboardIdentifier, SupersetMitMDatasetDef
from mitm_tooling.utilities.python_utils import deep_merge_dicts

VizDashboardIdentifierMap = dict[str, DashboardIdentifier]
VizCollectionIdentifierMap = dict[str, VizDashboardIdentifierMap]


class DatasourceIdentifierBundle(BaseSupersetDefinition):
    database: DatabaseIdentifier | None = None
    ds_id_map: DatasetIdentifierMap = pydantic.Field(default_factory=dict)

    @property
    def database_uuid(self) -> UUID | None:
        if self.database is not None:
            return self.database.uuid

    @classmethod
    def from_mitm_dataset(cls, mitm_dataset: SupersetMitMDatasetDef) -> Self:
        return cls(database=DatabaseIdentifier(uuid=mitm_dataset.database_uuid),
                   ds_id_map={t.table_name: t for t in (mitm_dataset.tables or [])})


class MitMDatasetIdentifierBundle(DatasourceIdentifierBundle):
    mitm_dataset: MitMDatasetIdentifier | None = None
    viz_id_map: VizCollectionIdentifierMap = pydantic.Field(default_factory=dict)

    @property
    def mitm_dataset_uuid(self) -> UUID | None:
        if self.mitm_dataset is not None:
            return self.mitm_dataset.uuid

    @classmethod
    def from_mitm_dataset(cls, mitm_dataset: SupersetMitMDatasetDef) -> Self:
        return cls(mitm_dataset=mitm_dataset.identifier,
                   database=DatabaseIdentifier(uuid=mitm_dataset.database_uuid),
                   ds_id_map={t.table_name: t for t in (mitm_dataset.tables or [])},
                   viz_id_map={
                       'default': {dash.dashboard_title: dash for dash in
                                   (mitm_dataset.dashboards or [])}})

    def with_visualizations(self, *viz_id_maps: VizCollectionIdentifierMap) -> Self:
        merged_viz_id_map = deep_merge_dicts(self.viz_id_map, *viz_id_maps)
        return self.model_copy(update=dict(viz_id_map=merged_viz_id_map), deep=True)