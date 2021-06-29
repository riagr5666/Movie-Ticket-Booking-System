from tkinter import * # This line is used to import the GUI interface
import pyqrcode
import png
from pyqrcode import QRCode
from tkinter.messagebox import * # This line of code is used for message box to appear
from twilio.rest import Client
import sqlite3 # Building and Importing the database
root=Tk() # Importing the Tkinter into root
root.configure(bg='#424242') # Configuring the background colour
root.title('MOVIE TICKET RESERVATION SYSTEM') # Showing the title for the GUI 
root.geometry('1000x1000') # The size of the window Showbook
con = None #Connections is initializes with None, in this we to have store integer because we can modify in python into any variable from integer to string at any give point
cur = None #Cursor is initialized with None
MAX_TICKETS = 200 # This shows the number of tickets available for each movie
DATABASE_NAME = "MovieDatabase1.db" # This is the database created

class LoginScreen: # The Login screen
    
    def __init__(self, master): # In this master == root ==Tk initialization block, master is an object instance of Tk
        self.createDbAndTables() # here we are creating a function for database table
        self.createView(master) # here we are passing master in createView because we have using it as arguments into the Tk
                
    def createDbAndTables(self): # default syntax that we have to pass the parameter self as the instance of the class       
        global con # globalizing the con 
        global cur # globalizing the cur
        con=sqlite3.connect(DATABASE_NAME) # Connecting the database with sqlite3
        cur=con.cursor() # Inbuilting the database with cursor
        cur.execute("create table if not exists accounts(id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(20), password varchar(10), name varchar(20), mob_no number(12))") # creating the Table for accounts                         
        cur.execute("create table if not exists bticket(id INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(20), movie varchar(10), date date, num_ticket number(10))") # creating table for booking tickets
        
    def createView(self, master):
        Label(master,text='MOVIE TICKET RESERVATION SYSTEM',font="Arial 30 bold italic",bd=5,bg="blue",relief='ridge').pack()
                
        Label(master,text='Enter Username').pack() # label for entering userbame
        self.username=Entry(master) # Entering the username
        self.username.pack() 
        
        Label(master,text='Enter Password').pack()
        self.pwd=Entry(master,show='*') # entering the password
        self.pwd.pack() 
                
        Label(root,text='                 ',bg='#424242').pack()#Gap between 2 views
        Button(root,text='Login',bd=5,command=self.onClickLogin,bg='light blue').pack() # calling onclicklogin using button

        
    def onClickLogin(self):
        cur.execute(('SELECT * FROM accounts WHERE username = ? and password = ?'),[(self.username.get()),(self.pwd.get())]) # Selecting the username and password 
        loginRecords = cur.fetchall() # loading all the list of table records 
        print(loginRecords)
        if(loginRecords): # if list is not null or empty
            homeScreen.createView(self.username.get()) # This will shift to homescreen
        else:
            showerror('Error','Invalid username or password')  
        
