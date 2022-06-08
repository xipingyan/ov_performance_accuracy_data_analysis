# README
This is a script for analyzing the csv file from OpenVINO performance and accuracy test.

``Functions:``
``1:`` Calc GOMean.
``2:`` Statistic performance data with big difference.
``3:`` Statistic accuracy with different result.
``4:`` Result will be also saved to "analysis_result.csv"

#### GOMean formula

For example, we test 2 times, there are 2 group data. X={Xi, Xj, Xz, ...}, Y={Yi, Yj, Yz, ...}, and they have same dim.

GOMean = pow(((Xi/Yi)*(Xj/Yj)*(Xz/Yz)*..., 1/n)

