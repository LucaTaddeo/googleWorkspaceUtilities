import time, os 
from constants import maxRowLength
from utils import printBoxAndAskUser, printTitle, printClosure

from auth import loginWithOAuthToken, loginWithDomainLevelServiceAccount

from users import getAllUsers, printFormattedUsers
from groups import getAllGroups, printFormattedGroups
from members import getMembersFromGroupName
from calendars import getCalendarListFromUserEmail, printCalendarList

directoryService = None

def welcome_script():
    global directoryService
    os.system('clear')
    print("\n" + "-"*maxRowLength)
    print("| Welcome to the Google Workspace Utils script!")
    print("-"*maxRowLength + "\n\n")
    time.sleep(0.5)

    print("\n" + "-"*3 + "Auth" + "-"*(maxRowLength-4-3))
    print("| Initializing authentication process...\n|")
    time.sleep(1)
    directoryService = loginWithOAuthToken("admin", "directory_v1")
    print("-"*maxRowLength + "\n\n")

    while True: 
        print("\n" + "-"*3 + "Supported functions" + "-"*(maxRowLength-19-3))
        print("| [1] Get All Users")
        print("| [2] Get All Groups")
        print("| [3] Get All Members of a Group")
        print("| [4] Get All Calendars of a User")
        print("| [q] Quit")

        
        choice = input("|\n| Enter your choice: ")
        print("-"*maxRowLength + "\n")
        
        if choice == "1":
            printTitle("Users")
            printFormattedUsers(getAllUsers(directoryService))
            printClosure()
            time.sleep(2)
        elif choice == "2":
            printTitle("Groups")
            printFormattedGroups(getAllGroups(directoryService))
            printClosure()
            time.sleep(2)
        elif choice == "3":
            name = printBoxAndAskUser(title="Group Name", label="Enter group name")
            printTitle("Members of "+name)
            printFormattedUsers(getMembersFromGroupName(directoryService, name))
            printClosure()
            time.sleep(2)
        elif choice == "4":
            email = printBoxAndAskUser(title="User Email", label="Enter user email")
            printTitle("Calendars of "+email)
            printCalendarList(getCalendarListFromUserEmail(email))
            printClosure()
        elif choice == "q":
            print("\n" + "-"*maxRowLength)
            print("| Quitting the program, goodbye! ")
            print("-"*maxRowLength + "\n")
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(0.5)



if __name__ == '__main__':
    try:
        welcome_script()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")