from groups import getGroupByEmail

def getMembersOfGroup(service, groupId):
    return service.members().list(groupKey=groupId).execute().get('members', [])


def getMembersFromGroupEmail(service, email):
    group = getGroupByEmail(service, email)
    if group is not None:
        return getMembersOfGroup(service, group['id'])
    else:
        return None
