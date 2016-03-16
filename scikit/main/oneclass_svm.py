#coding:utf-8

#Source： http://www.dataivy.cn/blog/%E6%96%B0%E5%A5%87%E6%A3%80%E6%B5%8Bnovelty-detection/

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn import svm
xx, yy = np.meshgrid(np.linspace(-5, 5, 500), np.linspace(-5, 5, 500))
# 生成训练数据
X = 0.3 * np.random.randn(100, 2)
X_train = np.r_[X+2, X-2]
# 生成新用于测试的数据
X = 0.3 * np.random.randn(10, 2)
X_test = np.r_[X + 2, X - 2]
# 模型拟合
clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)

#更多参数
#class sklearn.svm.OneClassSVM
#(kernel='rbf', degree=3, gamma=0.0, coef0=0.0, tol=0.001, nu=0.5, shrinking=True, cache_size=200, verbose=False, max_iter=-1, random_state=None)

clf.fit(X_train)
y_pred_train = clf.predict(X_train)
y_pred_test = clf.predict(X_test)
print ("novelty detection result:",y_pred_test)
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
# 在平面中绘制点、线和距离平面最近的向量
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.title("Novelty Detection")
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.Blues_r)
a = plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors="red")
plt.contourf(xx, yy, Z, levels=[0, Z.max()], colors="orange")
b1 = plt.scatter(X_train[:, 0], X_train[:, 1], c="white")
b2 = plt.scatter(X_test[:, 0], X_test[:, 1], c="green")
plt.axis("tight")
plt.xlim((-5, 5))
plt.ylim((-5, 5))
plt.legend([a.collections[0], b1, b2],
["learned frontier", "training observations",
"new observations", ],
loc="upper left",
prop=matplotlib.font_manager.FontProperties(size=11))
plt.xlabel(
"error train: %d/200 ; errors novel regular: %d/40 ; "
% (n_error_train, n_error_test,))
plt.show()
