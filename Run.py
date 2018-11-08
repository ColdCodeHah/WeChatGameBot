import sqlite3

nums={}
numstr='1112333'
money='10'
for n in numstr:
    if n not in nums:
        nums[n]=int(money)
    else:
        nums[n]+=int(money)
