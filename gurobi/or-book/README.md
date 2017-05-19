# or-book
参考图书《运筹学 第三版》（清华大学出版社），《运筹学同步辅导及课后习题答案》， 使用 gurobi 完成对应代码。

## Env 运行环境
```
pyenv version
# anaconda2-4.3.1
conda list gurobi
# gurobi                    7.0.2                    py27_0

Jupyter motebooks # 启动 notebook 环境
```

补充资料 evernote: gurobi or-book
## 第1章 线性规划与单纯形法
* `homework-1.1-1` 第6页 课后习题 用图解法解线性规划
* `homework-1.11` 第27页 1.11 某厂生产3种产品

## 第2章 运输问题
* `book-chap03-facility-p79.ipynb` 第79页 例题1
* `book-chap03-facility-p90-example2.ipynb` 第90页 例2 设有三个化肥厂( A, B, C)供应四个地区(I,II,III,IV)的农用化肥。假定等 量的化肥在这些地区使用效果相同。各化肥厂年 产量 , 各 地区 年需要 量及 从各化 肥厂 到 各地区运送单位化肥的运价如表 3 -25 所示。试求出总的运费最节省的化肥调拨方案。

## 第5章 整数规划
* `book-chap05-assign-p126-example7.ipynb` 第126页 第5节 指派问题 例7 p. 126 例7 有一份中文说明书,需译成英、日、德、俄四种文字。分别记作E、J、G、R。现 有甲、乙、丙、丁四人。他们将中文说明书翻译成不同语种的说明书所需时间如表 5-7 所 示。问应指派何人去完成何工作 , 使所需总时间最少 ?
