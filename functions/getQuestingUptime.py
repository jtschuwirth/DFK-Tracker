def getQuestingUptime(accounts_table):
    allAccounts = accounts_table.scan(
        FilterExpression="enabled_quester=:enabled_quester",
        ExpressionAttributeValues={
            ":enabled_quester": True
        }
    )["Items"]
    questingAccounts = accounts_table.scan(
        FilterExpression="questing=:questing",
        ExpressionAttributeValues={
            ":questing": True
        }
    )["Items"]
   
    return len(questingAccounts)/len(allAccounts)
