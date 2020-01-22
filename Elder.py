import sqlite3
with sqlite3.connect('Edyoda.db') as db:
    c = db.cursor()

class Elders:#Elder Class
	def __init__(self):
		self.Uname=str
		self.pwd=str
		self.eid=str
	def new_user(self,Name,Age,Contact,Uname,pwd):#login for new user "Sign Up"
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
		c.execute('Select * from Elders where Uname="'+Uname+'";')
		results=c.fetchall()
		if len(results)==0:
			insert = "INSERT INTO Elders(Name,Age,Contact,Uname,pwd) VALUES(?,?,?,?,?)"
			c.execute(insert,(Name,Age,Contact,Uname,pwd))
			db.commit()
			self.Uname=Uname
			self.pwd=pwd
			print("Congrats Account Created Start Exploring")
			self.existing_user(Uname,pwd)
		else:
			Eid=input("Please enter your id")
			results=c.execute('Select * from Elders where id="'+Eid+'";')
			if len(results)==0:
				print("UserName Already Exists")
			else:
				print("Profile Exists")
	def existing_user(self,Uname,pwd):#Login for Existing User
		self.Uname=Uname
		self.pwd=pwd
		self.Eid=str
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
		c.execute('Select id from Elders where Uname= ? and pwd=? ;',(Uname,pwd))
		results=c.fetchall()
		if len(results)==0:
			print("Please Enter Correct Details")
			return 0
		else:
			self.eid=results[0][0]
			print("Welcome")
			try:
				option='y'
				while option!='n':
					print("\n")
					self.user_options()
					choice=int(input())
					if choice==1:
						self.make_available()
					elif choice==2:
						self.check_Request()
					elif choice==3:
						self.review_rating()
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
			except Exception as E:
				print(E)
			return 1
	def make_available(self):#Enlist Themselves for being taken care by young people and allocation of funds for the same.
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
			c.execute('Select Available from Elders where Uname=?',(self.Uname,))
			results=c.fetchall()
			print(results[0][0])
			if results[0][0]=='NO':
				c.execute('Select count(*) from CareRequest where eid=? and Status=?',(self.eid,'Accepted'))
				results=c.fetchall()
				#print(results[0][0])
				if results[0][0]==0:
					c.execute('Update Elders set Available=? where Uname=?',('YES',self.Uname))
					funds=int(input(("Please allocate your Funds to proceed ")))
					c.execute('Update Elders set Funds=? where Uname=?',(funds,self.Uname))
					db.commit()
					print("Now You will shown as 'Available' to the CareTaker")
				else:
					print("You have already accepted a request")
			if results[0][0]=='YES':
				c.execute('Update Elders set Available=? where Uname=?',('NO',self.Uname))
				c.execute('Update Elders set Funds=? where Uname=?',(0,self.Uname))
				c.execute('Delete from CareRequest where eid=?',(self.Eid,))
				db.commit()
				print("Now You will not be shown to the CareTaker")
	def check_Request(self):#Function to Check Young Lads requests for taking care
		with sqlite3.connect('Edyoda.db') as db:
			c=db.cursor()
		c.execute('Select id from Elders where Uname=?',(self.Uname,))
		results=c.fetchall()
		Eid=results[0][0]
		self.eid=Eid
		insert='Select c.yid,y.Name,y.Age,y.Rating,y.ElderCount from CareRequest c left join Young y on c.Yid=y.id where c.eid=? and c.Status <>?'
		c.execute(insert,(Eid,'Declined'))
		results=c.fetchall()
		if len(results)!=0:
			for i in range(0,len(results)):
				print("CareTaker id: "+str(results[i][0])+" Name: "+results[i][1]+" Age: "+str(results[i][2])+" Rating: "+str(results[i][3])+" Elders Present: "+str(results[i][4])+"\n")
			choice=0
			while choice!=4:
				choice=int(input("Press 1 to accept the request\nPress 2 to reject request\nPress 3 to read CareTaker's Reviews\nPress 4 to exit\n"))
				if choice==1:
					yid=int(input("Please Enter CareTaker's Id: "))
					c.execute('Select ElderCount from young where id=?',(yid,))
					results=c.fetchall()
					c.execute('Select * from CareRequest where eid=? and yid=? and status=?',(Eid,yid,'Accepted'))
					results1=c.fetchall()
					if results[0][0]==None:
						ec=0
					else:
						ec=results[0][0]
					if ec<4 and ec>=0 and len(results1)==0:
						c.execute("Update CareRequest set Status=? where yid=? and eid=?",('Accepted',yid,Eid))
						c.execute('Update Young set ElderCount=? where id=?',(ec+1,yid))
						c.execute('update elders set previous=? where id=?',(yid,Eid))
						c.execute('update young set previouselder=? where id=?',(Eid,yid))
						c.execute("Update CareRequest set Status=? where eid=? and yid<>?",('Declined',Eid,yid))
						c.execute('Update Elders set available=? where id=?',('No',Eid))
						db.commit()
						print("Registered under "+str(yid)+" for care\n")
						break
					else:
						if len(results1)!=0:
							print("You are already Registered under this CareTaker ")
						else:
							print("Maximum Elders are already present with the CareTaker\nPlease choose a different CareTaker ")
							break
				elif choice==2:
					yid=int(input("Please Enter CareTaker's Id: "))
					c.execute('Select * from CareRequest where status=? and yid=?',('Accepted',yid))
					results=c.fetchall()
					if len(results)==0:
						c.execute("Update CareRequest set Status=? where yid=?",('Declined',yid))
						db.commit()
						print("Request Declined for the care taker with id "+str(yid))
					else:
						print("Cannot decline the already Accepted requests")
				elif choice==3:
					option='y'
					while option!='n':
						yid=int(input("Please Enter CareTaker's Id: "))
						c.execute('Select rid,review from YoungReview where yid=?',(yid,))
						results=c.fetchall()
						if len(results)!=0:
							for i in range(0,len(results)):
								print("Review Id: "+str(results[i][0])+" Review: "+results[i][1])
						else:
							print("No reviews posted yet")
						option=input("Wish to see more Reviews [y/n]").lower().strip()
						if option[0]=='n':
							option='n'
						elif option[0]=='y':
							option='y'
						else:
							print("Only Yes or No. Please Try again")
							option='y'
				else:
					break
		else:
			print("Currently You Dont Have any pending Requests")		
	def review_rating(self):#Function for giving ratings and reviews.
		with sqlite3.connect("Edyoda.db") as db:
			c=db.cursor()
		choice='y'
		c.execute('Select id from Elders where Uname=?',(self.Uname,))
		results=c.fetchall()
		Eid=results[0][0]
		while choice!='n':
			c.execute('Select y.id,y.Name from CareRequest c left join Young y on c.yid=y.id where Eid=? and c.status=?',(Eid,'Accepted'))
			results=c.fetchall()
			option=int(input("Press 1 to review\nPress 2 to exit "))
			if option==2:
				break
			if len(results)>0:
				for i in range(0,len(results)):
					print("CareTaker id: "+str(results[i][0])+" Name: "+results[i][1]+"\n")
				yid=int(input("Please enter the CareTaker Id you would like to Review "))
				c.execute('Select count(*) from YoungReview where yid=? and ReviewedBy=?',(yid,Eid))
				results=c.fetchall()
				if results[0][0]!=0:
					print("Already Reviewed")
					break
				else:
					try:
						r=0
						while r==0: 
							Rating=int(input("Please Rate out of 5 "))
							if Rating>5 or Rating<0:
								print("Out of 5 Only ")
							else:
								r=1
					except:
						print("Something went Wrong")
						pass
					Review=input("Please Review in less than 500 words ")
					c.execute('insert into YoungReview(Yid,ReviewedBy,Rating,Review) VALUES(?,?,?,?)',(yid,Eid,Rating,Review))
					db.commit()
					print("Review Posted")
					option=input("Do you wish to post more reviews y/n?").lower().strip()
					if option[0]=='n':
							option='n'
					elif option[0]=='y':
						option='y'
					else:
						print("Only Yes or No. Please Try again")
						option='y'
			else:
				print("Nothing to review now")
				break
	def Check_Ratings(self):#Function to see ones rating and reviews by other Caretakers
		with sqlite3.connect("Edyoda.db") as db:
			c=db.cursor()
		choice='y'
		c.execute('Select id from Elders where Uname=?',(self.Uname,))
		results=c.fetchall()
		Eid=results[0][0]
		c.execute('Select e.Review,y.name from ElderReview e left join young y on e.ReviewedBy=y.id where eid=?',(Eid,))
		results=c.fetchall()
		if len(results)<=0:
			print("No reviews yet to show ")
		else:
			for i in range(0,len(results)):
				print("Name: "+results[i][1]+"\nReview: "+results[i][0])
	def user_options(self):#Main Menu Options
		print("Press 1 to Make/Unmake yourself available ")
		print("Press 2 to see CareTaker requests")
		print("Press 3 to Rate and Review your CareTaker ")
		print("Press 4 to Check your Rating and Reviews given by CareTakers")
def initiate():#Object Inititation and function calling
	e=Elders()
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