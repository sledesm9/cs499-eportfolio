# CRUD_Python_Module.py
"""
Simple CRUD for the Animal collection in MongoDB.

Created for the CS 340 project and later enhanced for CS 499.
This module handles database operations so the dashboard code
doesn’t need to talk to MongoDB directly.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging
import os

# Basic logging setup so database actions and errors are recorded
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


class AnimalShelter(object):
    """CRUD helper class for the MongoDB animals collection."""
    
    def __init__(self, username='aacuser', password='MyStrongPassword123',
                 host='localhost', port=27017, db='aac', collection='animals'):
        """
        Set up the database connection when the class is created.
        Stores connection settings and opens the MongoDB client.

        Args:
            username (str): MongoDB username
            password (str): MongoDB password  
            host (str): Database server address
            port (int): Database port number
            db (str): Database name
            collection (str): Collection name
        """
        try:
            # Save connection settings
            self.USER = username
            self.PASS = password
            self.HOST = host
            self.PORT = port
            self.DB = db
            self.COL = collection
            
            # Open MongoDB connection and select database/collection
            self.client = MongoClient(
                f'mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}'
            )
            self.database = self.client[self.DB]
            self.collection = self.database[self.COL]
            
            logger.info("Successfully connected to MongoDB")
            
        except PyMongoError as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise Exception(f"Database connection failed: {e}")

    def create(self, data):
        """
        Insert one document into the animals collection.

        Args:
            data (dict): Record to insert

        Returns:
            bool: True if insert worked, False if it failed
        """
        try:
            if data is not None:

                # Make sure the input is a dictionary
                if not isinstance(data, dict):
                    raise ValueError("Data must be a dictionary")
                
                # Insert record into MongoDB
                result = self.collection.insert_one(data)
                
                if result.inserted_id:
                    logger.info("Document inserted successfully: %s",
                                result.inserted_id)
                    return True
                else:
                    print("Failed to insert document")
                    return False
            else:
                raise Exception("Nothing to save, data parameter is empty")
                
        except PyMongoError as e:
            logging.error(f"Error inserting document: {e}")
            logger.error("Database error during insert", exc_info=True)
            return False
        except Exception as e:
            logging.error(f"Error in create method: {e}")
            return False

    def read(self, query=None):
        """
        Read records from the animals collection.

        If no query is provided, it returns all records.

        Args:
            query (dict): Search filter (optional)

        Returns:
            list: Matching documents (or empty list if error)
        """
        try:
            # If no filter is provided, return everything
            if query is None:
                query = {}
            
            # Make sure the query is the right type
            if not isinstance(query, dict):
                raise ValueError("Query must be a dictionary")
            
            # Run the query and convert results to a list
            cursor = self.collection.find(query)
            results = list(cursor)
            
            logger.info("Query successful. Found %d documents",
                        len(results))
            return results
            
        except PyMongoError as e:
            logging.error(f"Error querying documents: {e}")
            return []
        except Exception as e:
            logging.error(f"Error in read method: {e}")
            return []

    def update(self, query, update_data):
        """
        Update matching records in the animals collection.

        Args:
            query (dict): Filter to choose which records to update
            update_data (dict): Fields and values to change

        Returns:
            int: Number of records updated
        """
        try:
            # Basic input checks
            if not isinstance(query, dict):
                raise ValueError("Query must be a dictionary")
            if not isinstance(update_data, dict):
                raise ValueError("Update data must be a dictionary")
            
            # Apply updates using MongoDB $set
            result = self.collection.update_many(
                query, {"$set": update_data}
            )
            
            print(f"Update successful. Modified {result.modified_count} documents")
            return result.modified_count
            
        except PyMongoError as e:
            logging.error(f"Error updating documents: {e}")
            return 0
        except Exception as e:
            logging.error(f"Error in update method: {e}")
            return 0

    def delete(self, query):
        """
        Delete matching records from the animals collection.

        Args:
            query (dict): Filter to choose which records to remove

        Returns:
            int: Number of records deleted
        """
        try:
            # Make sure query is valid
            if not isinstance(query, dict):
                raise ValueError("Query must be a dictionary")
            
            # Remove matching records
            result = self.collection.delete_many(query)
            
            print(f"Delete successful. Removed {result.deleted_count} documents")
            logger.info("Delete successful. Removed %d documents",
                        result.deleted_count)
            return result.deleted_count
            
        except PyMongoError as e:
            logging.error(f"Error deleting documents: {e}")
            return 0
        except Exception as e:
            logging.error(f"Error in delete method: {e}")
            return 0

    # -------- Preset Rescue Queries --------
    # These helper methods return filtered dog lists
    # based on the rescue category rules.

    def read_water_rescue(self):
        return self.read({
            "animal_type": "Dog",
            "breed": {"$in": [
                "Labrador Retriever",
                "Chesapeake Bay Retriever",
                "Newfoundland"
            ]},
            "age_upon_outcome_in_weeks": {"$lte": 104}
        })

    def read_mountain_rescue(self):
        return self.read({
            "animal_type": "Dog",
            "breed": {"$in": [
                "German Shepherd",
                "Alaskan Malamute",
                "Siberian Husky"
            ]},
            "age_upon_outcome_in_weeks": {"$lte": 104}
        })

    def read_disaster_tracking(self):
        return self.read({
            "animal_type": "Dog",
            "breed": {"$in": [
                "Bloodhound",
                "Belgian Malinois",
                "German Shepherd"
            ]},
            "age_upon_outcome_in_weeks": {"$lte": 104}
        })
