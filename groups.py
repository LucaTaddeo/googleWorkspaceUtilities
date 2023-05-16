from constants import maxRowLength

def getAllGroups(service):
    results = service.groups().list(customer='my_customer').execute()
    return results.get('groups', [])

def getAndPrintAllGroups(service):
    print("\n" + "-"*3 + "Groups" + "-"*(maxRowLength-7-3))
    groups = getAllGroups(service)
    if not groups:
        print('| No groups in the domain.')
    else:
        print(u'| {0} Groups:'.format(len(groups)))
        for group in groups:
            print(u'| {0} - {1} [{2}]'.format(group['name'], group['email'], group['id']))
    print("-"*maxRowLength + "\n")

def getGroupByName(service, name):
    groups = service.groups().list(customer='my_customer').execute().get('groups', [])
    for group in groups:
        if group['name'] == name:
            return group
    return None

def printFormattedGroups(groups):
    if not groups:
        print('| No groups found!')
    else:
        for group in groups:
            printSingleGroup(group)

def printSingleGroup(group):
    print(u'| [{2}] {0} - {1} '.format(group['name'], group['email'], group['id']))

