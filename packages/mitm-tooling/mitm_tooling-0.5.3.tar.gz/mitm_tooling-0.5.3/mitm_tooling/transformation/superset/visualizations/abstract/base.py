from abc import ABC, abstractmethod
from typing import Self, Type, Callable

from mitm_tooling.representation import TableName, Header, SQLRepresentationSchema
from ...asset_bundles.asset_bundles import SupersetVisualizationBundle
from ...definitions import DatasetIdentifier, SupersetChartDef, \
    SupersetDashboardDef, DatasetIdentifierMap, DashboardIdentifier, MitMDatasetIdentifier

ChartDefCollection = dict[str, SupersetChartDef]
DashboardDefCollection = dict[str, SupersetDashboardDef]


class ChartCreator(ABC):

    @abstractmethod
    def mk_chart(self, dataset_identifier: DatasetIdentifier) -> SupersetChartDef:
        ...


class ChartCollectionCreator(ABC):

    @abstractmethod
    def mk_chart_collection(self, ds_id_map: DatasetIdentifierMap) -> ChartDefCollection:
        ...

    @classmethod
    def cls_from_dict(cls, chart_creators: dict[str, tuple[TableName, ChartCreator]]) -> Type[Self]:
        chart_creators = dict(chart_creators)

        class ConcreteChartCollectionCreator(cls):

            def __init__(self, header: Header):
                super().__init__(header)
                self._chart_creators = chart_creators

            def mk_chart_collection(self, ds_id_map: DatasetIdentifierMap) -> ChartDefCollection:
                return {name: cc.mk_chart(ds_id_map[table_name]) for name, (table_name, cc) in
                        self._chart_creators.items()}

        return ConcreteChartCollectionCreator


class DashboardCreator(ABC):

    @property
    def viz_name(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def chart_collection_creator(self) -> ChartCollectionCreator:
        ...

    @abstractmethod
    def mk_dashboard(self,
                     chart_collection: ChartDefCollection,
                     dashboard_identifier: DashboardIdentifier| None = None) -> SupersetDashboardDef:
        ...

    def mk_bundle(self,
                  ds_id_map: DatasetIdentifierMap,
                  dashboard_identifier: DashboardIdentifier | None = None, collection_name: str = 'default') -> SupersetVisualizationBundle:
        chart_collection = self.chart_collection_creator.mk_chart_collection(ds_id_map)
        dashboard = self.mk_dashboard(chart_collection, dashboard_identifier)
        viz_name = self.viz_name
        return SupersetVisualizationBundle(charts=list(chart_collection.values()),
                                           dashboards=[dashboard],
                                           viz_collections={
                                               collection_name: {viz_name: dashboard.identifier}})


