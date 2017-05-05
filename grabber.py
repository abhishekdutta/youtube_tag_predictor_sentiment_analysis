import datetime
import json
import urllib2
from os import path

def grab(queryURL):
    existing = {'items':[]}

    if path.isfile('raw.json'):
        with open('raw.json', 'rb') as j:
            existing = json.load(j)

        with open('failSafe.json', 'wb') as f:
                json.dump(existing, f)

    with open('raw.json', 'wb') as j:
        results = json.load(urllib2.urlopen(queryURL))

        results['items'].extend(existing['items'])
        tok = results['nextPageToken']

        while True:
            try:
                temp = json.load(urllib2.urlopen(queryURL + '&pageToken=' + tok))
                results['items'].extend(temp['items'])

                if 'nextPageToken' not in temp:
                    break

                tok = temp['nextPageToken']
                print(tok)
            except:
                print('API key ran out')

                with open('failSafe.json', 'wb') as f:
                    json.dump(results, f)

                break

        json.dump(results, j)

def main():
    api_key = 'AIzaSyCXqjs2ZPb0PQReIWiENMAAkSx0_tvd4nk'
    # AIzaSyCrFWiPfGcb5IsyS-wpAMk6eaNdMaC8pXs
    # AIzaSyDlZR2UhwQXeGw2IhCRnpoZB8LHZkagwI4
    # AIzaSyCXqjs2ZPb0PQReIWiENMAAkSx0_tvd4nk
    # AIzaSyCsE91PTD-XjTU3O_IZpY0PvVom2tw4Dr8
    # AIzaSyArrhkh49b2GNlC8UdLodq3uSpKzcgdzeg
    # AIzaSyCPcAKC74SzgQB8MSXKcPO6zIoVfqwlOig
    # AIzaSyDBkoHdD1Iw6HooMhMoObbHFCXHFSwKzIU
    # AIzaSyC4C3gzSSErzmc2FeUTleQqZGzw8-z-d6w

    publishedBefore = ''
    publishedAfter = ''

    d1 = '2017-04-18T'
    d2 = '2017-04-19T'
    t = datetime.datetime(2017, 3, 1, 0, 0, 0)
    
    for i in range(144):
        publishedAfter = d1 + str(t.time()) + 'Z'
        t += datetime.timedelta(minutes=10)

        if i == 143:
            publishedBefore = d2 + str(t.time()) + 'Z'
        else:
            publishedBefore = d1 + str(t.time()) + 'Z'

        queryURL =  'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&order=date&publishedAfter=' \
                    + publishedAfter + '&publishedBefore=' + publishedBefore + '&type=video&key=' + api_key

        grab(queryURL)
        print(publishedBefore)

if __name__ == '__main__':
    main()