from mitm_tooling.definition import MITM
from mitm_tooling.representation import Header
from ..definitions import SupersetDefFile, StrUUID, DatasetIdentifier, \
    DashboardIdentifier, ChartIdentifier, \
    MitMDatasetIdentifier, SupersetObjectMixin

RelatedTable = DatasetIdentifier
RelatedSlice = ChartIdentifier
RelatedDashboard = DashboardIdentifier


class SupersetMitMDatasetDef(SupersetObjectMixin, SupersetDefFile):
    uuid: StrUUID
    dataset_name: str
    mitm: MITM
    mitm_header: Header | None = None
    database_uuid: StrUUID
    tables: list[RelatedTable] | None = None
    slices: list[RelatedSlice] | None = None
    dashboards: list[RelatedDashboard] | None = None
    version: str = '1.0.0'

    @property
    def identifier(self) -> MitMDatasetIdentifier:
        return MitMDatasetIdentifier(uuid=self.uuid, dataset_name=self.dataset_name, id=-1)

    @property
    def filename(self) -> str:
        return self.dataset_name
