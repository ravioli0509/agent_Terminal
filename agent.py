import time, sqlite3, datetime, re, getpass

def register_birth(user,conn):
    # The agent should be able to register a birth by providing the first name, the last name, the gender, the birth date, 
    # the birth place of the newborn, as well as the first and last names of the parents.
    # The registration date is set to the day of registration (today's date) and the registration place is set to the city of the user. 
    # The system should automatically assign a unique registration number to the birth record. 
    # The address and the phone of the newborn are set to those of the mother. 
    # If any of the parents is not in the database, the system should get information about the parent including first name, last name, 
    # birth date, birth place, address and phone. For each parent, any column other than the first name and last name can be null if it is not provided.
    c = conn.cursor()
    # Get inputs from user
    while True:
        fname = input("First name: ")
        # cancel command aborts operation and returns to main menu
        if fname.lower() == "cancel":
            return
        # Checks to see if input is not only whitespace or no input
        elif not fname.isspace() and fname != '':
            break
        # Loops until valid input is obtained
        print("Please enter a first name.")
    while True:
        lname = input("Last name: ")
        if lname.lower() == "cancel":
            return
        elif not lname.isspace() and lname !='':
            break
        print("Please enter a last name")
    # Check to see if person already exists in database
    c.execute('''SELECT * FROM persons WHERE fname=:fname COLLATE NOCASE AND lname=:lname COLLATE NOCASE''',{'fname':fname,'lname':lname})
    if c.fetchone() != None:
        print("Person already exists, can not register birth for this person")
        return
    while True:
        gender = input("Gender (M/F): ")
        if gender.lower() == "cancel":
            return
        elif gender.lower() =="f" or gender.lower() == "m":
            break
        print("Invalid Gender")
    # Checks to see if date is valid
    validdate = False
    while validdate == False:
        bdate = input("Birth date (YYYY-MM-DD): ")
        if bdate.lower() == "cancel":
            return
        else:
            validdate = True
            try:
                # Splits input into year month and day
                year,month,day = bdate.split("-")
                # Checks to see values are valid (ie. month isn't greater than 12 or day isn't greater than 31)
                datetime.datetime(int(year),int(month),int(day))
            except ValueError:
                # If input is not valid, cycle through loop until input is valid
                validdate = False
                print("Invalid date")
    while True:  
        blocation = input("Birth Location: ")
        if blocation.lower() == "cancel":
            return
        elif not blocation.isspace() and blocation !='':
            break
        print("Please enter the location where the person was born")
    while True:
        f_fname = input("Father's first name: ")
        if f_fname.lower() == "cancel":
            return
        elif not f_fname.isspace() and f_fname !='':
            break
        print("Please enter the father's first name")
    while True:
        f_lname = input("Father's last name: ")
        if f_lname.lower() == "cancel":
            return
        elif not f_lname.isspace() and f_lname!='':
            break
        print("Please enter the father's last name")
    while True:
        m_fname = input("Mother's first name: ")
        if m_fname.lower() == "cancel":
            return
        elif not m_fname.isspace() and m_fname!='':
            break
        print("Please enter the mother's first name")
    while True:
        m_lname = input("Mother's last name: ")
        if m_lname.lower() == "cancel":
            return
        elif not m_lname.isspace() and m_lname!='':
            break
        print("Please enter the mother's last name")
    # Check to see if father input is in database
    c.execute('''SELECT * FROM persons WHERE (fname = :f_fname COLLATE NOCASE AND lname = :f_lname COLLATE NOCASE) ''',{'f_fname':f_fname,'f_lname':f_lname})
    father = c.fetchone()
    # Get details of father if not in database
    if father == None:
        print("Father has no entry in database, Please input details")
        if addPerson(conn, f_fname,f_lname) == None:
            return
        # Get father's details
        c.execute('''SELECT * FROM persons WHERE (fname = :f_fname COLLATE NOCASE AND lname = :f_lname COLLATE NOCASE)''',{'f_fname':f_fname,'f_lname':f_lname})
        father = c.fetchone()
    # Check to see if mother input is in database
    c.execute('''SELECT * FROM persons WHERE (fname = :m_fname COLLATE NOCASE AND lname = :m_lname COLLATE NOCASE)''',{'m_fname':m_fname,'m_lname':m_lname})
    mother = c.fetchone()
    # Get details of mother if not in database
    if mother == None:
        print("Mother has no entry in database, Please input details")
        if addPerson(conn,m_fname,m_lname) == None:
            return
        # Get mother's details
        c.execute('''SELECT * FROM persons WHERE (fname = :m_fname COLLATE NOCASE AND lname = :m_lname COLLATE NOCASE)''',{'m_fname':m_fname,'m_lname':m_lname})
        mother = c.fetchone()
    # Assign unique registration number
    c.execute('''SELECT MAX(regno) FROM births''')
    regno = c.fetchone()
    if regno[0] == None:
        regno = 1
    else:
        regno = int(regno[0])+1
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # Create new person
    c.execute('''INSERT INTO persons VALUES (:fname,:lname,:bdate,:blocation,:address,:phone)''',{'fname':fname,'lname':lname,'bdate':bdate,'blocation':blocation,'address':mother[4],'phone':mother[5]})
    conn.commit()
    # Create new birth registration
    c.execute('''INSERT INTO births VALUES (:regno,:fname,:lname,:regdate,:regplace,:gender,:f_fname,:f_lname,:m_fname,:m_lname)''',{'regno':regno,'fname':fname,'lname':lname,'regdate':date,'regplace':user[5],'gender':gender,'f_fname':f_fname,'f_lname':f_lname,'m_fname':m_fname,'m_lname':m_lname})
    conn.commit()
    input("Birth registration successfully added (Press Enter to Proceed)")

