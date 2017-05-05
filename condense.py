import csv
from syn import Synonyms
import re

with open('videoStats.csv', 'rb') as c:
    reader = csv.reader(c)
    next(reader, None)

    with open('condensedStats.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Title', 'Description', 'LikeCount', 'DislikeCount', 'Location (latitude, longitude)', 'Condensed Tags (; delimited string)'])

        s = Synonyms.load(open('syns.txt'))

        for row in reader:
            row[1] = row[1].replace('\n', '')
            row[2] = row[2].replace('\n', '')

            if row[6] != '':
                l = row[6].split(';')

                for i in range(len(l)):
                    l[i] = l[i].replace('\r\n', '')
                    l[i] = l[i].replace('\n', '')
                    merge = s.match(l[i], ignoreCase=True)

                    if merge:
                        l[i] = merge

                row[6] = ';'.join(list(set(l)))
                print(row[6])
                row[6] = re.sub(r'\s*;\s*', ';', row[6])
                print(row[6])

            writer.writerow(row)