#Simple email report. Takes all rows that match the current day
#as well as the rack numbers that are specified in the "configpH.xml doc
#there is no real formatting done to it, just a new line for each row and
#it is then all sent out to the recipients in the list in the config file
#and the sender is the "from" element in the file.

import datetime #time module in python. allows for datetime objects to be
import MySQLdb #the sql connector client
import emailattempt as mail #my module for emailing
import pprint #just a module for printing more clearly, makes lists print nicer
import bs4 as Soup #module called Beautiful Soup, used for xml/html parsing
import lxml #the parser needed for xml parsing by bs4 module

xmlsource=open("configpH.xml", 'r')

config=Soup.BeautifulSoup(xmlsource, 'lxml')


rowslist = config.database.rows.text.split(',')
j=0
while j < len(rowslist):
    rowslist[j]=int(rowslist[j])
    j+=1
print (rowslist)


sender=config.email.sender.text
tto=config.email.tto.text.split(',')
login=config.email.login.text
password_email=config.email.password.text
subject=config.email.subject.text
file=False


hostname=config.database.hostname.text
user=config.database.user.text
password_db=config.database.password.text
dbname=config.database.dbname.text
Rows=rowslist
Date=config.database.date.text

db = MySQLdb.connect(hostname, user, password_db, dbname)

cursor=db.cursor()
message=''
current=datetime.datetime.now()
dateline="="+current.strftime("'%Y-%m-%d'")
#dateline="=" + (current-datetime.timedelta(days=4)).strftime("'%Y-%m-%d'")

message=''

message+='Room, Rack, pH, DO, Temp, PPM, Initials, Date'

for i in Rows:
    message+='\n'
    message+=str(i)+'\n'
    executeline="select Room, Rack, pH, DO, Temp, PPM, Initials, Date(Date) from\
 waterreadings where Rack="+str(i)+" and Date(Date)"+dateline
    cursor.execute(executeline)
    current=list(cursor.fetchall()[0])
    current[7]=current[7].strftime("%m/%d/%Y")
    for i in range(len(current)):
        message+=str(current[i])+",   "

pprint.pprint(message)

print (tto)
mail.outlooksimple(sender, tto, login, password_email, subject, False, str(message))
