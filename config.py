from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    # connecting with the database
    print('Establishing connection with the database'.center(100, '='))
    client = MongoClient('mongodb://%s:%s@127.0.0.1' % ('myUserAdmin', 'abc123'))
    print('Connection Established Successfully!')

    # Printing all the available databases
    print("Databases available: ", client.list_database_names())

    # creating the database for bank
    my_database = client['bankapi']
    print('Database successfully created', my_database)

    # Printing all the available databases
    print("Databases available: ", client.list_database_names())

except ConnectionFailure as e:
    print("Connection Error: ", e)



