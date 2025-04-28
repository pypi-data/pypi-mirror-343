from pyreglin.simdata.rlm import rlm
from pyreglin.tab_anova.tab_anova import tab_anova
from pyreglin.dataset.load_data import load_data, get_dataset_names
from pyreglin.statistics.press import press
from pyreglin.statistics.residuals_test import test_residuals
from pyreglin.statistics.r2 import R2, R2adj
from pyreglin.graphics.gginfluence import gginfluence
from pyreglin.graphics.ggresiduals import ggresiduals

__version__ = "0.1.5"
__all__ = ['rlm', 
           'tab_anova', 
           'load_data', 'get_dataset_names',
           'press', 'test_residuals', 'R2', 'R2adj',
           'gginfluence','ggresiduals']