def register_marriage(user,conn):
    # The user should be able to provide the names of the partners and the system should assign the registration date and place and a unique registration number as discussed in registering a birth. 
    # If any of the partners is not found in the database, the system should get information about the partner including first name, last name, birth date, birth place, address and phone. 
    # For each partner, any column other than the first name and last name can be null if it is not provided.
    c = conn.cursor()
    # Get both partners' first and last names
    while True:
        p1_fname = input("Enter partner 1's first name: ")
        if p1_fname.lower() == "cancel":
            return
        elif not p1_fname.isspace() and p1_fname != '':
            break
        print("Please enter the first name of partner 1.")
    while True:
        p1_lname = input("Enter partner 1's last name: ")
        if p1_lname.lower() == "cancel":
            return 
        elif not p1_lname.isspace() and p1_lname!= '':
            break
        print("Please enter the last name of partner 1.")
    while True:
        p2_fname = input("Enter partner 2's first name: ")
        if p2_fname.lower() == "cancel":
            return
        elif not p2_fname.isspace() and p2_fname!= '':
            break
        print("Please enter the first name of partner 2.")
    while True:
        p2_lname = input("Enter partner 2's last name: ")
        if p2_lname.lower() == "cancel":
            return
        elif not p2_lname.isspace() and p2_lname!= '':
            break
        print("Please enter the last name of partner 2.")
    
    # Check to see if partner 1 is in database
    c.execute('''SELECT * FROM persons WHERE (fname = :p1_fname COLLATE NOCASE AND lname = :p1_lname COLLATE NOCASE) ''', {'p1_fname':p1_fname,'p1_lname':p1_lname})
    p1 = c.fetchone()
    # Get details of partner 1 if not in database
    if p1 == None:
        print("Partner 1 has no entry in database, please input details")
        if addPerson(conn,p1_fname,p1_lname) == None:
            return
        c.execute('''SELECT * FROM persons WHERE (fname = :p1_fname COLLATE NOCASE AND lname = :p1_lname COLLATE NOCASE) ''', {'p1_fname':p1_fname,'p1_lname':p1_lname})
        p1 = c.fetchone()
    # Check to see if partner 2 is in database
    c.execute('''SELECT * FROM persons WHERE (fname = :p2_fname COLLATE NOCASE AND lname = :p2_lname COLLATE NOCASE) ''', {'p2_fname':p2_fname,'p2_lname':p2_lname})
    p2 = c.fetchone()
    # get details of partner 2 if not in databse
    if p2 == None: 
        print("Partner 2 has no entry in database, please input details")
        if addPerson(conn,p2_fname,p2_lname) == None:
            return
        c.execute('''SELECT * FROM persons WHERE (fname = :p2_fname COLLATE NOCASE AND lname = :p2_lname COLLATE NOCASE) ''', {'p2_fname':p2_fname,'p2_lname':p2_lname})
        p2 = c.fetchone()
    # Create unique registration number
    c.execute('''SELECT MAX(regno) FROM marriages''')
    regno = c.fetchone()
    if regno[0] == None:
        regno = 1
    else: 
        regno = int(regno[0])+1
    regdate = datetime.datetime.now().strftime("%Y-%m-%d")
    # Insert marriage registration
    c.execute('''INSERT INTO marriages VALUES (:regno,:regdate,:regplace,:p1_fname,:p1_lname,:p2_fname,:p2_lname)''', {'regno':regno,'regdate':regdate,'regplace':user[5],'p1_fname':p1_fname,'p1_lname':p1_lname,'p2_fname':p2_fname,'p2_lname':p2_lname})
    conn.commit()
    input("Marriage Registration successfully added (Press Enter to Proceed)")

