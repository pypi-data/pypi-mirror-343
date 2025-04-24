from enum import StrEnum
from typing import Type

from mitm_tooling.transformation.superset.visualizations.abstract import VisualizationsCreator
from mitm_tooling.transformation.superset.visualizations.maed.dashboards import BaselineMAEDDashboard, \
    ExperimentalMAEDDashboard


class MAEDVisualizationType(StrEnum):
    Baseline = 'baseline'
    Experimental = 'experimental'


maed_visualization_creators: dict[MAEDVisualizationType, Type[VisualizationsCreator]] = {
    MAEDVisualizationType.Baseline: VisualizationsCreator.wrap_single('baseline',
                                                                      lambda h, mdi: BaselineMAEDDashboard(h)),
    MAEDVisualizationType.Experimental: VisualizationsCreator.wrap_single('experimental',
                                                                          lambda h, mdi: ExperimentalMAEDDashboard(h,
                                                                                                                   mdi)),
}
