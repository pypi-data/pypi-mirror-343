"""
Author: Big Panda
Created Time: 25.04.2025 14:09
Modified Time: 25.04.2025 14:09
Description:
    
"""
import DataRestriction as dr

b = dr.NonNegativeIntProperty(default=1, doc="")
c = dr.NonNegativeIntProperty(default=b.value, doc="")
print(b)
print(c)


# 这里的示例也可以写成一个教程！！！！
# x, y = [1, 3]
# print(x)
# print(y)