def renew_vehicle_registration(conn):
    # The user should be able to provide an existing registration number and renew the registration. 
    # The system should set the new expiry date to one year from today's date if the current registration either has expired or expires today. 
    # Otherwise, the system should set the new expiry to one year after the current expiry date.
    c = conn.cursor()
    while True:
        # Get registration number from user
        regno = input("Registration Number: ")
        # Check to see if regno is a number
        if regno.isdigit():
            c.execute('''SELECT * FROM registrations WHERE regno =:regno''',{'regno':regno})
            registry = c.fetchone()
            if not registry == None:
                exdate = registry[2]
                year,month,day = exdate.split("-")
                expdate = datetime.datetime(int(year),int(month),int(day))
                if expdate < datetime.datetime.now():
                    expdate = datetime.datetime.now()
                exdate = datetime.datetime(expdate.year+1,expdate.month,expdate.day).strftime("%Y-%m-%d")
                c.execute('''UPDATE registrations SET expiry=:expiry WHERE regno = :regno''',{'expiry':exdate,'regno':regno})
                conn.commit()
                input("Registration successfully updated (Press Enter to Proceed)")
                break
        elif regno.lower() == "cancel":
            break
        print("Invalid registration number")


def process_bill(conn):
    # The user should be able to record a bill of sale by providing the vin of a car, the name of the current owner, the name of the new owner, and a plate number for the new registration. 
    # If the name of the current owner (that is provided) does not match the name of the most recent owner of the car in the system, the transfer cannot be made.
    # When the transfer can be made, the expiry date of the current registration is set to today's date and a new registration under the new owner's name is recorded with the registration date and the expiry date set by the system to today's date and a year after today's date respectively. 
    # Also a unique registration number should be assigned by the system to the new registration. 
    # The vin will be copied from the current registration to the new one.
    c = conn.cursor()
    # Get Vechicle identification number
    while True:
        vin = input("Vechicle Identification Number (VIN): ")
        if vin.lower() == "cancel":
            return
        elif vin.isdigit():
            c.execute("SELECT * FROM registrations WHERE vin =:vin ORDER BY regdate",{'vin':vin})
            cur_reg = c.fetchone()
            if cur_reg == None:
                print("Invalid VIN")
            else:
                break
    # Get current owner's first name and last name
    while True:
        while True:
            cur_fname = input("Current owner's first name: ")
            if cur_fname.lower() == "cancel":
                return
            elif not cur_fname.isspace() and cur_fname != '':
                break
        while True:
            cur_lname = input("Current owner's last name: ")
            if cur_lname.lower() == "cancel":
                return
            elif not cur_lname.isspace() and cur_lname != '':
                break
        # Check to see if input is correct
        if cur_fname.lower() == cur_reg[5].lower() and cur_lname.lower() == cur_reg[6].lower():
            break
        print("Name entered does not correspond to current owner's name")
        print("Please enter current owner's name")
    # Get new owner's first name and last name
    while True:
        while True:
            new_fname = input("New owner's first name: ")
            if new_fname.lower() == "cancel":
                return
            elif not new_fname.isspace() and new_fname != '':
                break
            print("Please enter the new owner's first name")
        
        while True:
            new_lname = input("New owner's last name: ")
            if new_lname.lower() == "cancel":
                return
            elif not new_lname.isspace() and new_lname != '':
                break
            print("Please enter the new owner's last name")
        # Check to see if person exists in the database
        c.execute('''SELECT * FROM persons WHERE fname=:fname AND lname=:lname''',{'fname':new_fname,'lname':new_lname})
        if c.fetchone() == None:
            print("Person to transfer ownership to does not exist")
        else:
            break
    
    while True:
        lic_plate = input("New Licence Plate Number: ")
        if lic_plate.lower() == 'cancel':
            return
        elif not lic_plate.isspace() and lic_plate != '':
            break
    # Get current date
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    # Get date one year from now
    nextyear = datetime.datetime(datetime.datetime.now().year+1,datetime.datetime.now().month,datetime.datetime.now().day)
    # Create unique registration number
    c.execute('''SELECT MAX(regno) FROM registrations''')
    regno = c.fetchone()
    if regno[0] == None:
        regno = 1
    else:
        regno = int(regno[0])+1
    # Change expiry of old owner to today's date
    c.execute('''UPDATE registrations SET expiry=:expiry WHERE regno=:regno''',{'expiry':today,'regno':cur_reg[0]})
    conn.commit()
    # Create new registration for new owner
    c.execute('''INSERT INTO registrations VALUES (:regno,:regdate,:expiry,:plate,:vin,:fname,:lname)''',{'regno':regno,'regdate':today,'expiry':nextyear,'plate':lic_plate,'vin':vin,'fname':new_fname,'lname':new_lname})
    conn.commit()
    input("Ownership successfully transferred (Press Enter to Proceed)")
    

