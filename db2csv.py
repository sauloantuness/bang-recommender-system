import sqlite3
from datetime import datetime


conn = sqlite3.connect('dataset.db')
c = conn.cursor()

print 'user,problem,category,date'

c.execute('''
	SELECT s.user_id, s.problem_id, p.category_id, s.date
	FROM solution s LEFT JOIN problem p 
	ON s.problem_id = p.problem_id
''')

for user, problem, category, date in c.fetchall():
	d = datetime.strptime(date,'%m/%d/%y, %I:%M:%S %p')
	print str(user) + ',' + str(problem) + ',' + str(category) + ',' + d.strftime('%y/%m/%d %I:%M')

conn.close()