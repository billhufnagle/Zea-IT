import datetime
import MySQLdb
import emailattempt
import pprint

sender="bhufnagle@zeabio.com"
tto="tschutz@zeabio.com"
login="bhufnagle@zeabio.com"
password="temp$1234"
subject="Attempting automated email"
file=False
message="This is where the info will be"


hostname="localhost"
user="root"
password="password"
dbname="datacollection"
ListOfFactors=["Lights", "Plants", "WaterFlow", "Reservoir50", "Pumps", "IPM",\
               "Airators", "NoDripsLeaks", "Risers"]
NumbToNote=[[1],[1],[1],[1],[1],[2,3],[1],[1],[1]]
#NumberOfRows=18

db = MySQLdb.connect(hostname, user, password, dbname)

cursor=db.cursor()
for i in range(len(ListOfFactors)):
      for j in range(len(NumbToNote[i])):
        linetoexec="select Rack,"+ListOfFactors[i]+"_comments"
        linetoexec+=" , Date From growroomwalkthrough\n Where "
        linetoexec=linetoexec+ListOfFactors[i]+"="
        linetoexec+=str(NumbToNote[i][j])+";"
        print(linetoexec)
        cursor.execute(linetoexec)
        pprint.pprint(cursor.fetchall())

pprint.pprint(cursor.fetchall())
