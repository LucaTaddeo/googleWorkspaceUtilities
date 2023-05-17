from auth import loginWithDomainLevelServiceAccount
from utils import getColoredText

def getCalendarListFromUserEmail(userEmail):
    delegatedService = loginWithDomainLevelServiceAccount("calendar", "v3", userEmail)
    if delegatedService is not None:
        try:
            return delegatedService.calendarList().list().execute().get("items")
        except:
            print("| "+getColoredText("Unable to get calendars for "+getColoredText(userEmail, "bold"), "red"))
    else: return None

def printCalendarList(calendars):
    if not calendars:
        print("| " + getColoredText("No calendars found!", "yellow"))
    else: 
        for calendar in calendars: 
            printSingleCalendar(calendar)

def printSingleCalendar(calendar): 
     print(u'| [ID: {0}] {1}'.format(calendar['id'], calendar['summary']))

def addCalendarToUser(userEmail, calendarId):
    delegatedService = loginWithDomainLevelServiceAccount("calendar", "v3", userEmail)
    if delegatedService is not None:
        try:
            return delegatedService.calendarList().insert(body={"id": calendarId}).execute()
        except:
            print("| "+getColoredText("Error: Impossible to add the calendar to the calendarList!", "red"))
    else: return None
         