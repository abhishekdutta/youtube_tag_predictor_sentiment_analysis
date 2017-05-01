import json
import csv
import urllib2
import re
import string

api_key = 'AIzaSyCrFWiPfGcb5IsyS-wpAMk6eaNdMaC8pXs'
url =  'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,recordingDetails&id='

#strip punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

#id, title, description, like count, dislike count, location, tags
with open('raw.json', 'rb') as f:    
    data = json.load(f)
    l = []

    for item in data['items']:
    	l.append([item['id']['videoId'], item['snippet']['title'], item['snippet']['description']])
    
    with open('videoStats.csv', 'wb') as c:
        writer = csv.writer(c)
        writer.writerow(['Id', 'Title', 'Description', 'LikeCount', 'DislikeCount', 'Location (latitude, longitude)', 'Tags (; delimited string)'])

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
                loc = str(s['recordingDetails']['location']['latitude']) + ';' + str(s['recordingDetails']['location']['longitude'])
            if 'tags' in s['snippet']:
                t = s['snippet']['tags']

                for i in range(len(t)):
                    t[i] = re.sub(r'http\S+|www.\S+', '', t[i])
                    t[i] = regex.sub('', t[i])

                tags = ';'.join(t)

            title = re.sub(r'http\S+|www.\S+', '', vid[1])
            descr = re.sub(r'http\S+|www.\S+', '', vid[2])

            title = regex.sub('', title)
            descr = regex.sub('', descr)

            writer.writerow([vid[0], title.encode('utf8').decode('unicode_escape').encode('ascii','ignore'), descr.encode('utf8').decode('unicode_escape').encode('ascii','ignore'), LC, DC, loc, tags.encode('utf8').decode('unicode_escape').encode('ascii','ignore')])