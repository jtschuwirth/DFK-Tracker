def getQuestingUptime(accounts_table):
    allAccounts = accounts_table.scan()["Items"]
    questingAccounts = accounts_table.scan(
        FilterExpression="questing=:questing",
        ExpressionAttributeValues={
            ":questing": True
        }
    )["Items"]
   
    return len(questingAccounts)/len(allAccounts)