loginScreen = LoginScreen(root)
class SignUpScreen:    
    def __init__(self, master):
        self.master = master
        
    def createView(self): # This function is used to create a account in the database
        print('create_cl#create() started')
        self.wSignUp = Toplevel(root) # this opens a new window
        self.wSignUp.configure(bg='light blue')
        self.wSignUp.geometry('300x300')
        
        Label(self.wSignUp,text='Enter your name').pack()
        self.name=Entry(self.wSignUp) # Loads the name
        self.name.pack()
        
        Label(self.wSignUp,text='Enter Username').pack()
        self.username=Entry(self.wSignUp) # loads the username
        self.username.pack() 
        
        Label(self.wSignUp,text='Enter Password').pack()
        self.pwd=Entry(self.wSignUp,show='*') # loads the password
        self.pwd.pack()
        
        Label(self.wSignUp,text='Enter yor mobile number(10 digits)').pack()
        self.mNumber=Entry(self.wSignUp) # Loads the password
        self.mNumber.pack()
        
        Button(self.wSignUp,text='create account',command = self.onClickSignUp).pack() # created account and goes the command of onclicksignup
        
    def onClickSignUp(self): # This used to check errors in the account created
        hasValidFields=True
        if self.username.get()=='' or self.pwd.get()=='' or self.mNumber.get()=='' or self.name.get()=='' :
            showerror('missing input','please fill every detail')
        
        # below code is to check unique in the username
        cur.execute(('SELECT * FROM accounts WHERE username = ? '),[(self.username.get())])
        userNameRecords = cur.fetchall() # table records return type is list
        if(userNameRecords): # check whether username is not null or not empty or whether username already exits in the table or not
            showerror('UserNameError',"User name already exists please try with other username")
            return # this will return again back for creating a new username
        
        num=len(self.mNumber.get()) # This loads the length of the mobile number
        if num!=10: # checkts whether the mobile number has the lenght of 10 or not
            hasValidFields=False
            showerror('error','mobile number is invalid')            
            
        else:
            try:
                val=int(self.mNumber.get()) # This loads the value of the monbile number
                cur.execute("insert into accounts values (?,?,?,?,?)",(None, self.username.get(),self.pwd.get(),val,self.name.get())) # This inserts all the values 
                con.commit()

            except ValueError: # This is used to check mobile number
                hasValidFields=False
                showerror('error','mobile number is invalid')                
                
            except sqlite3.IntegrityError: # any other errors
                hasValidFields=False 
                showerror('error','invalid input by the user')                
                
            except Exception as e:
                hasValidFields=False
                logger.error(str(e), exc_info=True)
                showerror('username not unique','username already exisits')                
                
            if(hasValidFields): # If there are no errors the account gets created
                showinfo('Welcome','Account is created')
                self.wSignUp.destroy()
                
                
signUpScreen = SignUpScreen(root)
class HomeScreen:
    def __init__(self, master):
        self.master = master
    
    def createView(self, username):
        self.username = username # This is used to check which user has looged in we have self.username
        wHome = Toplevel(self.master) # This is used to build Ticket booking window
        wHome.configure(bg='light blue')
        wHome.geometry('300x300')
        
        # on clicking the button below line it will invoke this onclickbookticket
        Button(wHome,text='Book Tickets',command=self.onClickBookTicket).pack() # in this we are passing the reference of the method 'onClickBookTicket' function name
        Button(wHome,text='Check Booking History',command=self.onClickBookingHistory).pack()
  
    def onClickBookTicket(self): bookTicketScreen.createView(self.username) # loading the bookTicketscreen function
    def onClickBookingHistory(self): historyScreen.createView(self.username) # loading the historyscreen function
        
