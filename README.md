# README
This is a script for analyzing the csv file from OpenVINO performance and accuracy test.
<br>

``Functions:``  <br>
``1:`` Calc GEOMEAM. <br>
``2:`` Statistic performance data with big difference. <br>
``3:`` Statistic accuracy with different result. <br>
``4:`` Result will be also saved to "analysis_result.csv" <br>

#### GEOMEAM formula

For example, we test 2 times, there are 2 group data. X={Xi, Xj, Xz, ...}, Y={Yi, Yj, Yz, ...}, and they have same dim.

GEOMEAM = pow(((Xi/Yi)*(Xj/Yj)*(Xz/Yz)*..., 1/n)

Refer: https://en.wikipedia.org/wiki/Geometric_mean
