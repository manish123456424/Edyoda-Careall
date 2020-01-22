The Python Script Consits of 4 files.
1.Elder.py
2.Young.py
3.Admin.py
4.Main.py
------------------------------Elder.py-----------------------------------------------------------------------------
This file consists of the Elder Class.
Which Consists of the following methods.
1.new login
2.Existing login
3.User Option- The main menu
4.Make available- here the elder people can make themselves available and unavailable. if they are making themselves available they need to allocate funds. Post this they will be shown to young lads.
5.Check Request- here the elder people can see the caretakers request to care for them. Elders can either accept or decline the requests.
6.Review Rating- The elders can review and rate the caretaker under whom they have been assigned.
7.Check Rating- The elders can see their reviews given by their care takers.

----------------------------Young.py-------------------------------------------------------------------------------
This file contains Youn class.
Which Consists of the following methods.
1.new login
2.Existing login
3.User Option- The main menu
4.Start Caring- Here the young people can see the available elder people and can send a request to them to start taking care for them.
5.Review Rating- The young can review and rate the Elderly under whom they have been assigned.
6.Request Updates- The young can see the status of the request sent to the elderly
7.Elder Details- The young can see the details of registered elder people under them.
8.Check Ratings- The young can see their reviews given by their elders.

-----------------------------------------------Admin.py------------------------------------------------------------
This file contains Admin class.
The admin username is root and Password is 1234 which is hardcoded.
The method consists of.
1. login
2. Status Check- here admin can view the following.
a. Who is taking care of Elder people.
b. See details of Elder people under Young people.

-----------------------------------------------Main.py-------------------------------------------------------------
This file contains main class
Over here by navigating the menu one can login as Elder,Young or Admin.
Based on the choices the respective class is called.

-----------------------------------------------Edyoda.db-----------------------------------------------------------
This is the database used in the program(Sqlite3 DB).
It consists of Following Table.
1. Elders - Details of Elders like name age contact etc.
2. Young - details of young like name age etc.
3. CareRequest- Table for request sent to elders by young
4. Young Review- Table to store the ratings and reviews of CareTakers given by elderly.
5. Elder Review- Table to store the ratings and reviews of elderly given by CareTakers.
-------------------------------------------------------------------------------------------------------------------