homeScreen = HomeScreen(root)
class BookTicketScreen:
    def __init__(self, master):
        self.master = master
        
    def createView(self, username): # This class is used to select movie
        self.username = username
        self.wBookTicket = Toplevel(self.master) #Ticket booking window
        self.wBookTicket.configure(bg='light blue')
        self.wBookTicket.geometry('300x300')
        
        Label(self.wBookTicket,text='Select Movie:',bg='light blue').pack()
        self.rbId = IntVar() # datatype of rbId is integer
        
        # The below we use radioButton for selecting the movie
        self.r=Radiobutton(self.wBookTicket,text='Robot 2.0',variable=self.rbId,value=1,bg='light blue')
        self.r.pack()
        
        self.r=Radiobutton(self.wBookTicket,text='Avengers End Game',variable=self.rbId,value=2,bg='light blue')
        self.r.pack()
        
        self.r=Radiobutton(self.wBookTicket,text='Godzilla vs. Kong',variable=self.rbId,value=3,bg='light blue')
        self.r.pack()
        
        self.r=Radiobutton(self.wBookTicket,text='Tom And Jerry',variable=self.rbId,value=4,bg='light blue')
        self.r.pack()
        
        self.r=Radiobutton(self.wBookTicket,text='Rumble',variable=self.rbId,value=5,bg='light blue')
        self.r.pack()
        
        Label(self.wBookTicket,text='enter the date(yyyy-mm-dd)',bg='light blue').pack()# This line used to select the date
        self.bookingDate=Entry(self.wBookTicket)
        self.bookingDate.pack()
        
        Label(self.wBookTicket,text='enter number of tickets to book',bg='light blue').pack() # this line is used to book the tickets
        self.numberOfTickets=Entry(self.wBookTicket)
        self.numberOfTickets.pack()
        
        Button(self.wBookTicket, text='Check availability tickets', command=self.onClickCheckAvailability).pack() # This function calls the ticket avaialbility
        Button(self.wBookTicket, text='Confirm Tickets', command=self.onClickConfirmTickets).pack() # this button used to confirm the tickets

    
    def hasValidFields(self): # This funciton is used to check the valid fields
        if(self.bookingDate.get().strip()==""): return False # Strip() method is defined by string class and has a return type of string; here self.e.get() returns string
        if(self.numberOfTickets.get().strip()==""): return False    
        else: return True
    
    # The below fucntion stores the value for the selected movie
    def getMovieName(self):
        print(self.rbId.get()) 
        if(self.rbId.get()==1):
            return 'robot 2.0'
        if(self.rbId.get()==2):
            return 'Avengers End Game'
        if(self.rbId.get()==3):
            return 'Godzilla vs. Kong'
        if(self.rbId.get()==4):
            return 'Tom And Jerry'
        if(self.rbId.get()==5):
            return 'Rumble'
        else:
            return None
    
    # The below function is used to check number of avaialable tickets
    def getNumberOfAvailableTickets(self):
        movieName = self.getMovieName()
        cur.execute("select sum(num_ticket) from bticket where movie = ? and date = ?",[(movieName),self.bookingDate.get()])
        self.availabeTickets=cur.fetchone()
        print(self.availabeTickets[0])
        if(self.availabeTickets[0]==None):
            return MAX_TICKETS
        else:
            return (MAX_TICKETS-self.availabeTickets[0])
        
        
     # This funciton works for checking the avaliable tickets if all the fields are filled properly   
    def onClickCheckAvailability(self):        
        if(self.hasValidFields() == False):
            showinfo('Invalid Fields','Please enter all field properly')
            #return
        else:
    
            tickets = self.getNumberOfAvailableTickets()
            Label(self.wBookTicket,text='available seats :-'+ str(tickets), bg='light blue').pack()
        
     
    # The below function is used to check whether the tickets booked are out of the avialable range in a movie
    def onClickConfirmTickets(self):
        if(self.hasValidFields() == False):
            showinfo('Invalid Fields','Please enter all field properly')
            return
        
        tickets = self.getNumberOfAvailableTickets()
        #mNumber = self.getmNumber()
        noOfTicketRequired = int(self.numberOfTickets.get())
    
        if((tickets-noOfTicketRequired) < 0):
            showinfo('Attention','Insufficient ticket are available, please check change no. of tickets, date or movie name.')        
            return
        
        movieName = self.getMovieName() # we have calling this 2 different methods because one for checking the no. of tickets and another one is for inserting the name inside  
        
        cur.execute("insert into bticket values (?,?,?,?,?)",(None, self.username, movieName, self.bookingDate.get(), self.numberOfTickets.get()))
        con.commit()
        showinfo('Well done','Your tickets are booked successfully, enjoy your show')
        # Your Account SID from twilio.com/console
        account_sid = "AC1c4fe13a08a8447514eba7c2a4f072da"
    # Your Auth Token from twilio.com/console
        auth_token  = "33e57733f0def596e25c56b34f5d74cc"

        client = Client(account_sid, auth_token)
        #movieName=StringVar()
       # noOfTicketRequired=StringVar()
       
        #list_sms = [text , movieName , self.bookingDate.get() ,noOfTicketRequired]
        text= (" Well done Your tickets are booked successfully, enjoy your show of ")
        list_sms = [text , movieName ,"on" , self.bookingDate.get() , "Total Tickets booked are" , noOfTicketRequired , "\nTHANKYOU FOR VISIT" ]
        text1=' '.join(map(str, list_sms))
        message = client.messages.create(
             to= "+919582365704" , 
             from_="+19542783536",
            body= text1)
        s = text1
  
        # Generate QR code
        url = pyqrcode.create(s)
          
        # Create and save the svg file naming "myqr.svg"
        url.svg("MyTicketInQR.svg", scale = 8)
          
        # Create and save the png file naming "myqr.png"
        url.png('MyTicketInQR.png', scale = 6)
        

        self.wBookTicket.destroy()
       
