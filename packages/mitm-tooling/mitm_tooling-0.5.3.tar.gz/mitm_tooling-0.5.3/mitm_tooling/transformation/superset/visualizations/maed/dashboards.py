from mitm_tooling.representation import Header, SQLRepresentationSchema, mk_sql_rep_schema
from mitm_tooling.transformation.superset.definitions import SupersetDashboardDef, DatasetIdentifierMap, \
    DashboardIdentifier
from mitm_tooling.transformation.superset.definitions.mitm_dataset import MitMDatasetIdentifier
from mitm_tooling.transformation.superset.factories.custom_charts import mk_maed_custom_chart
from mitm_tooling.transformation.superset.factories.dashboard import mk_dashboard_chart, mk_dashboard_def
from mitm_tooling.transformation.superset.visualizations.abstract import DashboardCreator, \
    ChartCollectionCreator, ChartDefCollection, MitMDashboardCreator
from mitm_tooling.transformation.superset.visualizations.maed.charts import BaselineMAEDCharts
from mitm_tooling.utilities.identifiers import mk_uuid
from mitm_tooling.utilities.python_utils import take_first


class BaselineMAEDDashboard(MitMDashboardCreator):

    @property
    def chart_collection_creator(self) -> ChartCollectionCreator:
        return BaselineMAEDCharts(self.header, self.sql_rep_schema)

    def mk_dashboard(self,
                     chart_collection: ChartDefCollection,
                     dashboard_identifier: DashboardIdentifier| None = None) -> SupersetDashboardDef:
        dashboard_identifier = dashboard_identifier or DashboardIdentifier()

        x = take_first(self.header.as_dict['measurement'])

        chart_grid = [
            [mk_dashboard_chart(chart_uuid=chart_collection['observation-objects-pie'].uuid, width=4, height=50),
             mk_dashboard_chart(chart_uuid=chart_collection['event-count-ts'].uuid, width=4, height=50),
             mk_dashboard_chart(chart_uuid=chart_collection['measurement-count-ts'].uuid, width=4, height=50)],
            [mk_dashboard_chart(chart_uuid=chart_collection[f'measurement-{x}-ts'].uuid, width=12, height=100)]]
        return mk_dashboard_def(dashboard_identifier.dashboard_title or 'MAED Dashboard',
                                chart_grid=chart_grid,
                                description='A rudimentary dashboard to view MAED data.',
                                uuid=dashboard_identifier.uuid)


class ExperimentalMAEDDashboard(MitMDashboardCreator):

    def __init__(self,
                 header: Header,
                 mitm_dataset_identifier: MitMDatasetIdentifier | None = None,
                 sql_rep_schema: SQLRepresentationSchema | None = None):
        super().__init__(header, sql_rep_schema)
        self.mitm_dataset_identifier = mitm_dataset_identifier or MitMDatasetIdentifier()

    @property
    def chart_collection_creator(self) -> ChartCollectionCreator:
        mitm_dataset_identifier = self.mitm_dataset_identifier

        class CustomChartCollectionCreator(ChartCollectionCreator):

            def mk_chart_collection(self, ds_id_map: DatasetIdentifierMap) -> ChartDefCollection:
                return {
                    'custom': mk_maed_custom_chart('Custom MAED Chart',
                                                   mitm_dataset_identifier,
                                                   ds_id_map['observations'])}

        return CustomChartCollectionCreator()

    def mk_dashboard(self,
                     chart_collection: ChartDefCollection,
                     dashboard_identifier: DashboardIdentifier| None = None) -> SupersetDashboardDef:
        dashboard_identifier = dashboard_identifier or DashboardIdentifier()

        chart_grid = [[mk_dashboard_chart(chart_uuid=chart_collection['custom'].uuid, width=12, height=400)]]
        return mk_dashboard_def(dashboard_identifier.dashboard_title or 'Experimental MAED Dashboard',
                                chart_grid,
                                description='An experimental dashboard to view MAED data.',
                                uuid=dashboard_identifier.uuid)
