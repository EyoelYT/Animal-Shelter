from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    # Definiing the Mongodb database object
    # You can add the host and port as parameters in this function later.
    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # Connection Variables
        #
        USER = str(username)
        PASS = str(password)
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 32312
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #

        self.client = MongoClient('mongodb://%s:%s@%s:%d/admin' % (USER,PASS,HOST,PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

 # Method that implements the C in CRUD.
    def addAnimal(self, data):
        if data and isinstance(data, dict): # check if there is data and it is a dictionary
            self.database.animals.insert_one(data)  
            return True            
        else:
            raise Exception("Invalid data request to be added.")

# Method that implements the R in CRUD.
    def getAllAnimals(self):
        return list(self.database.animals.find()) 
    
# Method that returns all found under a column
    def getAllProperties(self, column_name):
        column_name = str(column_name)
        return list(self.database.animals.distinct(column_name))
    
# Method that fetches all the animals that have elements that match with said criteria
    def getAllAnimalsWithCriteria(self, criteria):
        if not isinstance(criteria, dict):  # Ensure the criteria is a dictionary
            raise ValueError("Criteria should be a dictionary.")
        return list(self.database.animals.find(criteria))
    
# Method that reads the first animal with the input criteria
    def getFirstAnimal(self, criteria):
        if isinstance(criteria, dict):
            return self.database.animals.find_one(criteria)
        else:
            raise Exception("Invalid criteria provided.")
        
# Update method that implements the U in CRUD.
    def modifyAnimals(self, criteria, updates):
        if isinstance(criteria, dict) and isinstance(updates, dict):
            result = self.collection.update_many(criteria, {'$set': updates})
            return result.modified_count
        else:
            raise ValueError("Invalid criteria or updates provided.")

# Delete method that implements the D in CRUD.
    def removeAnimals(self, criteria):
        if isinstance(criteria, dict):
            result = self.collection.delete_many(criteria)
            return result.deleted_count
        else:
            raise ValueError("Invalid criteria given.")


