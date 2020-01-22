import sqlite3
with sqlite3.connect('Edyoda.db') as db:
    c = db.cursor()
class Main():
	def main(self):
		with sqlite3.connect('Edyoda.db') as db:
			c = db.cursor()
			c.execute('Select yid,avg(Rating) from YoungReview group by yid;')
			results=c.fetchall()
			if len(results)>0:
				for i in range(0,len(results)):
					c.execute('Update Young set Rating=? where id=?',(results[i][1],results[i][0]))
					db.commit()
			c.execute('Select eid,avg(Rating) from ElderReview group by eid')
			results=c.fetchall()
			if len(results)>0:
				for i in range(0,len(results)):
					c.execute('Update Elders set Rating=? where id=?',(results[i][1],results[i][0]))
					db.commit()
		choice=int(input("Press 1 if you are an Senior Citizen looking out for care\nPress 2 if you are a Young Chap looking out taking care of Senior Citizen\nPress 3 for admin Access\nPress 4 to exit.\n"))
		if choice==1:
			from Elder import initiate
		elif choice==2:
			from Young import initiate
		elif choice==3:
			from admin import initiate
		else:
			print("Thanks for visting\nPlease visit again")

m=Main()
m.main()