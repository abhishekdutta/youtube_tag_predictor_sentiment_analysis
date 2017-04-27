#!/usr/bin/env python

import json
from os.path import dirname, realpath

from mapreduce import mapreduce
import collections
import csv


# record: (Id,Title,Description,LikeCount,DislikeCount,location, tags)
def mapper1(record):
    ratio = 0

    if record[4] != '0':
        ratio = int(record[3])/int(record[4])
    
    return (ratio, [record[0], record[1], record[2]])

def reducer(a, b):
    return a + b

def main():

    with open('videoStats.csv', 'rb') as f:
        data = [line.split(',') for line in f]

        sc = mapreduce()
        result = sc.parallelize(data[1:], 128) \
                            .map(mapper1) \
                            .reduceByKey(reducer) \
                            .sortByKey(True) \
                            .collect()

        sc.stop()

        topVids = result[len(result)-51:]
        l = []

        for vid in topVids:
            l.extend(vid[1][0].lower().split(' '))
            l.extend(vid[1][1].lower().split(' '))

        counter = collections.Counter(l)

        with open('data.csv', 'wb') as c:
            writer = csv.writer(c)
            writer.writerow(['Word', 'Count'])

            for key,count in counter.most_common():
                writer.writerow([key, count])

if __name__ == '__main__':
    main()