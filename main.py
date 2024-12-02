import time, os 
from constants import maxRowLength
from utils import printTitle, printClosure

from auth import loginWithOAuthToken, loginWithDomainLevelServiceAccount

from mainFunctions import listUsers, listGroups, listMembersOfGroup, listCalendarsOfUser, addCalendar, createACLRule, addCalendarAndACLRuleToGroup, autoAddEachCalendarToEachGroup, removeCalendarFromGroup, quit

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
        print("| [7] Add calendar and ACL rule to group")
        print("| [8] Remove calendar from group")
        print("| [9] Auto-add each calendar to each group")
        print("| [q] Quit")
        
        choice = input("|\n| Enter your choice: ")
        print("-"*maxRowLength + "\n")
        
        if choice == "1":
            listUsers(directoryService)
            time.sleep(2)
        elif choice == "2":
            listGroups(directoryService)
            time.sleep(2)
        elif choice == "3":
            listMembersOfGroup(directoryService)
            time.sleep(2)
        elif choice == "4":
            listCalendarsOfUser()
            time.sleep(2)
        elif choice == "5":
            addCalendar(calendarService)
            time.sleep(2)
        elif choice == "6":
            createACLRule(calendarService)
            time.sleep(2)
        elif choice == "7":
            addCalendarAndACLRuleToGroup(directoryService, calendarService)
            time.sleep(2)
        elif choice == "8":
            removeCalendarFromGroup(directoryService, calendarService)
            time.sleep(2)
        elif choice == "9":
            autoAddEachCalendarToEachGroup(directoryService, calendarService)
            time.sleep(2)
        elif choice == "q":
            quit()
            break
        else:
            print("Invalid choice. Please try again.")
            time.sleep(0.5)



if __name__ == '__main__':
    try:
        welcome_script()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")