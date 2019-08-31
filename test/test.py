def DeleteConf():
    open('../confiles/postgresql.conf', 'w').close()


def removeSpace():
    s = open('../confiles/postgresql.conf').readlines()
    for x in s:
        print(x.rstrip('\n'))

removeSpace()

