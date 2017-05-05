import csv
from syn import Synonyms

with open('videoStats.csv', 'rb') as c:
    reader = csv.reader(c)
    next(reader, None)

    with open('condensedStats.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Id', 'Title', 'Description', 'LikeCount', 'DislikeCount', 'Location (latitude, longitude)', 'Condensed Tags (; delimited string)'])

        s = Synonyms.load(open('syns.txt'))

        for row in reader:
            row[1] = row[1].strip()
            row[2] = row[2].strip()

            if row[6] != '':
                l = row[6].split(';')

                for i in range(len(l)):
                    l[i] = l[i].strip()
                    merge = s.match(l[i], ignoreCase=True)

                    if merge:
                        l[i] = merge

                row[6] = ';'.join(list(set(l)))

            writer.writerow(row)