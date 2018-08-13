import datetime
import MySQLdb
import emailattempt as mail
import pprint
import time
start_time = time.time()
sender="bhufnagle@zeabio.com"
tto=["bhufnagle@zeabio.com", "dparlato@zeabio.com", "tschutz@zeabio.com", "jwilson@zeabio.com"]
login="bhufnagle@zeabio.com"
password_email="temp$1234"
subject=" report"
file=False
message="This is where the info will be"


hostname="localhost"
user="bhufnagle"
password_db="p1assword"
dbname="datacollection"
ListOfFactors=["Lights", "Plants", "WaterFlow", "Reservoir50", "Pumps", "IPM",\
               "Airators", "NoDripsLeaks", "Risers"]
NumbToNote=[[1],[1],[1],[1],[1],[2,3],[1],[1],[1]]
Rack=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
Room=[1]

db = MySQLdb.connect(hostname, user, password_db, dbname)
cursor=db.cursor()
message=''
now=str(datetime.datetime.now().strftime('%Y-%m-%d'))
DayofWeek=datetime.datetime.now().strftime('%A')
print (DayofWeek)
for i in range(len(ListOfFactors)):
    for j in range(len(NumbToNote[i])):
        factor=(ListOfFactors[i])
        message=message+str(factor)+ ' '+ str(NumbToNote[i][j]) + '\n'
        for k in Rack:
            for l in Room:
                linetoexec="select Rack,"+ListOfFactors[i]+"_comments"
                linetoexec+=" , Date From growroomwalkthrough\n Where "
                linetoexec=linetoexec+ListOfFactors[i]+"="
                linetoexec+=str(NumbToNote[i][j])
                linetoexec+=" And"+" Room="+str(l)+ " And Rack="+str(k)+" And Date(Date)="\
                         +'"'+now+'"'\
                         +" Order By Rack, Date;"
            #print(linetoexec)
            cursor.execute(linetoexec)
            holding=cursor.fetchall()
            lastmessage=message
            for l in range(len(holding)):
                new=''
                next=holding[l]
                #print (next)
                new+=next[0]+ ' '+str(next[1])+' '+ next[2].strftime\
                      ('%Y-%m-%d %H:%M:%S')+'\n'
                if message!= message+new:
                    message=message+new
            if message!=lastmessage:
                message=message+'\n'

        message=message+'\n\n'

#pprint.pprint(message)

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

x=time.time()
print ("---- %s seconds-----" %(x - start_time))
pprint.pprint (message)
print (tto)
mail.outlooksimple(sender, tto, login, password_email, DayofWeek+subject, False, str(message))