bookTicketScreen = BookTicketScreen(root)
class HistoryScreen:
    def __init__(self, master):
        self.master = master
    
        
    def createView(self, username): # This funciton is used to check the history of tickets booked
        self.username = username # here it is creating an instance variable for username
        wHistory = Toplevel(self.master) # creating the window for wHistory
        self.wHistory = wHistory
        wHistory.configure(bg='light blue')
        wHistory.geometry('450x500')
        
      
        cur.execute(('SELECT * FROM bticket WHERE username = ?'),[(self.username)])
        
        # The below code is used to execute the history in a table format
        g=cur.fetchall()
        if(g==[]):
            showerror('bookings','no bookings yet!!')
            wHistory.destroy()
            return
        
        Label(wHistory, text='   id',bg='light blue').grid(row=0,column=0)
        Label(wHistory, text='   username',bg='light blue').grid(row=0,column=1)
        Label(wHistory, text='   movie name',bg='light blue').grid(row=0,column=2)
        Label(wHistory, text='   date of the show',bg='light blue').grid(row=0,column=3)
        Label(wHistory, text='   number of tickets',bg='light blue').grid(row=0,column=4)

        j=0
        for i in g:
            Label(wHistory,text=g[j][0],bg='light blue').grid(row=j+1,column=0)
            Label(wHistory,text=g[j][1],bg='light blue').grid(row=j+1,column=1)
            Label(wHistory,text=g[j][2],bg='light blue').grid(row=j+1,column=2)
            Label(wHistory,text=g[j][3],bg='light blue').grid(row=j+1,column=3)
            Label(wHistory,text=g[j][4],bg='light blue').grid(row=j+1,column=4)
            j=j+1
            
        j = j+1
        Label(wHistory,text='   ',bg='light blue').grid(row=j,columnspan=5)

        j = j+1
        Label(wHistory,text='Enter the Id to cancel the Ticket',bg='light blue').grid(row=j,columnspan=5, sticky=W+E)
        self.cancelTicket = Entry(wHistory)

        j = j+1
        self.cancelTicket.grid(row=j,columnspan=5, sticky=W+E)

        j = j+1
        Button(self.wHistory,text='Confirm cancellation',command = self.onClickCancel).grid(row=j,columnspan=5, sticky=W+E)

        
    
    # The below funciton is used for canceling the tickets
    def onClickCancel(self): 
        if(self.cancelTicket.get().strip()==""):
            showinfo('Attention','Please enter valid Id')
            return
        else:
            cur.execute("delete FROM bticket WHERE id = ?",[(self.cancelTicket.get())])
            con.commit()
            showinfo('cancelled','your ticket has been cancelled')
            self.wHistory.destroy()
            self.createView(self.username)

        
        
        
historyScreen = HistoryScreen(root)
Label(root,text='                 ',bg='#424242').pack()
Button(root,text='create account',bd=5,bg='light blue',command=signUpScreen.createView).pack() # This creates the button for signupscreen
root.mainloop() # This is used to execute the GUI until it is closed by the user
