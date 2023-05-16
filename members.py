from groups import getGroupByName

def getMembersOfGroup(service, groupId):
    return service.members().list(groupKey=groupId).execute().get('members', [])


def getMembersFromGroupName(service, name):
    group = getGroupByName(service, name)
    if group is not None:
        return getMembersOfGroup(service, group['id'])
    else:
        return None
