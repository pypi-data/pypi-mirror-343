from abc import ABC, abstractmethod
from typing import Self, Type, Callable

from mitm_tooling.representation import Header, SQLRepresentationSchema, mk_sql_rep_schema
from .base import DashboardCreator
from ...asset_bundles.asset_bundles import SupersetVisualizationBundle
from ...asset_bundles.identifier import MitMDatasetIdentifierBundle
from ...definitions import MitMDatasetIdentifier

DashboardCreatorConstructor = Callable[[Header, MitMDatasetIdentifier | None], DashboardCreator]


class MitMDashboardCreator(DashboardCreator, ABC):
    def __init__(self, header: Header, sql_rep_schema: SQLRepresentationSchema | None = None, **kwargs):
        super().__init__(**kwargs)
        self.header = header
        self.sql_rep_schema = sql_rep_schema or mk_sql_rep_schema(header)


class VisualizationsCreator(ABC):

    def __init__(self, header: Header, **kwargs):
        super().__init__(**kwargs)
        self.header = header

    @property
    @abstractmethod
    def dashboard_creator_constructors(self) -> dict[str, DashboardCreatorConstructor]:
        ...

    def mk_dashboard_bundles(self, mitm_dataset_identifiers: MitMDatasetIdentifierBundle) -> dict[
        str, SupersetVisualizationBundle]:
        creators = {name: constr(self.header, mitm_dataset_identifiers.mitm_dataset) for name, constr in
                    self.dashboard_creator_constructors.items()}

        def get_dash_id(creator_name, viz_name):
            return mitm_dataset_identifiers.viz_id_map.get(creator_name, {}).get(viz_name)

        ds_id_map = mitm_dataset_identifiers.ds_id_map
        bundles = {name: creator.mk_bundle(ds_id_map, get_dash_id(name, creator.viz_name), collection_name=name) for
                   name, creator in creators.items()}
        return bundles

    def mk_bundle(self,
                  mitm_dataset_identifiers: MitMDatasetIdentifierBundle) -> SupersetVisualizationBundle:
        bundle_map = self.mk_dashboard_bundles(mitm_dataset_identifiers)
        return SupersetVisualizationBundle.combine(*bundle_map.values())

    @classmethod
    def wrap_single(cls, name: str, dashboard_creator_constr: DashboardCreatorConstructor) -> Type[Self]:
        dashboard_creator_constr_ = dashboard_creator_constr
        name_ = name

        class ConcreteVisualizationCreator(cls):
            @property
            def dashboard_creator_constructors(self) -> dict[str, DashboardCreatorConstructor]:
                return {name_: dashboard_creator_constr_}

        return ConcreteVisualizationCreator

    @classmethod
    def empty(cls) -> Type[Self]:
        class ConcreteVisualizationCreator(cls):
            @property
            def dashboard_creator_constructors(self) -> dict[str, DashboardCreatorConstructor]:
                return {}

        return ConcreteVisualizationCreator
