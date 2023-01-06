# Script Name     : radixsort.py
# Author          : tzzzzzzzx
# Created         : 6th Jan 2023
# Last Modified	  : 6th Jan 2023
# Version         : 1.0
# Modifications	  : 
# Description     : Sorting algorithms related to radixsort.

import copy
from .data import Data
import math

def pigeonhole_sort(data_set):
    frames = [data_set]
    ds = copy.deepcopy(data_set)
    maxval = max([j.value for j in ds])
    element_cnt = [0 for _ in range(maxval+1)]
    for i in range(Data.data_count):
        frames.append(copy.deepcopy(ds))
        frames[-1][i].set_color('r')
        element_cnt[ds[i].value] += 1
    cur_element = maxval
    for i in range(Data.data_count-1,-1,-1):
        while element_cnt[cur_element]<=0:
            cur_element -= 1
        ds[i].value = cur_element
        ds[i].set_color()
        element_cnt[cur_element] -= 1
        frames.append(copy.deepcopy(ds))
        frames[-1][i].set_color('r')
    frames.append(ds)
    return frames

def radix_sort(data_set):
    frames = [data_set]
    ds = copy.deepcopy(data_set)
    def getnthdigit(nth: int, value: int) -> int :
        return value//(10**nth)%10

    maxval = max([j.value for j in ds])
    maxradix = int(math.floor(math.log(maxval, 10)))
    bucket = []
    for i in range(10):
        bucket.append([])
    for radix in range(maxradix+1):
        bucket = []
        for i in range(10):
            bucket.append([])
        for i in range(Data.data_count):
            frames.append(copy.deepcopy(ds))
            frames[-1][i].set_color('r')
            bucket[getnthdigit(radix, ds[i].value)].append(copy.deepcopy(ds[i])) # avoid sharing the same addr
        ds[-1].value = maxval
        ds[-1].set_color() # Avoid height change
        cur_ptr = 0
        for i in range(10):
            for j in bucket[i]:
                frames.append(copy.deepcopy(ds))
                frames[-1][cur_ptr].set_color('r') # made other place red in prev version: data equal in value share the same address.
                ds[cur_ptr] = j
                cur_ptr += 1
    frames.append(copy.deepcopy(ds))
    return frames

