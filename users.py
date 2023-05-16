def getAllUsers(service): 
    results = service.users().list(customer='my_customer', maxResults=500, orderBy='email').execute()
    return results.get('users', [])

def printFormattedUsers(users):
    if not users:
        print('| No users found!')
    else:
        for user in users:
            printSingleUser(user)

def printSingleUser(user):
    print(u'| [ID: {1}] {0}'.format(user.get('email') or user.get('primaryEmail', 'N/A'), user['id']))
