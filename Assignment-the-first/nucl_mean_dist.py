#!/usr/bin/env python

in_file = "/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz"
out_png = "1294_S1_L008_R4_001.png"

import bioinfo
import gzip

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.'''
    x = 0
    lst = []
    while x in range(101):
        lst.append(value)
        x+=1
    return lst

my_list: list = []
my_list = init_list(my_list)

num_records = 0

with gzip.open(in_file, "r") as file:
    # Variables here:
    line_counter = 0  
    for line in file:
        line_counter+=1
        line = line.decode("utf-8").strip('\n')
        if line_counter % 4 == 0:
            num_records+=1
            for counter,score in enumerate(line):
                my_list[counter] += bioinfo.convert_phred(score)

for i in range(101):
    my_list[i] = my_list[i]/num_records

import matplotlib.pyplot as plt

x=range(101)
y=my_list

plt.bar(x, y)
plt.title("Distribution of quality scores per base position")
plt.xlabel("Base Position")
plt.ylabel("Mean Quality Score")
plt.savefig(out_png)