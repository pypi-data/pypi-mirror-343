from mitm_tooling.data_types import MITMDataType
from mitm_tooling.representation import ColumnName
from mitm_tooling.utilities.python_utils import unique
from .chart import mk_chart_def
from .core import mk_adhoc_metric, mk_empty_adhoc_time_filter, \
    mk_pivot_post_processing, mk_adhoc_column
from .query import mk_query_object, \
    mk_empty_query_object_time_filter_clause, mk_query_context
from ..definitions import DatasetIdentifier, SupersetChartDef, SupersetAggregate, \
    PieChartParams, SupersetVizType, SupersetAdhocFilter, TimeGrain, TimeSeriesBarParams, QueryObjectFilterClause, \
    TimeSeriesLineParams, QueryObjectExtras


def mk_pie_chart(name: str, dataset_identifier: DatasetIdentifier, col: ColumnName, dt: MITMDataType,
                 groupby_cols: list[ColumnName] | None = None) -> SupersetChartDef:
    groupby_cols = groupby_cols or []
    metric = mk_adhoc_metric(col, agg=SupersetAggregate.COUNT, dt=dt)
    params = PieChartParams(datasource=dataset_identifier,
                            metric=metric,
                            groupby=groupby_cols,
                            adhoc_filters=[mk_empty_adhoc_time_filter()])
    # TODO may not be necessary to add groupby
    qo = mk_query_object(unique([col], groupby_cols), metrics=[metric],
                         filters=[mk_empty_query_object_time_filter_clause()])
    qc = mk_query_context(datasource=dataset_identifier, queries=[qo], form_data=params)

    return mk_chart_def(name=name,
                        viz_type=SupersetVizType.PIE,
                        dataset_uuid=dataset_identifier.uuid,
                        params=params,
                        query_context=qc)


def mk_time_series_bar_chart(name: str,
                             dataset_identifier: DatasetIdentifier,
                             y_col: ColumnName,
                             y_dt: MITMDataType,
                             x_col: ColumnName,
                             groupby_cols: list[ColumnName] | None = None,
                             filters: list[SupersetAdhocFilter] | None = None,
                             time_grain: TimeGrain | None = None) -> SupersetChartDef:
    groupby_cols = groupby_cols or []
    metric = mk_adhoc_metric(y_col, agg=SupersetAggregate.COUNT, dt=y_dt)
    adhoc_filters = [mk_empty_adhoc_time_filter()]
    if filters:
        adhoc_filters.extend(filters)
    params = TimeSeriesBarParams(datasource=dataset_identifier,
                                 metrics=[metric],
                                 groupby=groupby_cols,
                                 adhoc_filters=adhoc_filters,
                                 x_axis=x_col,
                                 time_grain_sqla=time_grain
                                 )

    pp = mk_pivot_post_processing(x_col, cols=[y_col], aggregations={metric.label: 'mean'},
                                  renames={metric.label: None})
    adhoc_x = mk_adhoc_column(x_col, timeGrain=time_grain)
    qo = mk_query_object(columns=unique([adhoc_x, y_col], groupby_cols),
                         metrics=[metric],
                         filters=[QueryObjectFilterClause.from_adhoc_filter(af) for af in adhoc_filters],
                         post_processing=pp,
                         series_columns=[y_col])
    qc = mk_query_context(datasource=dataset_identifier, queries=[qo], form_data=params)

    return mk_chart_def(name=name,
                        viz_type=SupersetVizType.TIMESERIES_BAR,
                        dataset_uuid=dataset_identifier.uuid,
                        params=params,
                        query_context=qc)


def mk_avg_count_time_series_chart(name: str,
                                   dataset_identifier: DatasetIdentifier,
                                   groupby_cols: list[ColumnName],
                                   time_col: ColumnName = 'time',
                                   filters: list[SupersetAdhocFilter] | None = None,
                                   time_grain: TimeGrain | None = None):
    groupby_cols = groupby_cols or []
    metric = mk_adhoc_metric(time_col, agg=SupersetAggregate.COUNT, dt=MITMDataType.Datetime)
    adhoc_filters = [mk_empty_adhoc_time_filter()]
    if filters:
        adhoc_filters.extend(filters)
    params = TimeSeriesLineParams(datasource=dataset_identifier,
                                  metrics=[metric],
                                  groupby=groupby_cols,
                                  adhoc_filters=adhoc_filters,
                                  x_axis=time_col,
                                  time_grain_sqla=time_grain
                                  )

    pp = mk_pivot_post_processing(time_col, cols=groupby_cols, aggregations={metric.label: 'mean'},
                                  renames={metric.label: None})
    adhoc_time_col = mk_adhoc_column(time_col, timeGrain=time_grain)
    qo = mk_query_object(columns=unique([adhoc_time_col], groupby_cols),
                         metrics=[metric],
                         filters=[QueryObjectFilterClause.from_adhoc_filter(af) for af in adhoc_filters],
                         post_processing=pp,
                         series_columns=groupby_cols,
                         extras=QueryObjectExtras(time_grain_sqla=time_grain))
    qc = mk_query_context(datasource=dataset_identifier, queries=[qo], form_data=params)

    return mk_chart_def(name=name,
                        viz_type=SupersetVizType.TIMESERIES_LINE,
                        dataset_uuid=dataset_identifier.uuid,
                        params=params,
                        query_context=qc)
