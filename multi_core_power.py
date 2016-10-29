# coding:utf-8
# python multi-core test
# winxos 2016-04-14
import multiprocessing
import time
import math


def func(a, b):
    return a**b


def async_power(a, b):
    pool = multiprocessing.Pool(processes=4)
    result = []
    a1 = b // 4
    a2 = b - a1 * 3
    result.append(pool.apply_async(func, (a, a1)))
    result.append(pool.apply_async(func, (a, a1)))
    result.append(pool.apply_async(func, (a, a1)))
    result.append(pool.apply_async(func, (a, a2)))
    pool.close()
    pool.join()
    sum = 1
    for res in result:
        sum *= res.get()
    print math.log(sum)/math.log(10)
if __name__ == "__main__":
    async_power(2, 500000000)
    #print math.log(2**500000000)
