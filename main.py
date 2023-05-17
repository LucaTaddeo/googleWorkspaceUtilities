import time, os 
from constants import maxRowLength, aclRoles
from utils import printBoxAndAskUser, printTitle, printClosure, printBoxAndAskUserWithOptions

from auth import loginWithOAuthToken, loginWithDomainLevelServiceAccount

from users import getAllUsers, printFormattedUsers
from groups import getAllGroups, printFormattedGroups
from members import getMembersFromGroupName
from calendars import getCalendarListFromUserEmail, printCalendarList, addCalendarToUser, createAccessControlRule

directoryService = None
calendarService = None

def getDelegatedService(email):
    printTitle("Delegated Auth: "+email)
    delegatedService = loginWithDomainLevelServiceAccount("calendar", "v3", email)
    printClosure()
    return delegatedService

def welcome_script():
    global directoryService
    os.system('clear')
    print("\n" + "-"*maxRowLength)
    print("| Welcome to the Google Workspace Utils script!")
    print("-"*maxRowLength + "\n\n")
    time.sleep(0.5)

    printTitle("Auth")
    print("| Initializing authentication process...\n|")
    time.sleep(1)

    directoryService = loginWithOAuthToken("admin", "directory_v1")
    print("|")
    calendarService = loginWithOAuthToken("calendar", "v3")
    
    print("-"*maxRowLength + "\n\n")

    while True: 
        printTitle("Main Menu")
        print("| [1] List Users")
        print("| [2] List Groups")
        print("| [3] List Members of Group")
        print("| [4] List Calendars of User")
        print("| [5] Add Calendar to User")
        print("| [6] Create ACL Rule")
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
            delegatedService = getDelegatedService(email)
            printTitle("Calendars of "+email)
            printCalendarList(getCalendarListFromUserEmail(delegatedService, email))
            printClosure()
        elif choice == "5":
            email = printBoxAndAskUser(title="User Email", label="Enter user email")
            delegatedService = getDelegatedService(email)
            calendarId = printBoxAndAskUser(title="Calendar Id", label="Enter calendar id")
            #ask for background color  
            printTitle("Add "+calendarId+" to "+email)
            res = addCalendarToUser(email, calendarId)
            print(u'| {0}'.format(res)) if res is not None else None
            print("| ")
            print("| Calendar list of "+email+" after the addition: ")
            printCalendarList(getCalendarListFromUserEmail(email))
            printClosure()
        elif choice == "6":
            email = printBoxAndAskUser(title="User Email", label="Enter email of user")
            calendarId = printBoxAndAskUser(title="Calendar Id", label="Enter calendar id")
            role = aclRoles.get(printBoxAndAskUserWithOptions(
                title="Role", 
                label="Enter role [ r | w | o | f ]", 
                options=aclRoles.keys(), 
                text="Available roles are: [r]eader, [w]riter, [o]wner or [f]ree and busy reader"
            ))
            printTitle("Create ACL rule for "+email)
            res = createAccessControlRule(calendarService, email, calendarId, role)
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