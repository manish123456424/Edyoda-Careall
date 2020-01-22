import sqlite3
with sqlite3.connect('Edyoda.db') as db:
    c = db.cursor()

class admin:
	def login(self,username,password):
		if username=='root' and password=='1234':
			print("Welcome Admin \n")
			self.status_check()
		else:
			print("Not Authorized\nWrong Username or Password")
	def status_check(self):
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
		option=0
		while option!=1:
			print("Press 1 to see who is taking care of Elder people ")
			print("Press 2 to see details of Elder people under Young people ")
			print("Press 3 to exit ")
			choice=int(input())
			if choice==1:
				c.execute('Select id,Name,ElderCount from Young where ElderCount>0')
				results=c.fetchall()
				if len(results)==0:
					print("No Young people are currently taking care of Elders\n")
				else:
					for i in range(0,len(results)):
						print("Young id: "+str(results[i][0])+" Name: "+results[i][1]+" ElderCount: "+str(results[i][2])+"\n")
			elif choice==2:
				query='select c.eid,c.yid,e.name,y.name from carerequest c left join young y on c.yid=y.id left join elders e on c.eid=e.id where c.status=? order by c.yid;'
				c.execute(query,('Accepted',))
				results=c.fetchall()
				if len(results)==0:
					print("No Young people are currently taking care of Elders\n")
				else:
					for i in range(0,len(results)):
						print("Young id: "+str(results[i][1])+" Name: "+results[i][3]+" ElderId: "+str(results[i][0])+" ElderName: "+results[i][2]+"\n")
			else:
				print("Thanks for visiting ")
				option=0
				break
def initiate():
	username=input('Enter Admin Username ')
	password=input('Enter Admin Password ')
	a=admin()
	a.login(username,password)
initiate()
