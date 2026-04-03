# Read in a file from a URL and save a local CSV file with the first 10 rows

import pandas as pd
import numpy as np
import pyarrow

filename = 'https://drive.google.com/uc?id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA&export=download'

df  = pd.read_csv(filename, engine='pyarrow')

out_filename = "sales_data_test.csv"
df.head(10).to_csv(out_filename, index=False)
