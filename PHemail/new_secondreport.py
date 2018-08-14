import datetime
import MySQLdb
import emailattempt as mail
import pprint
import bs4 as Soup
import lxml
xmlsource=open("config.xml", 'r')

config=Soup.BeautifulSoup(xmlsource, 'lxml')


print (config.email.tto.text.split(","))

text=config.database.threshold_numbers.text
print (text)
i=0
j=0
holding=[]
torf=False
finallist=[]
while i < len(text):
    if text[i]==']':
        finallist.append(holding)
        holding=[]
        torf=False
    if torf==True:
        try:
            holding.append(int(text[i]))
        except:
            print('error')
    if text[i]=='[':
        torf=True
        
    i+=1
print (finallist[1][0])

rowslist = config.database.rows.text.split(',')

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
ListOfFactors=config.database.factors.text.split(',')
NumbToNote=finallist
Rows=rowslist
Date=config.database.date.text

db = MySQLdb.connect(hostname, user, password_db, dbname)
open('tempfile.txt','w')
cursor=db.cursor()
message=''
tempfile=open('tempfile.txt', 'w')
current=datetime.datetime.now()
#these if statements create the time specific part of the sql statement
if Date=='Week':
    dateline=" between " + (current-datetime.timedelta(days=7))\
                 .strftime("'%Y-%m-%d'") +" And "+current.strftime("'%Y-%m-%d'")

elif Date=='Month':
    dateline=" between " + (current-datetime.timedelta(days=31))\
              .strftime("'%Y-%m-%d'")+" And " + current.strftime("'%Y-%m-%d'")

elif Date=='Quarter':
    dateline=" between " + (current-datetime.timedelta(days=93))\
              .strftime("'%Y-%m-%d'")+ " And " + current.strftime("'%Y-%m-%d'")
    

elif Date=='Year':
    dateline=" between " + (current-datetime.timedelta(days=365))\
              .strftime("'%Y-%m-%d'")+ " And " + current.strftime("'%Y-%m-%d'")
else:
    dateline="=" + current.strftime("'%Y-%m-%d'")

    
for i in range(len(ListOfFactors)):
    for j in range(len(NumbToNote[i])):
        factor=(ListOfFactors[i])
        message=message+"------"+str(factor)+ ': '+ str(NumbToNote[i][j]) +\
                 '-------\n'
        for k in Rows:
            linetoexec="select Rack,"+ListOfFactors[i]+"_comments"
            linetoexec+=" , Date From growroomwalkthrough\n Where "
            linetoexec+=ListOfFactors[i]+"="
            linetoexec+=str(NumbToNote[i][j])
            linetoexec+=" And Rack="+str(k)+" And Date(Date)"+dateline
            linetoexec+=" Order By Room, Rack, Date;"
            #print(linetoexec)
            cursor.execute(linetoexec)
            holding=cursor.fetchall()
            lastmessage=message
            for l in range(len(holding)):
                new=''
                next=holding[l]
                print (next)
                new+=next[0]+ ' '+str(next[1])+' '+ next[2].strftime\
                      ('%Y-%m-%d %H:%M:%S')+'\n'
                #tempfile.write(str(new))
                #tempfile.write('\n')
                if message!= message+new:
                    message=message+new
            if message!=lastmessage:
                message=message+'\n'

        message=message+'\n\n'  
print (linetoexec)
pprint.pprint(message)

#for i in range(len(message)):
    #print (type(message[i]))
    #if type(message[i])!= str:
    #    try :
   #         message[i]=list(message[i])
  #      except : 
 #           1+1
#print(message)
#for i in range(len(message)):
#    try:
   #     for j in range(len(message[i])):
  #          if type(message[i][j]) is not str:
 #               message[i][j]=str(message[i][j])
#    except:
     #   if type(message[i])==int:
    #        message[i]=' '+str(message[i])
   #     1+1
#print (message)
#for i in range(len(message)):
 #   if type(message[i])==list:
  #      message[i]=''.join(message[i])

#print(message)

tempfile.close()

#pprint.pprint (message)
print(tto)
mail.outlooksimple(sender, tto, login, password_email,\
                  subject, False, str(message)) 
