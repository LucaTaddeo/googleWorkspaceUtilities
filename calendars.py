from utils import getColoredText

def getCalendarListFromUserEmail(service, userEmail):
    try:
        return service.calendarList().list().execute().get("items")
    except:
        print("| "+getColoredText("Unable to get calendars for "+getColoredText(userEmail, "bold"), "red"))

def printCalendarList(calendars):
    if not calendars: 
        print("| " + getColoredText("No calendars found!", "yellow"))
    else: 
        for calendar in calendars: 
            printSingleCalendar(calendar)

def printSingleCalendar(calendar): 
    print(u'| [ID: {0}] {1}'.format(calendar['id'], calendar['summary']))

def addCalendarToUser(service, calendarId):
    try:
        return service.calendarList().insert(body={"id": calendarId}).execute()
    except:
        print("| "+getColoredText("Error: Impossible to add the calendar to the calendarList!", "red"))

def createAccessControlRule(service, userEmail, calendarId, role="reader", scope="user"):
    print("| Creating ACL Rule for "+userEmail+"...")
    try:
        rule = {
            'scope': {
                'type': scope,
                'value': userEmail
            },
            'role': role
        }

        res = service.acl().insert(calendarId=calendarId, body=rule).execute()
        print("| " + getColoredText(u'ACL Rule for {0} {1} with access role {2} created'
                                    .format(res['scope']['type'], res['scope']['value'], res['role']), "green"))
        return res
    except: 
        print("| "+getColoredText("Error: unable to create ACL rule!", "red"))