import time, sqlite3, datetime, re, getpass,os, sys
import agent, traffic_officer

def login(c,uid,pwd):
    c.execute('''SELECT * FROM users WHERE uid = :username;''',{'username':uid})
    user = c.fetchone()
    if user == None:
        return None
    elif pwd == user[1]:
        return user
    else:
        return None

def agent_menu(user,conn):
    action = None
    while action != 8 or action.lower()=="exit":
        os.system('clear')
        print("Agent Menu:")
        print("1. Register a birth")
        print("2. Register a marriage")
        print("3. Renew a vehicle registration")
        print("4. Process a bill of sale")
        print("5. Process a payment")
        print("6. Get a driver abstract")
        print("7. Logout")
        print("8. Exit")
        action = input("Enter the number to which the action corresponds to: ")
        if action == '1':
            os.system('clear')
            agent.register_birth(user,conn)
        elif action == '2':
            os.system('clear')
            agent.register_marriage(user,conn)
        elif action == "3":
            os.system('clear')
            agent.renew_vehicle_registration(conn)
        elif action == "4":
            os.system('clear')
            agent.process_bill(conn)
        elif action == '5':
            os.system('clear')
            agent.process_payment(conn)
        elif action == '6':
            os.system('clear')
            agent.get_driver_abstract(conn)
        elif action == '7' or action.lower()=="logout":
            os.system('clear')
            return
        elif action == '8' or action.lower()=="exit":
            os.system('clear')
            sys.exit()
        else:
            os.system('clear')
            print ("Invalid Action.")

def traffic_officer_menu(user,conn):
    action = None
    while action != 4 or action.lower()=="exit":
        os.system('clear')
        print("Traffic Officer Menu:")
        print("1. Issue a ticket")
        print("2. Find a car owner")
        print("3. Logout")
        print("4. Exit")
        action = input("Enter the number to which the action corresponds to: ")
        if action == '1':
            os.system('clear')
            traffic_officer.issue_ticket(conn)
        elif action == '2':
            os.system('clear')
            traffic_officer.find_car_owner(conn)
        elif action == '3' or action.lower()=="logout":
            os.system('clear')
            return
        elif action == '4' or action.lower()=="exit":
            os.system('clear')
            sys.exit()
        else:
            os.system('clear')
            print("Invalid Action.")

def main():
    if len(sys.argv)>2 or len(sys.argv)<2:
        print("Invalid number of arguments")
        return
    
    conn = sqlite3.connect(sys.argv[1],timeout=30)
    c = conn.cursor()
    while True:
        os.system('clear')
        user = None
        while user == None:
            uid = input("UID: ")
            pwd = getpass.getpass("PWD: ")
            user = login(c,uid,pwd)
            if user == None:
                os.system('clear')
                print("Invalid user ID or password")
        if user[2] == 'a':
            agent_menu(user,conn)
        elif user[2] == 'o':
            traffic_officer_menu(user,conn)

main()