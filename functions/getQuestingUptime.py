from functions.classes.TablesManager import TablesManager


def getQuestingUptime(tablesManager: TablesManager):
    allAccounts = tablesManager.accounts.scan(
        FilterExpression="enabled_quester=:enabled_quester",
        ExpressionAttributeValues={
            ":enabled_quester": True,
        }
    )["Items"]
    questingAccounts = tablesManager.accounts.scan(
        FilterExpression="questing=:questing",
        ExpressionAttributeValues={
            ":questing": True
        }
    )["Items"]
   
    return len(questingAccounts)/len(allAccounts)


def getQuestingUptimeByProfession(tablesManager: TablesManager, profession: str):

    allAccounts = tablesManager.accounts.scan(
        FilterExpression="enabled_quester=:enabled_quester AND profession=:profession",
        ExpressionAttributeValues={
            ":enabled_quester": True,
            ":profession": profession
        }
    )["Items"]
    questingAccounts = tablesManager.accounts.scan(
        FilterExpression="questing=:questing AND profession=:profession",
        ExpressionAttributeValues={
            ":questing": True,
            ":profession": profession
        }
    )["Items"]
   
    return len(questingAccounts)/len(allAccounts)