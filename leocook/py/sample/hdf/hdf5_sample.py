import h5py
import pandas as pd
import numpy as np

lines = 1000
cloumns = 2

cube = np.random.rand(lines, cloumns)

# print(cube)
# print(cube)

#######

e = {
    'A' : pd.Series([1,2,3]),
    'B' : pd.Series([1,2,3,4])
}

df1 = pd.DataFrame(e)


print('df1:')
print(df1)

df1.to_hdf('./hdf/hdf_01_e.h5', key='sample_01', mode='a')
print(pd.read_hdf('./hdf/hdf_01_e.h5', 'sample_01'))