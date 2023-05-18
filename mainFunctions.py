from constants import maxRowLength, aclRoles, aclScopeTypes
from utils import printBoxAndAskUser, printTitle, printClosure, printBoxAndAskUserWithOptions, askUserWithOptions, getColoredText

from auth import loginWithDomainLevelServiceAccount

from users import getAllUsers, printFormattedUsers
from groups import getAllGroups, printFormattedGroups
from members import getMembersFromGroupEmail
from calendars import getCalendarListFromUserEmail, printCalendarList, addCalendarToUser, createAccessControlRule

def getDelegatedService(email):
    printTitle("Delegated Auth: "+email)
    delegatedService = loginWithDomainLevelServiceAccount("calendar", "v3", email)
    printClosure()
    return delegatedService

def listUsers(directoryService):
    printTitle("Users")
    printFormattedUsers(getAllUsers(directoryService))
    printClosure()

def listGroups(directoryService):
    printTitle("Groups")
    printFormattedGroups(getAllGroups(directoryService))
    printClosure()

def listMembersOfGroup(directoryService):
    email = printBoxAndAskUser(title="Group Email", label="Enter group email")
    printTitle("Members of "+email)
    printFormattedUsers(getMembersFromGroupEmail(directoryService, email))
    printClosure()

def listCalendarsOfUser(): 
    email = printBoxAndAskUser(title="User Email", label="Enter user email")
    delegatedService = getDelegatedService(email)
    printTitle("Calendars of "+email)
    printCalendarList(getCalendarListFromUserEmail(delegatedService, email))
    printClosure()

def addCalendar(calendarService):
    email = printBoxAndAskUser(title="User Email", label="Enter user email")
    delegatedService = getDelegatedService(email)
    calendarId = printBoxAndAskUser(title="Calendar Id", label="Enter calendar id")
    printTitle("Add "+calendarId+" to "+email)
    print("| Adding calendar to "+email+"...")
    addCalendarToUser(delegatedService, calendarId)
    print("| ")
    print("| Calendar list of "+email+" after the addition: ")
    printCalendarList(getCalendarListFromUserEmail(delegatedService, email))
    print("| ")
    if askUserWithOptions(
        label="[ y | n ]", 
        options=["y", "n"], 
        text="Do you want to add an ACL rule for this user?"
    ) == "y":
        printClosure()
        role = aclRoles.get(printBoxAndAskUserWithOptions(
            title="Role", 
            label="Enter role [ r | w | o | f ]", 
            options=aclRoles.keys(), 
            text="Available roles are: [r]eader, [w]riter, [o]wner or [f]ree and busy reader"
        ))
        printTitle("Create ACL rule for user " + email)
        createAccessControlRule(calendarService, email, calendarId, role)
    printClosure()


def createACLRule(calendarService):
    email = printBoxAndAskUser(title="User Email", label="Enter email of user")
    calendarId = printBoxAndAskUser(title="Calendar Id", label="Enter calendar id")
    role = aclRoles.get(printBoxAndAskUserWithOptions(
        title="Role", 
        label="Enter role [ r | w | o | f ]", 
        options=aclRoles.keys(), 
        text="Available roles are: [r]eader, [w]riter, [o]wner or [f]ree and busy reader"
    ))
    scopeType = aclScopeTypes.get(printBoxAndAskUserWithOptions(
        title="Scope Type",
        label="Enter scope type [ u | g | d ]",
        options=aclScopeTypes.keys(),
        text="Available scope types are: [u]ser, [g]roup or [d]omain"
    ))
    printTitle("Create ACL rule for " + scopeType + " " + email)
    createAccessControlRule(calendarService, email, calendarId, role, scopeType)
    printClosure()

def addCalendarAndACLRuleToGroup(directoryService, calendarService): 
    calendarId = printBoxAndAskUser(title="Calendar Id", label="Enter calendar id")
    groupEmail = printBoxAndAskUser(title="Group Email", label="Enter group email")
    role = aclRoles.get(printBoxAndAskUserWithOptions(
        title="Access Role for the Group", 
        label="Enter access role [ r | w | o | f ]", 
        options=aclRoles.keys(), 
        text="Available roles are: [r]eader, [w]riter, [o]wner or [f]ree and busy reader"
    )) 
    printTitle("Add Calendar to "+groupEmail)
    print("| Fetching group information...")
    users = getMembersFromGroupEmail(directoryService, groupEmail)
    if len(users) < 1:
        print("| "+getColoredText("There are no users in "+groupEmail+" or the group doesn't exist!", "yellow"))
        printClosure()
    elif askUserWithOptions(
        label="[ y | n ]", 
        options=["y", "n"], 
        text="Do you want to add the calendar to "+str(len(users))+" users in "+groupEmail+"?"
    ) == "y":
        printClosure()
        for user in users:
            delegatedService = getDelegatedService(user['email'])
            printTitle("Add Calendar to "+user['email'])
            print("| Adding calendar to "+user['email']+"...")
            addCalendarToUser(delegatedService, calendarId)
            calendars = getCalendarListFromUserEmail(delegatedService, user['email'])
            for cal in calendars:
                if cal['id'] == calendarId:
                    print("| " + getColoredText("Calendar added to "+user['email']+"!", "green"))
                    break
            else:
                print("| "+getColoredText("Unable to add calendar to "+user['email']+"!", "red"))
            printClosure()
        printTitle("Add ACL rule for "+groupEmail)
        createAccessControlRule(calendarService, groupEmail, calendarId, role, scope="group")
        printClosure()
    else: 
        print("| "+getColoredText("Canceled adding calendar to users in "+groupEmail+"...", "yellow"))
        printClosure()
        
def quit():
    print("\n" + "-"*maxRowLength)
    print("| Quitting the program, goodbye! ")
    print("-"*maxRowLength + "\n")