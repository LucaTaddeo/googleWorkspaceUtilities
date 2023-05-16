from constants import maxRowLength

def getAllGroups(service):
    results = service.groups().list(customer='my_customer').execute()
    return results.get('groups', [])

def getAndPrintAllGroups(service):
    print("\n" + "-"*3 + "Get Groups" + "-"*(maxRowLength-10-3))
    groups = getAllGroups(service)
    if not groups:
        print('| No groups in the domain.')
    else:
        print(u'| {0} Groups:'.format(len(groups)))
        for group in groups:
            print(u'| \t{0} - {1} [{2}]'.format(group['name'], group['email'], group['id']))
    print("-"*maxRowLength + "\n")