def process_payment(conn):
    # The user should be able to record a payment by entering a valid ticket number and an amount. 
    # The payment date is automatically set to the day of the payment (today's date). 
    # A ticket can be paid in multiple payments but the sum of those payments cannot exceed the fine amount of the ticket.
    c = conn.cursor()
    validation = True
    while True:
        # Get tno from user
        tno = input("Please enter the ticket number (tno): ")
        if tno.lower() == 'cancel':
            return
        # Check to see if tno is a number
        elif tno.isdigit(): 
            # Check to see if tno has a corresponding ticket
            c.execute('''SELECT *, fine FROM tickets WHERE tno=:tno''', {'tno':tno})
            ticket = c.fetchone()
            # No ticket associated with given ticket number
            if ticket == None:
                print("Invalid ticket number, please enter a valid ticket number.")
            else:
                validation = False
            while validation == False:
                # Get fine amount of ticket
                c.execute('''SELECT fine FROM tickets WHERE tno=:tno''', {'tno':tno})
                info = c.fetchone()
                amount = int(info[0])
                # Get current amount payed for
                c.execute('''SELECT SUM(amount) FROM payments WHERE tno=:tno''', {'tno':tno})
                info_1 = c.fetchone()[0]
                if info_1 == None:
                    sum_amount = 0
                else:
                    sum_amount = int(info_1)
                # If ticket already paid for
                if (amount-sum_amount) <= 0:
                    input("This ticket has already been paid for. (Press Enter to Continue)")
                    return
                # Check if payment has been made today (since unique key: tno + ddate)
                c.execute('''SELECT * FROM payments WHERE tno=:tno AND pdate = date('now','localtime')''', {'tno':tno})
                check = c.fetchone()
                if check != None:
                    input("You have already processed your payment today for tno: "+ str(tno) +" (Press Enter to Continue)")
                    return
                # Get how much user wants to pay
                while True:
                    print("You still owe $"+ str(amount-sum_amount) + ".")
                    payment = input("Please enter the payment ($): ")
                    if payment.lower() == 'cancel':
                        return
                    elif payment.isdigit():
                        if ((amount - sum_amount - int(payment)) < 0):
                            print("Payment is over the amount you owe.")
                        else:
                            validation = True
                            break
            update_date = datetime.datetime.now().strftime("%Y-%m-%d")
        break
    # Add payment to payments table
    c.execute('''INSERT INTO payments VALUES (:tno,:pdate,:amount)''',{'tno':tno,'pdate':update_date,'amount':payment})
    conn.commit()
    input("Payment successfully processed (Press Enter to Proceed)")


