from constants import maxRowLength

def getAllUsers(service): 
    results = service.users().list(customer='my_customer', maxResults=500, orderBy='email').execute()
    return results.get('users', [])

def getAndPrintAllUsers(service):
    print("\n" + "-"*3 + "Get Users" + "-"*(maxRowLength-9-3))
    users = getAllUsers(service)
    if not users:
        print('| No users in the domain.')
    else:
        print(u'| {0} Users:'.format(len(users)))
        for user in users:
            print(u'| \t{0} - {1} [{2}]'.format(user['name']['fullName'], user['primaryEmail'], user['id']))
    print("-"*maxRowLength + "\n")