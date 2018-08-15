from tkinter import *
import datetime
import MySQLdb
import imp

class Data_entry:

    def __init__(self, master):
        self.master = master
        master.title("Grow Room water readings")



        #Labels
        self.emptylabel = Label(master, text="")
        self.secondempty = Label(master, text="")
        self.errorlab = Label(master, text="ERROR: All inputs must be numbers"\
                              , fg="red")
        self.workerlab = Label(master, text="Initials of data collector")
        self.roomlab = Label(master, text="Room number: ")
        self.racklab = Label(master, text="Rack number: ")
        self.pHlab = Label(master, text="pH(should be between 5.4 and 6.2): ")
        self.ppmlab = Label(master, text="PPM(should be between 800 and 1000): ")
        self.DOlab = Label(master, text="Dissolved Oxygen(should be close to 8): "\
                           )
        self.templab = Label(master, text="Temperature(should be close to 72): ")

        #Entry boxes
        vcmd = master.register(self.validate) # validate command for int inputs
        commentvcmd = master.register(self.commentvalidate) #validate command for str inputs(worker, rack, room, comments)
        floatvcmd = master.register(self.validatefloat) #validate floats(allows ".")

        self.worker = Entry(master, validate="key", validatecommand=(commentvcmd\
                                                                     , '%P'))
        self.room = Entry(master, validate="key", validatecommand=(commentvcmd,\
                                                                   '%P'))
        self.rack = Entry(master, validate="key", validatecommand=(commentvcmd,\
                                                                   '%P'))
        self.pH = Entry(master, validate="key", validatecommand=(floatvcmd,\
                                                                 '%P'))
        self.ppm = Entry(master, validate="key", validatecommand = (vcmd,\
                                                                    '%P'))
        self.DO = Entry(master, validate="key", validatecommand = (floatvcmd,\
                                                                   '%P'))
        self.temp = Entry(master, validate="key", validatecommand = (floatvcmd,\
                                                                     '%P'))



        #Submit button
        self.submit_button = Button(master, text="Submit", command=lambda:\
                                    self.submit())

        self.report_button = Button(master, text="Send email report", command=\
                                    lambda: self.sendreport())
        #self.report_button = Button(master, text="Send Email Report",\
                                   # command=lambda: self.sendreport())

        # LAYOUT
        self.workerlab.grid(row=0, column=0, columnspan=2, sticky=W+E)

        self.worker.grid(row=1, column=0, columnspan=1, sticky=W+E)
        #self.emptylabel.grid(row=1, column=3)

        self.roomlab.grid(row=3, column=0)
        self.room.grid(row=3, column=3, columnspan=1, sticky=W+E)

        self.racklab.grid(row=6, column=0)
        self.rack.grid(row=6, column=3, columnspan=1, sticky=W+E)

        self.pHlab.grid(row=9, column=0)
        self.pH.grid(row=9, column=3, columnspan=1, sticky=W+E)

        self.ppmlab.grid(row=12, column=0)
        self.ppm.grid(row=12, column=3, columnspan=1, sticky=W+E)

        self.DOlab.grid(row=18, column=0)
        self.DO.grid(row=18, column=3, columnspan=1, sticky=W+E)

        self.templab.grid(row=15, column=0)
        self.temp.grid(row=15, column=3, columnspan=1, sticky=W+E)

        self.submit_button.grid(row=21, column=3, sticky=W+E)
        self.report_button.grid(row=25, column=0, sticky=W+E)

        #self.reportlab.grid(row=28, column=0, columnspan=2, sticky=W+E)
        #self.report_button.grid(row=29, column=0, columnspan=2, sticky=W+E)

        master.grid_columnconfigure(0, minsize=200, weight=1)
        master.grid_columnconfigure(3, minsize=30, weight=1)

        self.errorclear()
        self.workerempty=self.worker.get()
        self.db = MySQLdb.connect("databaseserver", "root", "password", "datacollection")

        self.cursor = self.db.cursor()

        #Empty checkers
        self.emptynum = self.pH.get()
        self.emptycmnt = self.room.get()
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

    def validatefloat(self, new_text):
        if not new_text:
            return True
        for i in range(len(new_text)):
            if (new_text[i] in '1234567890.') and (new_text[i] not in ' '):
                try:
                    float(new_text)
                    print ("working")
                    return True
                except ValueError:
                    print ("can't float")
                    return False
            else:
                print ("not in string")
                return False

    def clearcells(self):
        #self.worker.delete(0, END) #commenting this out because the initials should stay same
                                    #almost every time, can still be manually deleted
        #self.room.delete(0, END)
        self.rack.delete(0, END)
        self.temp.delete(0, END)
        self.ppm.delete(0, END)
        self.pH.delete(0, END)
        self.DO.delete(0, END)
        self.temp.delete(0, END)
        return

    def sendreport(self):    #Currently, this can only be called once per
        try:
            imp.reload(phemail)
        except:
            import phemail
            #instance of the tkinter window, need to find
                             #how to unimport, so the function is re-called

    def submit(self):
        if self.worker.get()==self.workerempty:
            return
        if self.rack.get()==self.workerempty:
            return
        if self.room.get()==self.workerempty:
            return

        racknum=list(self.rack.get())
        for i in range(len(racknum)):
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
        print (self.pH.get())
        ppm=self.ppm.get().replace(' ','')
        pH=self.pH.get().replace(' ','')
        DO=self.DO.get().replace(' ','')
        temp=self.temp.get().replace(' ','')
        print (pH)

        if self.pH.get()==self.emptynum:
            pH='NULL'
        if self.ppm.get()==self.emptynum:
            ppm='NULL'
        if self.DO.get()==self.emptynum:
            DO='NULL'
        if self.temp.get()==self.emptynum:
            temp='NULL'



        holdingstring = roomnum + ',' + racknum\
                        + ','+ pH + ',' + ppm + ',' + DO + ',' + temp

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

        holdingstring += ",'" + worker + "',"#concatenate worker at end, and add new line character

        timestamp=datetime.datetime.now().strftime("'%A','%Y-%m-%d %H:%M:%S'") #keeps DoW, date, H:M:S from date obj

        holdingstring+= timestamp#concats all data with timestamp
        mysqlholdingstring=holdingstring
        holdingstring+="\n"
        filename="WaterData.csv"
        output=open(filename, 'a+')
        output.write(holdingstring)
        output.close()
        holdinglist=holdingstring.split(',')
        print (len(holdinglist))
        mysqlholdingstring='('+mysqlholdingstring+')'
        #mysqlholdingstring = "".join(mysqlholdingstring)
        print (mysqlholdingstring)


        #SQL input string to be run
        self.cursor.execute("""INSERT INTO waterreadings (Room,Rack,\
pH, PPM, DO, Temp, Initials, Day, Date) VALUES """ + mysqlholdingstring)

        self.db.commit()


        self.clearcells()


root=Tk()

my_gui=Data_entry(root)

root.mainloop()
