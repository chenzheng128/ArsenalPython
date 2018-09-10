import matplotlib.pyplot as plt
import tushare as ts
df = ts.get_h_data('600848', start='2018-01-01', end='2018-06-30')
plt.show()