def get_driver_abstract(conn):
    # The user should be able to enter a first name and a last name and get a driver abstract, 
    # which includes the number of tickets, the number of demerit notices, the total number of demerit points received both within the past two years and within the lifetime. 
    # The user should be given the option to see the tickets ordered from the latest to the oldest. 
    # For each ticket, you will report the ticket number, the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. 
    # If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
    c = conn.cursor()
    # Get first name and last name of person to get information about
    while True:
        fname = input("First name: ")
        if fname.lower() == "cancel":
            return
        elif not fname.isspace() and fname != '':
            break
    while True:
        lname = input("Last name: ")
        if lname.lower() == "cancel":
            return
        elif not fname.isspace() and fname != '':
            break
    # Get number of tickets in person's lifetime
    c.execute('''SELECT count(tno) FROM registrations LEFT JOIN tickets ON registrations.regno = tickets.regno WHERE fname=:fname COLLATE NOCASE and lname=:lname COLLATE NOCASE GROUP BY fname,lname''',{'fname':fname,'lname':lname})
    numTickets = c.fetchone()
    if numTickets == None:
        numTickets = 0
    else:
        numTickets = numTickets[0]
    # Get number of tickets in last two years
    c.execute('''SELECT count(tno) FROM registrations LEFT JOIN tickets ON registrations.regno = tickets.regno WHERE fname=:fname COLLATE NOCASE and lname=:lname COLLATE NOCASE AND vdate>datetime('now','-2 years')  GROUP BY fname,lname''',{'fname':fname,'lname':lname})
    rec_numTickets = c.fetchone()
    if rec_numTickets == None:
        rec_numTickets = 0
    else:
        rec_numTickets = rec_numTickets[0]
    # Get number of demerit notices in person's lifetime
    c.execute('''SELECT count(points) FROM demeritNotices WHERE fname=:fname COLLATE NOCASE and lname=:lname COLLATE NOCASE GROUP BY fname,lname''',{'fname':fname,'lname':lname})
    numDemerits = c.fetchone()
    if numDemerits == None:
        numDemerits = 0
    else:
        numDemerits = numDemerits[0]
    # Get number of demerit notices in last two years
    c.execute('''SELECT count(points) FROM demeritNotices WHERE fname=:fname COLLATE NOCASE and lname=:lname COLLATE NOCASE AND ddate>datetime('now','-2 years') GROUP BY fname,lname''',{'fname':fname,'lname':lname})
    rec_numDemerits = c.fetchone()
    if rec_numDemerits == None:
        rec_numDemerits = 0
    else:
        rec_numDemerits = rec_numDemerits[0]
    # Get number of demerit points in last two years
    c.execute('''SELECT sum(points) FROM demeritNotices WHERE fname=:fname COLLATE NOCASE and lname=:lname COLLATE NOCASE AND ddate>datetime('now','-2 years') GROUP BY fname,lname''',{'fname':fname,'lname':lname})
    recentDemeritPoints = c.fetchone()
    if recentDemeritPoints == None:
        recentDemeritPoints = 0
    else:
        recentDemeritPoints = recentDemeritPoints[0]
    # Get number of demerit points in person's lifetime
    c.execute('''SELECT sum(points) FROM demeritNotices WHERE fname=:fname COLLATE NOCASE and lname=:lname COLLATE NOCASE GROUP BY fname,lname''',{'fname':fname,'lname':lname})
    totalDemeritPoints = c.fetchone()
    if totalDemeritPoints == None:
        totalDemeritPoints = 0
    else:
        totalDemeritPoints = totalDemeritPoints[0]
    print("Number of tickets in the last two years:",rec_numTickets)
    print("Number of tickets within entire lifetime:",numTickets)
    print("Number of demerit notices in the last two years:",rec_numDemerits)
    print("Number of demerit notices within entire lifetime:",numDemerits)
    print("Number of demerit points in the last two years:",recentDemeritPoints)
    print("Number of demerit points within entire lifetime:",totalDemeritPoints)
    if int(numTickets)>0:
        while True:
            # Ask user if ticket details should be printed
            getTickets = input("Get tickets? (y/n): ")
            if getTickets.lower() == 'y':
                c.execute('''SELECT * FROM registrations LEFT JOIN tickets ON registrations.regno = tickets.regno INNER JOIN vehicles ON registrations.vin = vehicles.vin WHERE fname=:fname COLLATE NOCASE and lname=:lname COLLATE NOCASE AND tno IS NOT NULL ORDER BY vdate DESC''',{'fname':fname,'lname':lname})
                tickets = c.fetchall()
                print("TNO | Ticket date | Description | Fine Amount | Regno | Vehicle")
                for i in range(len(tickets)):
                    print(tickets[i][7],'|',tickets[i][11],'|',tickets[i][10],'|',tickets[i][9],'|',tickets[i][8],'|',tickets[i][13],'|',tickets[i][14])
                    # Everytime 5 tickets have been printed, ask if more should be printed
                    if (i+1)%5==0:
                        while True:
                            getTickets = input('Continue getting tickets? (y/n): ')
                            if getTickets.lower() == 'y':
                                break
                            elif getTickets.lower() == 'n':
                                return
                break
            elif getTickets.lower() == 'n':
                break
    input("(Press Enter to Proceed)")

