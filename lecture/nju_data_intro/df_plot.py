import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.randn(4,4),index = list('ABCD'),columns=list('OPKL'))
df.plot()
plt.show()