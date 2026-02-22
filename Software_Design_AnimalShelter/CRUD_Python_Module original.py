# CRUD_Python_Module.py
"""
CRUD operations for Animal collection in MongoDB
CS 340 Module Four Milestone
Provides Create and Read functionality for AAC database
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """
    
    def __init__(self, username='aacuser', password='MyStrongPassword123', host='localhost', port=27017, db='aac', collection='animals'):
        """
        Initialize the AnimalShelter with database connection
        
        Args:
            username (str): Database username
            password (str): Database password  
            host (str): MongoDB host
            port (int): MongoDB port
            db (str): Database name
            collection (str): Collection name
        """
        try:
            # Connection Variables
            self.USER = username
            self.PASS = password
            self.HOST = host
            self.PORT = port
            self.DB = db
            self.COL = collection
            
            # connection initialization
            self.client = MongoClient(f'mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}')
            self.database = self.client[self.DB]
            self.collection = self.database[self.COL]
            
            print("Successfully connected to MongoDB")
            
        except PyMongoError as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise Exception(f"Database connection failed: {e}")

    def create(self, data):
        """
        Insert a document into the animals collection (C in CRUD)
        
        Args:
            data (dict): Document to insert as key/value pairs
            
        Returns:
            bool: True if successful insert, else False
            
        Raises:
            Exception: If data parameter is empty
        """
        try:
            if data is not None:
                # Validate that data is a dictionary
                if not isinstance(data, dict):
                    raise ValueError("Data must be a dictionary")
                
                # Insert the document
                result = self.collection.insert_one(data)
                
                if result.inserted_id:
                    print(f"Document inserted successfully with ID: {result.inserted_id}")
                    return True
                else:
                    print("Failed to insert document")
                    return False
            else:
                raise Exception("Nothing to save, because data parameter is empty")
                
        except PyMongoError as e:
            logging.error(f"Error inserting document: {e}")
            print(f"Database error during insert: {e}")
            return False
        except Exception as e:
            logging.error(f"Error in create method: {e}")
            print(f"Error: {e}")
            return False

    def read(self, query=None):
        """
        Query for documents from the animals collection (R in CRUD)
        
        Args:
            query (dict): Key/value lookup pair for query. If None, returns all documents.
            
        Returns:
            list: List of documents if successful, else empty list
        """
        try:
            # when no query provided, return all documents
            if query is None:
                query = {}
            
            # validate that query is a dictionary
            if not isinstance(query, dict):
                raise ValueError("Query must be a dictionary")
            
            # use find() method and convert cursor to list
            cursor = self.collection.find(query)
            results = list(cursor)
            
            print(f"Query successful. Found {len(results)} documents")
            return results
            
        except PyMongoError as e:
            logging.error(f"Error querying documents: {e}")
            print(f"Database error during query: {e}")
            return []
        except Exception as e:
            logging.error(f"Error in read method: {e}")
            print(f"Error: {e}")
            return []

    def update(self, query, update_data):
        """
        Update documents in the animals collection (U in CRUD)
        
        Args:
            query (dict): Key/value lookup pair to find documents to update
            update_data (dict): Key/value pairs to update in the documents
        
        Returns:
            int: Number of documents modified
        """
        try:
            # we validate that query and update_data are dictionaries
            if not isinstance(query, dict):
                raise ValueError("Query must be a dictionary")
            if not isinstance(update_data, dict):
                raise ValueError("Update data must be a dictionary")
            
            # we then update documents using $set operator
            result = self.collection.update_many(query, {"$set": update_data})
            
            print(f"Update successful. Modified {result.modified_count} documents")
            return result.modified_count
            
        except PyMongoError as e:
            logging.error(f"Error updating documents: {e}")
            print(f"Database error during update: {e}")
            return 0
        except Exception as e:
            logging.error(f"Error in update method: {e}")
            print(f"Error: {e}")
            return 0

    def delete(self, query):
        """
        Delete documents from the animals collection (D in CRUD)
        
        Args:
            query (dict): Key/value lookup pair to find documents to delete
        
        Returns:
            int: Number of documents deleted
        """
        try:
            # validate that query is a dictionary
            if not isinstance(query, dict):
                raise ValueError("Query must be a dictionary")
            
            # delete documents
            result = self.collection.delete_many(query)
            
            print(f"Delete successful. Removed {result.deleted_count} documents")
            return result.deleted_count
            
        except PyMongoError as e:
            logging.error(f"Error deleting documents: {e}")
            print(f"Database error during delete: {e}")
            return 0
        except Exception as e:
            logging.error(f"Error in delete method: {e}")
            print(f"Error: {e}")
            return 0
    def read_water_rescue(self):
        return self.read({
            "animal_type": "Dog",
            "breed": {"$in": ["Labrador Retriever", "Chesapeake Bay Retriever", "Newfoundland"]},
            "age_upon_outcome_in_weeks": {"$lte": 104}
        })

    def read_mountain_rescue(self):
        return self.read({
            "animal_type": "Dog",
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Siberian Husky"]},
            "age_upon_outcome_in_weeks": {"$lte": 104}
        })

    def read_disaster_tracking(self):
        return self.read({
            "animal_type": "Dog",
            "breed": {"$in": ["Bloodhound", "Belgian Malinois", "German Shepherd"]},
            "age_upon_outcome_in_weeks": {"$lte": 104}
        })

