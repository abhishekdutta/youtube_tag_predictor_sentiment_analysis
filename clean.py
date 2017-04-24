import json
import csv
import urllib2
import re
import string

api_key = 'AIzaSyCrFWiPfGcb5IsyS-wpAMk6eaNdMaC8pXs'
url =  'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,recordingDetails&id='

regex = re.compile('[%s]' % re.escape(string.punctuation))

#id, title, description, like count, dislike count, location, tags
with open('raw.json', 'rb') as f:    
    data = json.load(f)
    l = []

    for item in data['items']:
    	l.append([item['id']['videoId'], item['snippet']['title'], item['snippet']['description']])
    
    with open('videoStats.csv', 'wb') as c:
        writer = csv.writer(c)
        writer.writerow(['Id', 'Title', 'Description', 'LikeCount', 'DislikeCount', 'Location (latitude, longitude)', 'Tags (comma delimited string)'])

        for vid in l:
            stats = json.load(urllib2.urlopen(url + vid[0] + '&key=' + api_key))

            if stats['items'] == []:
                writer.writerow([vid[0], vid[1].encode('utf8'), vid[2].encode('utf8'),0,0,'',''])
                continue

            s = stats['items'][0]
            LC = 0
            DC = 0
            loc = ''
            tags = ''

            if 'likeCount' in s['statistics']:
                LC = s['statistics']['likeCount']
            if 'dislikeCount' in s['statistics']:
                DC = s['statistics']['dislikeCount']
            if 'latitude' in s.get('recordingDetails', {}).get('location', {}):
                loc = str(s['recordingDetails']['location']['latitude']) + ',' + str(s['recordingDetails']['location']['longitude'])
            if 'tags' in s['snippet']:
                tags = ','.join(s['snippet']['tags'])

            title = regex.sub('', vid[1])
            descr = regex.sub('', vid[2])

            writer.writerow([vid[0], title.encode('utf8'), descr.encode('utf8'), LC, DC, loc, tags.encode('utf-8')])