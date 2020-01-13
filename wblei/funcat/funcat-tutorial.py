from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np

np.seterr(all='ignore')
rcParams['figure.figsize'] = (14, 6)

from funcat import *
from funcat.data.tushare_backend import TushareDataBackend
from funcat.data.rqalpha_data_backend import RQAlphaDataBackend

backend = 'rqalpha'

if backend == 'rqalpha':
    set_data_backend(RQAlphaDataBackend("~/.rqalpha/bundle"))
elif backend == 'tushare':
    set_data_backend(TushareDataBackend())

set_start_date('2015-01-01')
S("000001.XSHG")
T("2019-09-02")

print(O)