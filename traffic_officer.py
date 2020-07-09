import time, sqlite3, datetime, re, getpass

def issue_ticket(conn):
    # The user should be able to provide a registration number and see the person name that is listed in the registration and the make, model, year and color of the car registered. 
    # Then the user should be able to proceed and ticket the registration by providing a violation date, a violation text and a fine amount. 
    # A unique ticket number should be assigned automatically and the ticket should be recorded. 
    # The violation date should be set to today's date if it is not provided.
    c = conn.cursor()
    while True:
        regno = input("Enter Registration Number: ")
        if regno.lower() == 'cancel':
            return
        elif regno.isdigit():
            c.execute('''SELECT fname, lname FROM registrations WHERE regno =:regno''',{'regno':regno})
            names = c.fetchone()
            if names == None:
                print("Error, the registration doesn't exist on the database. Try again")
            else: 
                print("First Name: ", names[0])
                print("Last Name: ", names[1])
                c.execute(''' SELECT make, model, year, color FROM registrations LEFT JOIN vehicles ON registrations.vin = vehicles.vin WHERE regno =:regno''', {'regno':regno})
                car = c.fetchone()
                print("Vehicle details: ")
                print("Make: ", car[0])
                print("Model: ", car[1])
                print("Year: ", car[2])
                print("Color: ", car[3])
                v_text = input("Enter the violation text: ")
                if v_text.isspace() or v_text == '':
                    v_text = None
                fine = input("Enter the fine amount ($): ")
                while True:
                    check_date = input("Is the violation date today? (Y/N)")
                    if check_date.lower() == 'y':
                        v_date = datetime.datetime.now().strftime("%Y-%m-%d")
                        break
                    elif check_date.lower() == 'n': 
                        validdate = False
                        while validdate == False:
                            v_date = input("Enter the violation date (YYYY-MM-DD): ")
                            validdate = True
                            try:
                                year,month,day = v_date.split("-")
                                datetime.datetime(int(year),int(month),int(day))
                            except ValueError:
                                validdate = False
                                print("Invalid date")
                        break
                    elif check_date.lower() != 'y' or 'n':
                        print("Please choose an option")

                c.execute('''SELECT MAX(tno) FROM tickets''')
                tno = c.fetchone()
                if tno[0] == None:
                    tno = 1
                else:
                    tno = int(tno[0])+1
                break
        else:
            print("Invalid Registration Number")
    c.execute('''INSERT INTO tickets VALUES (:tno,:regno,:fine,:violation,:vdate)''', {'tno':tno,'regno':regno,'fine':fine,'violation':v_text,'vdate':v_date})
    conn.commit()  
    input("Ticket Successfully Issued (Press Enter to Continue)")

    
def find_car_owner(conn):
    # The user should be able to look for the owner of a car by providing one or more of make, model, year, color, and plate. 
    # The system should find and return all matches. 
    # If there are more than 4 matches, you will show only the make, model, year, color, and the plate of the matching cars and let the user select one. 
    # When there are less than 4 matches or when a car is selected from a list shown earlier, for each match, the make, model, year, color, and the plate of the matching car will be shown 
    # as well as the latest registration date, the expiry date, and the name of the person listed in the latest registration record.
    c = conn.cursor()
    while True:
        make = input('make: ')
        if make.lower() == "cancel":
            return
        model = input('model: ')
        if model.lower() == "cancel":
            return
        while True:
            year = input('year: ')
            if year.lower() == "cancel":
                return
            elif year.isdigit() or year.isspace() or year =='':
                break
            else:
                print("Invalid Year")
        color = input('color: ')
        if color.lower() == "cancel":
            return
        plate = input('plate: ')
        if plate.lower() == "cancel":
            return
        given_params = []
        params = {}
        if not make.isspace() and make != '':
            given_params.append('make=:make COLLATE NOCASE')
            params['make']=make
        if not model.isspace() and model != '':
            given_params.append("model=:model COLLATE NOCASE")
            params['model']=model
        if not year.isspace() and year != '':
            given_params.append('year=:year')
            params['year']=year
        if not color.isspace() and color != '':
            given_params.append("color=:color COLLATE NOCASE")
            params['color']=color
        if not plate.isspace() and plate != '':
            given_params.append("plate=:plate COLLATE NOCASE")
            params['plate']=plate
        if given_params:
            break
        else:
            print("Please provide at least one detail.")

    c.execute('''SELECT * FROM vehicles WHERE ''' + ' AND '.join(given_params), params)
    searchcar = c.fetchall()
    index = 1
    # 4 or more matches
    if len(searchcar) >= 4:
        for car in searchcar:
            c.execute('''SELECT * FROM registrations WHERE vin=:vin''', {'vin':car[0]})
            carreg = c.fetchone()
            # make, model, year, color, and the plate
            print(str(index) + ": " + car[1] + ", " + car[2] + ", " + str(car[3]) + ", " + car[4] + ", " + carreg[3])
            index += 1
        while True:
            selectcarnum = input ("Select one or type 'cancel' to return: ")
            if selectcarnum.lower() == 'cancel':
                return
            elif selectcarnum.isdigit() and int(selectcarnum)>=0 and int(selectcarnum)<=index: 
                selectcarnum = int(selectcarnum)-1
                c.execute('''SELECT * FROM registrations WHERE vin=:vin ORDER BY regdate DESC''', {'vin':searchcar[selectcarnum][0]})
                selectedcarreg = c.fetchone()
                # make, model, year, color, and the plate
                print("Selected: " + str(searchcar[selectcarnum][1]) + ", " + str(searchcar[selectcarnum][2]) + ", " + str(searchcar[selectcarnum][3]) + ", " + str(selectedcarreg[3]))
                # latest registration date, the expiry date, and the name of the person listed in the latest registration record.
                print("reg date: " + str(selectedcarreg[1]))
                print("expiry date: " + str(selectedcarreg[2]))
                print("owner: " + str(selectedcarreg[5]) + " " + str(selectedcarreg[6]))
            else:
                print('Invalid Option')
    # less than four matches
    else:
        for car in searchcar:
            c.execute('''SELECT * FROM registrations WHERE vin=:vin ORDER BY regdate DESC''', {'vin':car[0]})
            carreg = c.fetchone()
            print(str(index) + ": " + car[1] + ", " + car[2] + ", " + str(car[3]) + ", " + car[4] + ", " + carreg[3])
            print("reg date: " + carreg[1])
            print("expiry date: " + carreg[2])
            print("owner: " + carreg[5] + " " + carreg[6])
            print('')
            index += 1
            input("(Press Enter to Proceed)")