#!/usr/bin/env python

import json
from os.path import dirname, realpath

from mapreduce import mapreduce
import collections
import csv
import urllib2
import re
import string

api_key = 'AIzaSyCrFWiPfGcb5IsyS-wpAMk6eaNdMaC8pXs'
url =  'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId='

# record: (Id, Title, Description, LikeCount, DislikeCount, location, tags)
def mapper1(record):
    ratio = 0

    if record[4] != '0':
        ratio = int(record[3])/int(record[4])
    
    return (ratio, [record[0], record[1], record[2], record[6]])

def reducer(a, b):
    return a + b

def main():

    with open('condensedStats.csv', 'rb') as f:
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
            l.extend(vid[1][3].lower().split(';'))

        counter = collections.Counter(l)

        with open('mostCommonTags.csv', 'wb') as c:
            writer = csv.writer(c)
            writer.writerow(['Tag', 'Count'])

            for key,count in counter.most_common():
                writer.writerow([key, count])

        with open('commentsFile.csv', 'wb') as c:
            writer = csv.writer(c)
            writer.writerow(['Id', 'Title', 'Description', 'Comments (; delimited list)'])

            regex = re.compile('[%s]' % re.escape(string.punctuation))

            for vid in topVids:
                comments = json.load(urllib2.urlopen(url + vid[1][0] + '&key=' + api_key))

                commentList = ''

                if comments['items']:
                    thread = []

                    for item in comments['items']:
                        if 'textDisplay' in item['snippet'].get('topLevelComment', {}).get('snippet', {}):
                            thread.append(regex.sub('', item['snippet']['topLevelComment']['snippet']['textDisplay']))

                    commentList = ';'.join(thread)

                writer.writerow([vid[1][0], vid[1][1], vid[1][2], commentList.encode('utf8').decode('unicode_escape').encode('ascii','ignore')])

if __name__ == '__main__':
    main()