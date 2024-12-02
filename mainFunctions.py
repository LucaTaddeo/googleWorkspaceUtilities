import json
import os
from constants import maxRowLength, aclRoles, aclScopeTypes
from utils import printBoxAndAskUser, printTitle, printClosure, printBoxAndAskUserWithOptions, askUserWithOptions, getColoredText

from auth import loginWithDomainLevelServiceAccount

from users import getAllUsers, printFormattedUsers
from groups import getAllGroups, printFormattedGroups
from members import getMembersFromGroupEmail
from calendars import getCalendarListFromUserEmail, printCalendarList, addCalendarToUser, createAccessControlRule, removeCalendarFromUser

import sys
from contextlib import contextmanager
from io import StringIO

@contextmanager
def silencedPrints():
    original_stdout = sys.stdout
    try:
        sys.stdout = StringIO()  # Redirect stdout to a buffer
        yield
    finally:
        sys.stdout = original_stdout  # Restore original stdout

def askForColors():
    printTitle("Colors")
    askForColors = askUserWithOptions(label="Do you want to set colors for the calendars? [ y | n ]", options=["y", "n"], text="If you don't set colors, the default color will be used")
    if askForColors == "y":
        print("| ")
        print("| Available colors: ")
        print("| 1: Copper, 2: Terra Cotta, 3: Flame, 4: Tangerine, 5: Orange Peel, 6: Yellow Orange, 7: Mint, 8: Jungle Green,")
        print("| 9: Meadow Green, 10: Lime Green, 11: Daffodil, 12: Goldenrod, 13: Turquoise, 14: Sky Blue, 15: Cornflower Blue, 16: Cerulean,")
        print("| 17: Lavender, 18: Amethyst, 19: Cool Gray, 20: Rose Quartz, 21: Blush, 22: Pink Flamingo, 23: Orchid, 24: Wisteria")
        print("| ")
        bgColor = input("| Enter colorId: ")
        return bgColor
    else:
        print("| Default colors will be used")
        printClosure()
        return None


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
    colorId = askForColors()
    printTitle("Add "+calendarId+" to "+email)
    print("| Adding calendar to "+email+"...")
    res = addCalendarToUser(delegatedService, calendarId, colorId=colorId)
    print("| Fetching calendars of "+email+"...")
    calendars = getCalendarListFromUserEmail(delegatedService, email)
    for cal in calendars:
        if cal['id'] == calendarId:
            print("| " + getColoredText(u'Calendar {0} added to user with access role {1}'
                                    .format(res['summary'], res['accessRole']), "green"))
            break
    else:
        print("| "+getColoredText("Unable to add calendar to "+email+"!", "red"))
    print("| ")
    print("| Calendar list of "+email+" after the addition: ")
    printCalendarList(calendars)
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
    colorId = askForColors()
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
        for i, user in enumerate(users):
            delegatedService = getDelegatedService(user['email'])
            printTitle("["+str(i+1)+"/"+str(len(users))+"] Add Calendar to "+user['email'])
            print("| Adding calendar to "+user['email']+"...")
            addCalendarToUser(delegatedService, calendarId, colorId=colorId)
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

def autoAddEachCalendarToEachGroup(directoryService, calendarService):
    printTitle("Initializing auto-add")
    print("| This process will add each calendar with read properties to each group.")
    print("| You can handle the pairing from the input.json file!")
    role = aclRoles.get("r") 
    if askUserWithOptions(
        label="[ y | n ]", 
        options=["y", "n"], 
        text="Do you want to continue?"
    ) == "y":
        if not os.path.exists("input.json"):
            print("| "+getColoredText("input.json file not found!", "red"))
            printClosure()
        else:
            printClosure()
            with open("input.json", "r") as file:
                groupsAndCalendars = json.load(file)
                groupsAndCalendarsLength = str(len(groupsAndCalendars))

                for i, groupAndCalendar in enumerate(groupsAndCalendars):
                    calCounter = "[" + str(i + 1) + "/" + groupsAndCalendarsLength + "] "
                    printTitle(calCounter + "Adding Calendar to " + groupAndCalendar['groupEmail'])
                    calendarId = groupAndCalendar['calendarId']
                    groupEmail = groupAndCalendar['groupEmail']
                    print("| Calendar Id: " + calendarId)
                    print("| Group Email: " + groupEmail)
                    print("| ")
                    print("| Fetching group information...")
                    users = getMembersFromGroupEmail(directoryService, groupEmail)
                    
                    usersLength = str(len(users))
                    print("| " + usersLength + " users found in " + groupEmail)
                    print("| ")
                    
                    for j, user in enumerate(users):
                        with silencedPrints():
                            delegatedService = getDelegatedService(user['email'])
                        userCounter = "[" + str(j + 1) + "/" + usersLength + "] "
                        print("| " + userCounter + "Adding calendar to " + user['email'] + "...")
                        addCalendarToUser(delegatedService, calendarId)
                        calendars = getCalendarListFromUserEmail(delegatedService, user['email'])
                        for cal in calendars:
                            if cal['id'] == calendarId:
                                break
                        else:
                            print("| "+getColoredText("Unable to add calendar to "+user['email']+"!", "red"))
                    print("| ")
                    createAccessControlRule(calendarService, groupEmail, calendarId, role, scope="group")
                    print("| ") 
                    print("| " + getColoredText("Calendar added to users in" + groupEmail + "!", "green"))
                    printClosure()
    else: 
        print("| " + getColoredText("Canceled auto-add process...", "yellow"))
        printClosure()
        
def removeCalendarFromGroup(directoryService, calendarService):
    calendarId = printBoxAndAskUser(title="Calendar Id", label="Enter calendar id")
    groupEmail = printBoxAndAskUser(title="Group Email", label="Enter group email")
    printTitle("Remove Calendar from "+groupEmail)
    print("| Fetching group information...")
    users = getMembersFromGroupEmail(directoryService, groupEmail)
    if len(users) < 1:
        print("| "+getColoredText("There are no users in "+groupEmail+" or the group doesn't exist!", "yellow"))
        printClosure()
    elif askUserWithOptions(
        label="[ y | n ]", 
        options=["y", "n"], 
        text="Do you want to remove the calendar from "+str(len(users))+" users in "+groupEmail+"?"
    ) == "y":
        printClosure()
        for user in users:
            delegatedService = getDelegatedService(user['email'])
            printTitle("Removing Calendar from "+user['email'])
            print("| Removing calendar from "+user['email']+"...")
            removeCalendarFromUser(delegatedService, calendarId)
            calendars = getCalendarListFromUserEmail(delegatedService, user['email'])
            for cal in calendars:
                if cal['id'] == calendarId:
                    print("| "+getColoredText("Unable to remove calendar from "+user['email']+"!", "red"))
                    break
            else:
                print("| " + getColoredText("Calendar removed from "+user['email']+"!", "green"))
            printClosure()
        # printTitle("Add ACL rule for "+groupEmail)
        # createAccessControlRule(calendarService, groupEmail, calendarId, role, scope="group")
        # printClosure()
    else: 
        print("| "+getColoredText("Canceled removing calendar from users in "+groupEmail+"...", "yellow"))
        printClosure()

def quit():
    print("\n" + "-"*maxRowLength)
    print("| Quitting the program, goodbye! ")
    print("-"*maxRowLength + "\n")