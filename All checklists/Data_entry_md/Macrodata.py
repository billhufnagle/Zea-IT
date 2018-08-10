#A GUI for taking the grow room, cold room, and processing room data
#

from tkinter import *
import datetime
import MySQLdb

class Data_entry:

    def __init__(self, master):
        self.master = master
        master.title("Grow Room Data Entry")

        #self.rackval=""
        #self.ltsval=""
        #self.pltsval=""
        #self.wtrflwval=""
        #self.res50val=""
        #self.pmpsval=""
        #self.ipmval=""         Might use these at another time
        #self.airval=""         to check if input is there
        #self.drpleakval=""
        #self.riserval=""
        #self.commentsval=""
        #self.riserholding=""


        #Labels
        self.emptylabel = Label(master, text="")
        self.secondempty = Label(master, text="")
        self.thirdempty = Label(master, text="")
        self.fourthempty = Label(master, text="")
        self.fifthempty = Label(master, text="")
        self.sixthempty = Label(master, text="")
        #self.errorlab = Label(master, text="ERROR: All inputs must be numbers, except for comments", fg="red")
        self.workerlab = Label(master, text="Initials of data collector")
        self.roomlab = Label(master, text="Room number: ")
        self.excesslab = Label(master, text="Excess Items(0/1): ")
        self.co2lab = Label(master, text="CO2 Level~1500: ")
        self.growtemplab = Label(master, text="Temp(F)~72: ")
        self.growhumidlab = Label(master, text="Humidity(%)~58: ")
        self.cornvalvlab = Label(master, text="Corner Valves Off(0/1): ")
        self.templab = Label(master, text="Temp(F)~39.43: ")
        self.grwrmlab = Label(master, text="--Grow Room--")
        self.procrmlab = Label(master, text="--Processing Room--")
        self.cldrmlab = Label(master, text="--Cold Room--")
        self.instrlab = Label(master, text="Only do one column at a time!", bg="red", fg="white")#, bg="white")
        self.comments = Label(master, text = "--Comments--")

        #Entry boxes
        vcmd = master.register(self.validate)
        commentvcmd = master.register(self.commentvalidate)
        tempvcmd= master.register(self.validatefloat)
        self.initials = Entry(master, validate = "key", validatecommand = (commentvcmd, '%P'))
        self.grwrm = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.procrm = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.cldrm = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.excess = Entry(master, validate="key", validatecommand = (vcmd, '%P'))
        self.co2 = Entry(master, validate="key", validatecommand = (vcmd, '%P'))
        self.grwtemp = Entry(master, validate="key", validatecommand = (tempvcmd, '%P'))
        self.humid = Entry(master, validate="key", validatecommand = (vcmd, '%P'))
        self.corner = Entry(master, validate="key", validatecommand = (vcmd, '%P'))
        self.cldtemp = Entry(master, validate="key", validatecommand = (tempvcmd, '%P'))
        self.excesscmnt = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.co2cmnt = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.grwtempcmnt = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.humidcmnt = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.cornercmnt = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))
        self.cldtempcmnt = Entry(master, validate="key", validatecommand = (commentvcmd, '%P'))

        #Radio buttons
        self.option = StringVar()
        self.option.set(None)
        self.grwrmbtn=Radiobutton(master, text="Grow Room", variable=self.option, value = "GrowRoom")
        self.procrmbtn=Radiobutton(master, text="Processing Room", variable=self.option, value="ProcessingRoom")
        self.cldrmbtn=Radiobutton(master, text="Cold Room", variable=self.option, value = "ColdRoom")

        #Submit button
        self.submit_button = Button(master, text="Submit", command=lambda: self.submit())

        #Layout
        self.workerlab.grid(row=0, column=3)
        self.initials.grid(row=0, column=4, columnspan=2)

        self.grwrmbtn.grid(row=1, column=1)
        self.procrmbtn.grid(row=1, column=3)
        self.cldrmbtn.grid(row=1, column=5)

        self.grwrmlab.grid(row=5, column=1)
        self.emptylabel.grid(row=5, column=2)
        self.procrmlab.grid(row=5, column=3)
        self.secondempty.grid(row=5, column=4)
        self.cldrmlab.grid(row=5, column=5)
        self.thirdempty.grid(row=5, column=6)
        self.comments.grid(row=5, column=7)
        master.grid_columnconfigure(1, minsize=20)
        master.grid_columnconfigure(3, minsize=20)
        master.grid_columnconfigure(5, minsize=20)

        self.roomlab.grid(row=10, column=0, sticky=E)
        self.excesslab.grid(row=11, column=0, sticky=E)
        self.co2lab.grid(row=15, column=0, sticky=E)
        self.growtemplab.grid(row=20, column=0, sticky=E)
        self.growhumidlab.grid(row=25, column=0, sticky=E)
        self.cornvalvlab.grid(row=30, column=0, sticky=E)
        self.templab.grid(row=35, column=0, sticky=E)

        self.grwrm.grid(row=10, column=1, sticky=W+E)
        self.procrm.grid(row=10, column=3, sticky=W+E)
        self.cldrm.grid(row=10, column=5, sticky=W+E)

        self.excess.grid(row=11, column=1, sticky=W+E)
        self.co2.grid(row=15, column=1, sticky=W+E)
        self.grwtemp.grid(row=20, column=1, sticky=W+E)
        self.humid.grid(row=25, column=1, sticky=W+E)
        self.corner.grid(row=30, column=3, sticky=W+E)
        self.cldtemp.grid(row=35, column=5, sticky=W+E)

        self.excesscmnt.grid(row=11, column=7, sticky=W+E)
        self.co2cmnt.grid(row=15, column=7, sticky=W+E)
        self.grwtempcmnt.grid(row=20, column=7, sticky=W+E)
        self.humidcmnt.grid(row=25, column=7, sticky=W+E)
        self.cornercmnt.grid(row=30, column=7, sticky=W+E)
        self.cldtempcmnt.grid(row=35, column=7, sticky=W+E)

        self.submit_button.grid(row=40, column=7, sticky=W+E)

        self.emptycmnt=self.cldtempcmnt.get()
        self.emptynum=self.grwrm.get()

        self.db = MySQLdb.connect("localhost", "root", "password", "datacollection")

        self.cursor = self.db.cursor()
        self.initialshold=self.initials.get()
    #Methods


    def commentvalidate(self, new_text):
        if not new_text:
            return True
        try:
            str(new_text)           #ensures input can be made into string
            return True
        except ValueError:
            return False

    def validate(self, new_text):
        if not new_text:
            return True
        try:
            int(new_text)          #checks so that input is only int
            return True            #other chars can't be input
        except ValueError:
            return False

    def validatefloat(self, new_text):
        if not new_text:
            return True
        for i in range(len(new_text)):
            if new_text[i] in '1234567890.':
                try:
                    float(new_text)
                    print ("working")
                    return True
                except:
                    print ("can't float")
                    return False
            else:
                print ("not in string")
                return False
    def clearcells(self):
        #self.initials.delete(0, END)
        self.grwrm.delete(0, END)
        self.excess.delete(0, END)
        self.co2.delete(0, END)
        self.grwtemp.delete(0, END)
        self.humid.delete(0, END)
        self.procrm.delete(0,END)
        self.corner.delete(0, END)
        self.cldrm.delete(0, END)
        self.cldtemp.delete(0, END)
        self.excesscmnt.delete(0, END)
        self.co2cmnt.delete(0, END)
        self.grwtempcmnt.delete(0, END)
        self.humidcmnt.delete(0, END)
        self.cornercmnt.delete(0, END)
        self.cldtempcmnt.delete(0, END)

    def submit(self):
        if self.initials.get()==self.emptycmnt:
            return
        if (self.grwrm.get()==self.emptycmnt and self.cldrm.get()==\
            self.emptycmnt)and self.procrm.get()==self.emptycmnt:
            return
        mysqlstring=None
        initials=list(self.initials.get())
        for i in range(len(initials)):
            if ord(initials[i])==92:
                initials[i]='backslash'
            if initials[i]==',':
                initials[i]=';'
            if initials[i]=='"':
                initials[i]='dblquote'
            if initials[i] == "'":
                initials[i]= 'snglquote'
        initials="'"+"".join(initials)+"'"
        if self.option.get() == "GrowRoom":

            grwrm=list(self.grwrm.get())
            excesscmnt=list(self.excesscmnt.get())
            co2cmnt=list(self.co2cmnt.get())
            grwtempcmnt=list(self.grwtempcmnt.get())
            humidcmnt=list(self.humidcmnt.get())

            for i in range(len(grwrm)):
                if ord(grwrm[i])==92:
                    grwrm[i]='backslash'
                if grwrm[i]==',':
                    grwrm[i]=';'
                if grwrm[i]=='"':
                    grwrm[i]='dblquote'
                if grwrm[i] == "'":
                    grwrm[i]= 'snglquote'
            grwrm="'"+"".join(grwrm)+"'"

            for i in range(len(excesscmnt)):
                if ord(excesscmnt[i])==92:
                    excesscmnt[i]='backslash'
                if excesscmnt[i]==',':
                    excesscmnt[i]=';'
                if excesscmnt[i]=='"':
                    excesscmnt[i]='dblquote'
                if excesscmnt[i] == "'":
                    excesscmnt[i]= 'snglquote'
            excesscmnt="'"+"".join(excesscmnt)+"'"

            for i in range(len(co2cmnt)):
                if ord(co2cmnt[i])==92:
                    co2cmnt[i]='backslash'
                if co2cmnt[i]==',':
                    co2cmnt[i]=';'
                if co2cmnt[i]=='"':
                    co2cmnt[i]='dblquote'
                if co2cmnt[i] == "'":
                    co2cmnt[i]= 'snglquote'
            co2cmnt="'"+"".join(co2cmnt)+"'"

            for i in range(len(grwtempcmnt)):
                if ord(grwtempcmnt[i])==92:
                    grwtempcmnt[i]='backslash'
                if grwtempcmnt[i]==',':
                    grwtempcmnt[i]=';'
                if grwtempcmnt[i]=='"':
                    grwtempcmnt[i]='dblquote'
                if grwtempcmnt[i] == "'":
                    grwtempcmnt[i]= 'snglquote'
            grwtempcmnt="'"+"".join(grwtempcmnt)+"'"

            for i in range(len(humidcmnt)):
                if ord(humidcmnt[i])==92:
                    humidcmnt[i]='backslash'
                if humidcmnt[i]==',':
                    humidcmnt[i]=';'
                if humidcmnt[i]=='"':
                    humidcmnt[i]='dblquote'
                if humidcmnt[i] == "'":
                    humidcmnt[i]= 'snglquote'
            humidcmnt="'"+"".join(humidcmnt)+"'"

            excess=self.excess.get()
            co2=self.co2.get()
            grwtemp=self.grwtemp.get()
            humid=self.humid.get()


            if self.grwrm.get()==self.emptycmnt:
                grwrm='NULL'
            if self.excess.get()==self.emptynum:
                excess='NULL'
            if self.co2.get()==self.emptycmnt:
                co2='NULL'
            if self.grwtemp.get()==self.emptynum:
                grwtemp='NULL'
            if self.humid.get()==self.emptynum:
                humid='NULL'
            if self.excesscmnt.get()==self.emptycmnt:
                excesscmnt='NULL'
            if self.co2cmnt.get()==self.emptycmnt:
                co2cmnt='NULL'
            if self.grwtempcmnt.get()==self.emptycmnt:
                grwtempcmnt='NULL'
            if self.humidcmnt.get()==self.emptycmnt:
                humidcmnt='NULL'


            holdingstring=""+grwrm+','+excess+','\
                           +co2+','+grwtemp+','+\
                           humid+','+excesscmnt+','\
                           +co2cmnt+','+grwtempcmnt+\
                           ','+humidcmnt+','+initials
            time=datetime.datetime.now().strftime(", '%A', '%Y-%m-%d %H:%M:%S'")
            mysqlstring='('+holdingstring+time+')'
            holdingstring=holdingstring+time+"\n"
            #print (holdingstring)
            output = open("GrowRoomData.csv", 'a+')
            output.write(holdingstring)
            output.close()
            print (mysqlstring)
            print (len(list(mysqlstring)))
            self.cursor.execute("""INSERT INTO growroommacro (Room, Excessitems\
, Co2, Temp, Humidity, Excessitems_comments, Co2_comments, Temp_comments, \
Humidity_comments, Initials, Day, Date) VALUES """ + mysqlstring)

            self.db.commit()
            self.clearcells()


        elif self.option.get() == "ProcessingRoom":

            procrm=list(self.procrm.get())
            cornercmnt=list(self.cornercmnt.get())
            corner=self.corner.get()

            for i in range(len(procrm)):
                if ord(procrm[i])==92:
                    procrm[i]='backslash'
                if procrm[i]==',':
                    procrm[i]=';'
                if procrm[i]=='"':
                    procrm[i]='dblquote'
                if procrm[i] == "'":
                    procrm[i]= 'snglquote'
            procrm="'"+"".join(procrm)+"'"

            for i in range(len(cornercmnt)):
                if ord(cornercmnt[i])==92:
                    cornercmnt[i]='backslash'
                if cornercmnt[i]==',':
                    cornercmnt[i]=';'
                if cornercmnt[i]=='"':
                    cornercmnt[i]='dblquote'
                if cornercmnt[i] == "'":
                    cornercmnt[i]= 'snglquote'
            cornercmnt="'"+"".join(cornercmnt)+"'"

            if self.procrm.get()==self.emptycmnt:
                procrm='NULL'
            if self.cornercmnt.get()==self.emptycmnt:
                cornercmnt='NULL'
            if self.corner.get()==self.emptynum:
                corner='NULL'

            holdingstring=procrm+", "+ corner+", "\
                           +cornercmnt+", "+\
                            initials+","
            time=datetime.datetime.now().strftime(" '%A', '%Y-%m-%d %H:%M:%S'")
            mysqlstring='('+holdingstring+time+')'
            holdingstring=holdingstring+time+"\n"
            #print (holdingstring)
            output = open("ProcRoomData.csv", 'a+')
            output.write(holdingstring)
            output.close()
            print (mysqlstring)
            print (len(list(mysqlstring)))
            self.cursor.execute("""INSERT INTO procroommacro (Room, Cornervalves\
off, Cornervalves_comments, Initials, Day, Date) VALUES """ + mysqlstring)

            self.db.commit()
            self.clearcells()

        elif self.option.get() == "ColdRoom":

            cldrm=list(self.cldrm.get())
            cldtempcmnt=list(self.cldtempcmnt.get())



            for i in range(len(cldrm)):
                if ord(cldrm[i])==92:
                    cldrm[i]='backslash'
                if cldrm[i]==',':
                    cldrm[i]=';'
                if cldrm[i]=='"':
                    cldrm[i]='dblquote'
                if cldrm[i] == "'":
                    cldrm[i]= 'snglquote'
            cldrm="'"+"".join(cldrm)+"'"

            for i in range(len(cldtempcmnt)):
                if ord(cldtempcmnt[i])==92:
                    cldtempcmnt[i]='backslash'
                if cldtempcmnt[i]==',':
                    cldtempcmnt[i]=';'
                if cldtempcmnt[i]=='"':
                    cldtempcmnt[i]='dblquote'
                if cldtempcmnt[i] == "'":
                    cldtempcmnt[i]= 'snglquote'
            cldtempcmnt="'"+"".join(cldtempcmnt)+"'"

            cldtemp=self.cldtemp.get()

            if self.cldrm.get()==self.emptycmnt:
                cldcrm='NULL'
            if self.cldtempcmnt.get()==self.emptycmnt:
                cldtempcmnt='NULL'
            if self.cldtemp.get()==self.emptynum:
                cldtemp='NULL'

            holdingstring=cldrm+", "+cldtemp+', '+cldtempcmnt+', '+\
                           initials+','
            time=datetime.datetime.now().strftime(" '%A', '%Y-%m-%d %H:%M:%S'")
            mysqlstring='('+holdingstring+time+')'
            holdingstring=holdingstring+time+"\n"
            #print (holdingstring)
            output = open("ColdRoomData.csv", 'a+')
            output.write(holdingstring)
            output.close()
            print (mysqlstring)
            print (len(list(mysqlstring)))
            self.cursor.execute("""INSERT INTO coldroommacro (Room, Temp\
, Temp_comments, Initials, Day, Date) VALUES """ + mysqlstring)

            self.db.commit()
            self.clearcells


        #print (mysqlstring)




root=Tk()

my_gui=Data_entry(root)

root.mainloop()
