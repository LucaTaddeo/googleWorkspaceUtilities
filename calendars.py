
from auth import loginWithDomainLevelServiceAccount

def getCalendarListFromUserEmail(userEmail):
    try: 
        delegatedService = loginWithDomainLevelServiceAccount("calendar", "v3", userEmail)
        return delegatedService.calendarList().list().execute().get("items")
    except :
        print("| Error: email is invalid or unauthorized user!")
        return None

def printCalendarList(calendars):
    if not calendars:
        print("| No calendars found!")
    else: 
        for calendar in calendars: 
            printSingleCalendar(calendar)

def printSingleCalendar(calendar): 
     print(u'| [{0}] {1}'.format(calendar['id'], calendar['summary']))