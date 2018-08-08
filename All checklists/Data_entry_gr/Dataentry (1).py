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
        self.errorlab = Label(master, text="ERROR: All inputs must be numbers, except for comments", fg="red")
        self.workerlab = Label(master, text="Initials of data collector")
        self.roomlab = Label(master, text="Room number: ")
        self.racklab = Label(master, text="Rack number: ")
        self.ltslab = Label(master, text="Lights: ", bg="white")
        self.pltslab = Label(master, text="Plants: ")
        self.wtrflwlab = Label(master, text="Water Flow: ", bg="white")
        self.res50lab = Label(master, text="Reservoir > 50%: ")
        self.pmpslab = Label(master, text="Pumps: ", bg="white")
        self.ipmlab = Label(master, text="IPM(1,2,3): ")
        self.airlab = Label(master, text="Airators: ", bg="white") 
        self.drpleaklab = Label(master, text="No Drips/Leaks: ")
        self.riserlab = Label(master, text="Risers: ", bg="white")
        self.commentslab = Label(master, text="---Comments---")
        self.dontfitup = Label(master, text = "0 = Good || 1 = Bad", bg="red", fg="white")
        self.seconddont = Label(master, text = "0 = Good || 1 = Bad", bg="red", fg="white")
        self.legend = Label(master, text = "----Key----")
        self.secondlegend = Label(master, text = "----Key----")
        self.daily = Label(master, text = "---Daily list---")
        self.weekend = Label(master, text = "---Weekend list---")
        self.weekendpmps = Label(master, text = "Pumps: ", bg="white")
        self.weekendmaniflw = Label(master, text = "Manifold Flow: ", bg="white")
        self.weekenddrpleak = Label(master, text = "No Drips/Leaks: ")
        self.weekendvisplts = Label(master, text = "Visual on Plants: ")
        self.ltsignore = Label(master, text = "Leave blank", fg="navy", bg="white")
        self.res50ignore = Label(master, text = "Leave blank", fg="navy")
        self.ipmignore = Label(master, text = "Leave blank", fg="navy")
        self.airignore = Label(master, text = "Leave blank", fg="navy", bg="white")
        self.riserignore = Label(master, text = "Leave blank", fg="navy", bg="white")
        self.keylabel = Label(master, text = "---Key---", fg = "black" , bg = "blue")
        self.lightskey = Label(master, text = "Lights: Multi, Bar, Diode")
        self.plantskey = Label(master, text = "Plants: Necrosis, Overgrown,\
Discolored, Wilted, Brown tipped roots, Brown Roots")
        self.ipmkey = Label(master, text = "IPM: Aphids, Thrips, Brown Mold, Damage to Leaves")
        self.waterflowkey = Label(master, text = "Waterflow: Where is the issue")
        self.pumpskey = Label(master, text = "Pumps: Record # if <90")
        self.dripskey = Label(master, text = "Drips: Observations. Why?")
        self.reportlab = Label(master, text = "Only send report when you have \
finished SUBMITTING all Racks", bg="navy", fg="white")
        
        #Entry boxes
        vcmd = master.register(self.validate) # validate command for int inputs
        commentvcmd = master.register(self.commentvalidate) #validate command for str inputs(worker, rack, room, comments)
        self.worker = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.room = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.rack = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.lts = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.ltscmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.plts = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.pltscmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.wtrflw = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.wtrflwcmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.res50 = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.res50cmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.pmps = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.pmpscmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.ipm = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.ipmcmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.air = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.aircmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.drpleak = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.drpleakcmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))
        self.riser = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.risercmnt = Entry(master, validate="key", validatecommand=(commentvcmd, '%P'))

        self.riserholding=self.riser.get()  #holding of empty strings to check

        #Submit button
        self.submit_button = Button(master, text="Submit", command=lambda: self.submit())
        self.report_button = Button(master, text="Send Email Report",\
                                    command=lambda: self.sendreport())
        
        # LAYOUT
        self.workerlab.grid(row=0, column=0, columnspan=3, sticky=W+E)

        self.worker.grid(row=1, column=0, columnspan=2, sticky=W+E)
        self.emptylabel.grid(row=1, column=3)
        
        self.roomlab.grid(row=2, column=0)
        self.room.grid(row=2, column=1, columnspan=1, sticky=W+E)

        self.racklab.grid(row=3, column=0)
        self.rack.grid(row=3, column=1, columnspan=1, sticky=W+E)

        self.secondlegend.grid(row=4, column=2)
        #self.secondempty.grid(row=4, column=0, columnspan=2)

        self.daily.grid(row=5, column=0)
        self.weekend.grid(row=5, column=1)
        self.seconddont.grid(row=5, column=2)
        self.commentslab.grid(row=5, column=4)
        
        self.ltslab.grid(row=6, column=0, sticky=W+E)
        self.ltsignore.grid(row=6, column=1, sticky=W+E)
        self.lts.grid(row=6, column=2, columnspan=1, sticky=W+E)
        self.ltscmnt.grid(row=6, column=4, columnspan=1, sticky=W+E)

        self.pltslab.grid(row=7, column=0, sticky=W+E)
        self.weekendvisplts.grid(row=7, column=1, sticky=W+E)
        self.plts.grid(row=7, column=2, columnspan=1, sticky=W+E)
        self.pltscmnt.grid(row=7, column=4, columnspan=1, sticky=W+E)

        self.wtrflwlab.grid(row=8, column=0, sticky=W+E)
        self.weekendmaniflw.grid(row=8, column=1, sticky=W+E)
        self.wtrflw.grid(row=8, column=2, columnspan=1, sticky=W+E)
        self.wtrflwcmnt.grid(row=8, column=4, columnspan=1, sticky=W+E) 

        self.res50lab.grid(row=9, column=0, sticky=W+E)
        self.res50ignore.grid(row=9, column=1, sticky=W+E)
        self.res50.grid(row=9, column=2, columnspan=1, sticky=W+E)
        self.res50cmnt.grid(row=9, column=4, columnspan=1, sticky=W+E)

        self.pmpslab.grid(row=10, column=0, sticky=W+E)
        self.weekendpmps.grid(row=10, column=1, sticky=W+E)
        self.pmps.grid(row=10, column=2, columnspan=1, sticky=W+E)
        self.pmpscmnt.grid(row=10, column=4, columnspan=1, sticky=W+E)

        self.ipmlab.grid(row=11, column=0, sticky=W+E)
        self.ipmignore.grid(row=11, column=1, sticky=W+E)
        self.ipm.grid(row=11, column=2, columnspan=1, sticky=W+E)
        self.ipmcmnt.grid(row=11, column=4, columnspan=1, sticky=W+E)

        self.airlab.grid(row=12, column=0, sticky=W+E)
        self.airignore.grid(row=12, column=1, sticky=W+E)
        self.air.grid(row=12, column=2, columnspan=1, sticky=W+E)
        self.aircmnt.grid(row=12, column=4, columnspan=1, sticky=W+E)

        self.drpleaklab.grid(row=13, column=0, sticky=W+E)
        self.weekenddrpleak.grid(row=13, column=1, sticky=W+E)
        self.drpleak.grid(row=13, column=2, columnspan=1, sticky=W+E)
        self.drpleakcmnt.grid(row=13, column=4, columnspan=3, sticky=W+E)

        self.riserlab.grid(row=14, column=0, sticky=W+E)
        self.riserignore.grid(row=14, column=1, sticky=W+E)
        self.riser.grid(row=14, column=2, columnspan=1, sticky=W+E)
        self.risercmnt.grid(row=14, column=4, columnspan=1, sticky=W+E)

        self.errorlab.grid(row=16, column=2, columnspan=2, sticky=W)

        self.legend.grid(row=17, column=2)

        self.dontfitup.grid(row=18, column=2)
        self.submit_button.grid(row=18, columnspan=1, column=4, sticky=W+E)

        self.keylabel.grid(row=19, columnspan=2, column=1, sticky=W+E)
        self.lightskey.grid(row=20, columnspan=2, column=1, sticky=W+E)
        self.plantskey.grid(row=21, columnspan=2, column=1, sticky=W+E)
        self.ipmkey.grid(row=23, columnspan=2, column=1, sticky=W+E)
        self.waterflowkey.grid(row=25, columnspan=2, column=1, sticky=W+E)
        self.pumpskey.grid(row=26, columnspan=2, column=1, sticky=W+E)
        self.dripskey.grid(row=27, columnspan=2, column=1, sticky=W+E)

        self.reportlab.grid(row=28, column=0, columnspan=2, sticky=W+E)
        self.report_button.grid(row=29, column=0, columnspan=2, sticky=W+E)
        
        master.grid_columnconfigure(0, minsize=200, weight=1)
        master.grid_columnconfigure(1, minsize=50, weight=1)
        master.grid_columnconfigure(2, minsize=50, weight=2)
        master.grid_columnconfigure(3, minsize=30)
        master.grid_columnconfigure(4, weight=2)

        self.errorclear()
        self.workerempty=self.worker.get()
        self.db = MySQLdb.connect("localhost", "root", "password", "datacollection")

        self.cursor = self.db.cursor()

        #Empty checkers
        self.emptynumb = self.lts.get()
        self.emptycmnt = self.ltscmnt.get()
    def errorclear(self):           #Error message removal
        self.errorlab.grid_forget()

    def errorhandle(self):          #error message showing
        self.errorlab.grid(row=16, column=1, columnspan=2, sticky=W)
    
    def commentvalidate(self, new_text):
        self.errorclear()           
        try:
            str(new_text)           #ensures input can be made into string
            return True
        except ValueError:
            return False
    
    def validate(self, new_text):
        self.errorclear()
        if not new_text:
            self.errorclear()
            return True
        try:
            int(new_text)
            self.errorclear()       #checks so that input is only int
            return True             #other chars can't be input
        except ValueError:
            self.errorhandle()
            return False

    def clearcells(self):
        #self.worker.delete(0, END) #commenting this out because the initials should stay same
                                    #almost every time, can still be manually deleted
        #self.room.delete(0, END)
        self.rack.delete(0, END)
        self.lts.delete(0, END)
        self.ltscmnt.delete(0, END)
        self.plts.delete(0, END)
        self.pltscmnt.delete(0, END)
        self.wtrflw.delete(0, END)
        self.wtrflwcmnt.delete(0, END)
        self.res50.delete(0, END)
        self.res50cmnt.delete(0, END)
        self.pmps.delete(0, END)
        self.pmpscmnt.delete(0, END)
        self.ipm.delete(0, END)
        self.ipmcmnt.delete(0, END)
        self.air.delete(0, END)
        self.aircmnt.delete(0, END)
        self.drpleak.delete(0, END)
        self.drpleakcmnt.delete(0, END)
        self.riser.delete(0, END)
        self.risercmnt.delete(0, END)
        return

    def sendreport(self):    #Currently, this can only be called once per 
        import report        #instance of the tkinter window, need to find
                             #how to unimport, so the function is re-called

    def submit(self):
        if self.worker.get()==self.workerempty:
            return
        if self.rack.get()==self.workerempty:
            return
        
        racknum=list(self.rack.get())
        for i in range(len(racknum)):
            print(racknum[i])
            if ord(racknum[i])==92:
                racknum[i]='backslash'
            if racknum[i]==',':
                racknum[i]=';'
            if racknum[i]=='"':
                racknum[i]='dblequote'
            if racknum[i]=="'":
                racknum[i]='snglquote'
        racknum="'"+"".join(racknum)+"'"
                
        roomnum=list(self.room.get())
        for i in range(len(roomnum)):
            if ord(roomnum[i])==92:
                roomnum[i]='backslash'
            if roomnum[i]==',':
                roomnum[i]=';'
            if roomnum[i]=='"':
                roomnum[i]='dblequote'
            if roomnum[i]=="'":
                roomnum[i]='snglquote'
        roomnum="'"+"".join(roomnum)+"'"
        

        #MySQL doesnt allow empty inputs in the fields, so need to set empty
        #entry boxes as null

        lts=self.lts.get()
        plts=self.plts.get()
        wtrflw=self.wtrflw.get()
        res50=self.res50.get()
        pmps=self.pmps.get()
        ipm=self.ipm.get()
        air=self.air.get()
        drpleak=self.drpleak.get()
        risers=self.riser.get()
        
        if self.rack.get()==self.emptycmnt:
            racknum='NULL'
        if self.room.get()==self.emptycmnt:
            roomnum='NULL'
        if self.lts.get()==self.emptynumb:
            lts='NULL'
        if self.plts.get()==self.emptynumb:
            plts='NULL'
        if self.wtrflw.get() == self.emptynumb:
            wtrflw='NULL'
        if self.res50.get()==self.emptynumb:
            res50='NULL'
        if self.pmps.get()==self.emptynumb:
            pmps='NULL'
        if self.ipm.get()==self.emptynumb:
            ipm='NULL'
        if self.air.get()==self.emptynumb:
            air='NULL'
        if self.drpleak.get()==self.emptynumb:
            drpleak='NULL'
        if self.riser.get()==self.emptynumb:
            risers='NULL'
        print(drpleak)
        print (self.air.get())
        
        
        
        holdingstring = roomnum + ',' + racknum\
                        + "," + lts + "," + plts\
                        +","+wtrflw+","+res50+","+\
                        pmps+","+ipm+","+air \
                        + "," + drpleak + "," + risers #Concats all the basic data

        ltscmnt=list(self.ltscmnt.get())
        for i in range(len(ltscmnt)):
            if ord(ltscmnt[i])==92:
                ltscmnt[i]='backslash'
            if ltscmnt[i]==',':
                ltscmnt[i]=';'
            if ltscmnt[i]=='"':
                ltscmnt[i]='dblequote'
            if ltscmnt[i]=="'":
                ltscmnt[i]='snglquote'
        ltscmnt="'"+"".join(ltscmnt)+"'"
        
        pltscmnt=list(self.pltscmnt.get())
        for i in range(len(pltscmnt)):
            if ord(pltscmnt[i])==92:
                pltscmnt[i]='backslash'
            if pltscmnt[i]==',':
                pltscmnt[i]=';'
            if pltscmnt[i]=='"':
                pltscmnt[i]='dblequote'
            if pltscmnt[i]=="'":
                pltscmnt[i]='snglquote'
        pltscmnt="'"+"".join(pltscmnt)+"'"

        wtrflwcmnt=list(self.wtrflwcmnt.get())
        for i in range(len(wtrflwcmnt)):
            if ord(wtrflwcmnt[i])==92:
                wtrflwcmnt[i]='backslash'
            if wtrflwcmnt[i]==',':
                wtrflwcmnt[i]=';'
            if wtrflwcmnt[i]=='"':
                wtrflwcmnt[i]='dblequote'
            if wtrflwcmnt[i]=="'":
                wtrflwcmnt[i]='snglquote'
        wtrflwcmnt="'"+"".join(wtrflwcmnt)+"'"

        res50cmnt=list(self.res50cmnt.get())
        for i in range(len(res50cmnt)):
            if ord(res50cmnt[i])==92:
                res50cmnt[i]='backslash'
            if res50cmnt[i]==',':
                res50cmnt[i]=';'
            if res50cmnt[i]=='"':
                res50cmnt[i]='dblequote'
            if res50cmnt[i]=="'":
                res50cmnt[i]='snglquote'
        res50cmnt="'"+"".join(res50cmnt)+"'"

        pmpscmnt=list(self.pmpscmnt.get())
        for i in range(len(pmpscmnt)):
            if ord(pmpscmnt[i])==92:
                pmpscmnt[i]='backslash'
            if pmpscmnt[i]==',':
                pmpscmnt[i]=';'
            if pmpscmnt[i]=='"':
                pmpscmnt[i]='dblequote'
            if pmpscmnt[i]=="'":
                pmpscmnt[i]='snglquote'
        pmpscmnt="'"+"".join(pmpscmnt)+"'"

        ipmcmnt=list(self.ipmcmnt.get())
        for i in range(len(ipmcmnt)):
            if ord(ipmcmnt[i])==92:
                ipmcmnt[i]='backslash'
            if ipmcmnt[i]==',':
                ipmcmnt[i]=';'
            if ipmcmnt[i]=='"':
                ipmcmnt[i]='dblequote'
            if ipmcmnt[i]=="'":
                ipmcmnt[i]='snglquote'
        ipmcmnt="'"+"".join(ipmcmnt)+"'"

        aircmnt=list(self.aircmnt.get())
        for i in range(len(aircmnt)):
            if ord(aircmnt[i])==92:
                aircmnt[i]='backslash'
            if aircmnt[i]==',':
                aircmnt[i]=';'
            if aircmnt[i]=='"':
                aircmnt[i]='dblequote'
            if aircmnt[i]=="'":
                aircmnt[i]='snglquote'
        aircmnt="'"+"".join(aircmnt)+"'"

        drpleakcmnt=list(self.drpleakcmnt.get())
        for i in range(len(drpleakcmnt)):
            if ord(drpleakcmnt[i])==92:
                drpleakcmnt[i]='backslash'
            if drpleakcmnt[i]==',':
                drpleakcmnt[i]=';'
            if drpleakcmnt[i]=='"':
                drpleakcmnt[i]='dblequote'
            if drpleakcmnt[i]=="'":
                drpleakcmnt[i]='snglquote'
        drpleakcmnt="'"+"".join(drpleakcmnt)+"'"

        risercmnt=list(self.risercmnt.get())
        for i in range(len(risercmnt)):
            if ord(risercmnt[i])==92:
                risercmnt[i]='backslash'
            if risercmnt[i]==',':
                risercmnt[i]=';'
            if risercmnt[i]=='"':
                risercmnt[i]='dblequote'
            if risercmnt[i]=="'":
                risercmnt[i]='snglquote'
        risercmnt="'"+"".join(risercmnt)+"'"

        if self.ltscmnt.get()==self.emptycmnt:
            ltscmnt='NULL'
        if self.pltscmnt.get()==self.emptycmnt:
            pltscmnt='NULL'
        if self.wtrflwcmnt.get()==self.emptycmnt:
            wtrflwcmnt='NULL'
        if self.res50cmnt.get()==self.emptycmnt:
            res50cmnt='NULL'
        if self.pmpscmnt.get()==self.emptycmnt:
            pmpscmnt='NULL'
        if self.ipmcmnt.get()==self.emptycmnt:
            ipmcmnt='NULL'
        if self.aircmnt.get()==self.emptycmnt:
            aircmnt='NULL'
        if self.drpleakcmnt.get()==self.emptycmnt:
            drpleakcmnt='NULL'
        if self.risercmnt.get()==self.emptycmnt:
            risercmnt='NULL'

        holdingstring=holdingstring +","+ltscmnt+","+pltscmnt+","+\
                       wtrflwcmnt+","+res50cmnt+","+pmpscmnt+","+\
                       ipmcmnt+","+aircmnt+","+\
                       drpleakcmnt+","+risercmnt

        worker=list(self.worker.get())  #Change worker entry input into list so its mutable
        for i in range(len(worker)):   #check for commas, change to semicolons
            if ord(worker[i])==92:
                worker[i]='backslash'
            if worker[i]==',':
                worker[i]=';'
            if worker[i]=='"':
                worker[i]='dblquote'
            if worker[i] == "'":
                worker[i]= 'snglquote'
            
        worker="".join(worker)

        holdingstring=holdingstring + ",'" + worker + "',"#concatenate worker at end, and add new line character
        
        timestamp=datetime.datetime.now().strftime("'%A','%Y-%m-%d %H:%M:%S'") #keeps DoW, date, H:M:S from date obj
        
        holdingstring+= timestamp#concats all data with timestamp
        mysqlholdingstring=holdingstring
        holdingstring+="\n"
        print (holdingstring)
        filename="DailyWalkthrough_db.csv"
        output=open(filename, 'a+')
        output.write(holdingstring)
        output.close()
        holdinglist=holdingstring.split(',')
        print (len(holdinglist))
        mysqlholdingstring='('+mysqlholdingstring+')'
        mysqlholdingstring = "".join(mysqlholdingstring)
        print (mysqlholdingstring)
        #SQL input string to be run
        self.cursor.execute("""INSERT INTO growroomwalkthrough (Room,Rack,Lights,\
Plants,WaterFlow,Reservoir50,Pumps,IPM,Airators,NoDripsLeaks,Risers,Lights_commen\
ts,Plants_comments,WaterFlow_comments,Reservoir50_comments,Pumps_comments,IPM_co\
mments,Airators_comments,NoDripsLeaks_comments,Risers_comments,Initials,Day,Date)\
VALUES """ + mysqlholdingstring)
                            #(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
#%s, %s, %s, %s, %s, %s, %s, %s, %s)""" % (mysqlholdingstring[i] for \
 #                                    i in range(len(mysqlholdingstring))))
        self.db.commit()
        #except MySQLdb.MySQLError:
        #    self.db.rollback()
        #    print ("error somewhere")
        #except
        
        self.clearcells()
        
        
root=Tk()

my_gui=Data_entry(root)

root.mainloop()
