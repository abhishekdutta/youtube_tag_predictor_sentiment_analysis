import pymysql
import csv

db = pymysql.connect(host='localhost',
					user='root',
					password='password',
					db='youtube_data',
					charset='utf8mb4',
					cursorclass=pymysql.cursors.DictCursor)

cursor = db.cursor()

create_video_info_table = """CREATE TABLE IF NOT EXISTS video_info (
							video_id VARCHAR(11) NOT NULL,
							title VARCHAR(255),
							popularity FLOAT,
							sentiment_percentage FLOAT,
							sentiment_category VARCHAR(8));"""

create_tag_video_table = """CREATE TABLE IF NOT EXISTS tag_to_video (
							tag VARCHAR(255) NOT NULL,
							video_id VARCHAR(11) NOT NULL);"""

create_tag_freq_table = """CREATE TABLE IF NOT EXISTS tag_frequency (
							tag VARCHAR(255) NOT NULL,
							frequency INT NOT NULL);"""

cursor.execute(create_video_info_table)
cursor.execute(create_tag_video_table)

insert_tag = """INSERT INTO tag_to_video (tag, video_id) VALUES (%s, %s);"""
insert_video = """INSERT INTO video_info (video_id, title, popularity, 
				sentiment_percentage, sentiment_category) VALUES (%s, %s, %s, %s, %s);"""

with open('../sentiment_analysis_of_predicted_tags.csv', 'r') as f:
	reader = csv.reader(f, delimiter=',')
	next(reader, None)
	for entry in reader:
		video_id = entry[0]
		title = entry[1]
		if float(entry[4]) == 0 and float(entry[3]) == 0:
			popularity = 0
		else:
			popularity = float(entry[3])/(float(entry[3]) + float(entry[4]))
		if entry[6] not in (None, ""):
			tags = [x.strip() for x in entry[6].split(',')]
			for tag in tags:
				tag_args = tag, video_id
				cursor.execute(insert_tag, tag_args)
		sentiment_percentage = entry[7]
		sentiment_category = entry[8]
		video_args = video_id, title, popularity, sentiment_percentage, sentiment_category
		cursor.execute(insert_video, video_args)	
			
db.commit()
db.close()