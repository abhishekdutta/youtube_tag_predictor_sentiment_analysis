import csv
import datetime

days = [(datetime.date(2017, 3, 1) + datetime.timedelta(days=(1*i))).strftime("%Y-%m-%d") for i in range(31 + 30 + 9)]

with open('commentsFile.csv', 'rb') as c:
    reader = csv.reader(c)
    next(reader, None)

    with open('separatedCommentsFile.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['Id'] + days)

        for row in reader:
            commentsList = row[3].split(';')
            l = ['' for i in range(len(days))]

            for comment in commentsList:
                c = comment.split('|')
                print(c)
                
                if c[0] == '':
                    continue

                cTime = datetime.datetime.strptime(c[1], "%Y-%m-%dT%H:%M:%S.000Z")
                index = days.index(cTime.date().strftime("%Y-%m-%d"))

                if l[index] == '':
                    l[index] = c[0]
                else:
                    l[index] = l[index] + ';' + c[0]

            writer.writerow([row[0]] + l)