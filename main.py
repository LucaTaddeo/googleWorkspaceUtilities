import time, os 
from auth import loginAndInitializeService

service = None

def welcome_script():
    global service
    os.system('clear')
    print("\n" + "-"*75)
    print("| Welcome to the Google Workspace Utils script!")
    print("-"*75 + "\n\n")
    time.sleep(0.5)

    print("\n" + "-"*3 + "Auth" + "-"*(75-4))
    print("| Initializing authentication process...")
    time.sleep(1)
    service = loginAndInitializeService()
    print("-"*75 + "\n\n")

    while True: 
        print("\n" + "-"*3 + "Supported functions" + "-"*(72-19))
        print("| [1] Get All Users")
        print("| [2] Get All Groups")
        print("| [3] Get All Members of a Group")
        
        choice = input("|\n| Enter your choice: ")
        print("-"*75 + "\n")
        
        if choice == "1":
            print("1")
            time.sleep(2)
        elif choice == "2":
            print("2")
            time.sleep(2)
        elif choice == "3":
            print("3")
            time.sleep(2)
        elif choice == "q":
            print("\n" + "-"*75)
            print("| Quitting the program, goodbye! ")
            print("-"*75 + "\n")
        else:
            print("Invalid choice. Please try again.")
            time.sleep(0.5)



if __name__ == '__main__':
    try:
        welcome_script()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")