def addPerson(conn,fname,lname):
    # get first name and last name inputs from previous functions
    c = conn.cursor()
    print("First Name: "+fname)
    print("Last Name: "+lname)
    validdate = False
    while not validdate:
        bdate = input("Birth date (YYYY-MM-DD): ")
        if bdate.lower() == "cancel":
            return
        elif bdate.isspace() or bdate=='':
            bdate = None
            break
        else:
            validdate = True
            try:
                year,month,day = bdate.split("-")
                datetime.datetime(int(year),int(month),int(day))
            except ValueError:
                validdate = False
                print("Invalid date")
    blocation = input("Birth Location: ")
    if blocation.lower() == "cancel":
        return
    elif blocation.isspace() or blocation =='':
        blocation = None
    address = input("Current Address: ")
    if address.lower() == "cancel":
        return
    elif address.isspace() or address == '':
        address = None
    phone = input("Current Phone Number: ")
    if phone.lower() == "cancel":
        return
    elif phone.isspace() or phone == '':
        phone = None
    c.execute('''INSERT INTO persons VALUES (:fname,:lname,:bdate,:bplace,:address,:phone)''',{'fname':fname,'lname':lname,'bdate':bdate,'bplace':blocation,'address':address,'phone':phone})
    conn.commit()
    return 1