import matplotlib
import numpy as np
import heapq
import pandas as pd
matplotlib.use("agg")
#import random
import math


filepath = "Datasets/RandomCheckerData/"
#output_filename = "Checker_Data_40_32_32.txt"
output_filename = "Checker_s_1_100_16by16.txt"
# grid=[2,4,8,16,32,64,128,256,512,1024]
grid = [16]
zero_zero_val = 1.0
zero_one_val = 100.0
percentage = 1.0



data = []

for g in grid:
    data = []
    total_possible_pick = math.floor(g * g / 2)
    random_index_length = math.floor(percentage * g * g / 2)
    print("Pick Count : " + str(random_index_length))

    random_index = np.sort(np.random.choice(np.arange(0, total_possible_pick), random_index_length, replace=False))

    temp_count = 0
    for i in range(g):
        for j in range(g):
            if (i+j)%2 == 0:
                data.append(zero_zero_val)
            else:
                if temp_count in random_index:
                    data.append(zero_one_val)
                else:
                    data.append(zero_zero_val)
                temp_count += 1

    print("Checker Data is generating for " + str(g) + " by " + str(g) + " with percentage " + str(percentage))

    output_txt_file = filepath + output_filename

    count = 1
    with open(output_txt_file, 'w') as f:
        for i in data:
            if count != g * g:
                f.write('{:.10f},'.format(i))
                if count % g == 0:
                    f.write('\n')
            else:
                f.write('{:.10f}'.format(i))
            count += 1
