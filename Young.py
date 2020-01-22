import sqlite3
with sqlite3.connect('Edyoda.db') as db:
    c = db.cursor()
class Young:
	def __init__(self):
		self.Uname=str
		self.pwd=str
		self.eldercount=int
		self.Yid=int
	def new_user(self,Name,Age,Contact,Uname,pwd):
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
		c.execute('Select * from Young where Uname="'+Uname+'";')
		results=c.fetchall()
		if len(results)==0:
			insert = "INSERT INTO Young(Name,Age,Contact,Uname,pwd) VALUES(?,?,?,?,?)"
			c.execute(insert,(Name,Age,Contact,Uname,pwd))
			db.commit()
			self.Uname=Uname
			self.pwd=pwd
			print("Congrats Account Created Start Exploring")
			self.existing_user(Uname,pwd)
		else:
			Yid=input("Please enter your id")
			results=c.execute('Select * from Young where id="'+Yid+'";')
			if len(results)==0:
				print("UserName Already Exists")
			else:
				print("Profile Exists")
	def existing_user(self,Uname,pwd):
		self.Uname=Uname
		self.pwd=pwd
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
		c.execute('Select eldercount,id from Young where Uname= ? and pwd=? ;',(Uname,pwd))
		results=c.fetchall()
		if len(results)==0:
			print("Please Enter Correct Details")
			return 0
		else:
			self.eldercount=results[0][0]
			self.Yid=results[0][1]
			print("Welcome")
			try:
				option='y'
				while option!='n':
					self.user_options()
					choice=int(input())
					if choice==1:
						self.start_caring()
					elif choice==2:
						self.review_rating()
					elif choice==3:
						self.request_updates()
					elif choice==4:
						self.elder_details()
					else:
						self.Check_Ratings()
					option=input("Want to explore more options y/n ").lower().strip()
					#print(option[0])
					if option[0]=='n':
						print("Thank you for visiting")
						option='n'
					elif option[0]=='y':
						option='y'
					else:
						print("Please enter yes or no")
						option='y'
			except:
				print("Something Went Wrong Please Try Again")
			return 1
	def user_options(self):
		print("Press 1 to Start Caring ")
		print("Press 2 to Rate and Review your Elders ")
		print("Press 3 to see request updates")
		print("Press 4 to see Details of elders Currently registered under you")
		print("Press 5 to check your Review ")
	def start_caring(self):
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
		c.execute('Select id,Name,Funds from Elders where available=?;',('YES',))
		results=c.fetchall()
		if len(results)==0:
			print("No elderly is Currently available.")
		else:
			print("Below are the available elders\n")
			for i in range (0,len(results)):
				print("Elder Id= "+str(results[i][0])+", Elder Name= "+results[i][1]+ ", Allocated Funds= "+str(results[i][2])+"\n")
			eid=input("Please Enter the Elder Id ")
			c.execute('Select id,ElderCount from Young where Uname=?',(self.Uname,))
			results=c.fetchall()
			Yid=results[0][0]
			if results[0][1]==None:
				self.eldercount=0
			else:
				self.eldercount=results[0][1]
			if self.eldercount>=4:
				print("Maximum Care Count Reached")
			else:
				c.execute('Select Status from CareRequest where Eid=? and Yid=?',(eid,Yid))
				results=c.fetchall()
				if len(results)!=0:
					print('Request already in Queue\nStatus:- '+str(results[0][0]))
				else:
					insert='INSERT INTO CareRequest(Eid,Yid,Status) VALUES(?,?,?)'
					c.execute(insert,(eid,Yid,'Pending'))
					db.commit()
					print("Request Sent")
	def review_rating(self):
		with sqlite3.connect("Edyoda.db") as db:
			c=db.cursor()
		choice='y'
		while choice!='n':
			c.execute('Select e.id,e.Name from CareRequest c left join Elders e on c.eid=e.id where yid=? and c.status=?',(self.Yid,'Accepted'))
			results=c.fetchall()
			option=int(input("Press 1 to review\nPress 2 to exit "))
			if option==2:
				break
			if len(results)>0:
				for i in range(0,len(results)):
					print("Elder id: "+str(results[i][0])+" Name: "+results[i][1]+"\n")
				eid=int(input("Please enter the Elder Id you would like to Review "))
				c.execute('Select * from ElderReview where eid=? and ReviewedBy=?',(eid,self.Yid))
				results=c.fetchall()
				if len(results)!=0:
					print("Already Reviewed")
				else:
					r=0
					try:
						while r==0: 
							Rating=int(input("Please Rate out of 5 "))
							if Rating>5 or Rating<0:
								print("Out of 5 Only ")
							else:
								r=1
					except:
						print("Something Went Wrong ")
						pass
					Review=input("Please Review in less than 500 words ")
					c.execute('insert into ElderReview(Eid,ReviewedBy,Rating,Review) VALUES(?,?,?,?)',(eid,self.Yid,Rating,Review))
					db.commit()
					print("Review Posted")
					option=input("Do you wish to post more reviews y/n?").lower().strip()
					if option[0]=='n':
						option='n'
						break
					elif option[0]=='y':
						option='y'
					else:
						print("Only Yes or No. Please Try again")
						option='y'
			else:
				print("Nothing to review now")
				break
	def request_updates(self):
		with sqlite3.connect("Edyoda.db") as db:
			c=db.cursor()
		c.execute('Select careid,Eid,Status from CareRequest where yid=?',(self.Yid,))
		results=c.fetchall()
		if len(results)<=0:
			print("You have not yet request to take care of any elders ")
		else:
			for i in range(0,len(results)):
				print("CareId: "+str(results[i][0])+" ElderId: "+str(results[i][1])+" Status: "+results[i][2]+"\n")	
	def elder_details(self):
		with sqlite3.connect("Edyoda.db") as db:
			c=db.cursor()
		query='Select c.careid,e.id,e.name,e.age,e.contact from CareRequest c left join elders e on c.eid=e.id where yid=? and status=?'
		c.execute(query,(self.Yid,'Accepted'))
		results=c.fetchall()
		if len(results)<=0:
			print("Currently You dont have any Elders registered under you ")
		else:
			for i in range(0,len(results)):
				print("Request Id: "+str(results[i][0])+" Elder Id "+str(results[i][1])+" Elder Name: "+results[i][2]+" Age: "+str(results[i][3])+" Contact: "+str(results[i][4])+"\n")
			print("Total Elders Currently under you: "+str(len(results)))
	def Check_Ratings(self):
		with sqlite3.connect("Edyoda.db") as db:
			c=db.cursor()
		choice='y'
		c.execute('Select y.Review,e.name from YoungReview y left join elders e on y.ReviewedBy=e.id where yid=?',(self.Yid,))
		results=c.fetchall()
		if len(results)<=0:
			print("No reviews yet to show ")
		else:
			for i in range(0,len(results)):
				print("Name: "+results[i][1]+"\nReview: "+results[i][0])
def initiate():
	e=Young()
	i=0
	while i!=1:
		try:
			choice=input("Are you and existing user [y/n] ").lower().strip()
			if choice[0]=='y':
				trial=1
				login_try=0
				while login_try!=1 and trial<4:#3 login attempts
					login_try=e.existing_user(input("Enter UserName "),input("Enter Password "))
					if login_try==1:
						break
					else:
						if trial==3:
							print("Maximum login attempts reached")
							break
						else:
							trial=trial+1
			elif choice[0]=='n':
				print("Please enter your Details ")
				e.new_user(input("Name "),int(input("Age ")),int(input("Contact ")),input("UserName "),input("Password "))
			else:
				print("Please enter Y/N ")
			i=1
		except:
			print("Please Try again ")
			pass
initiate()