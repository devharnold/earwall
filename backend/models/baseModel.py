#!/usr/bin/env python3
"""
class BaseModel
"""
import uuid
from datetime import datetime
import psycopg2
import models
import os
from os import getenv
from dotenv import load_dotenv
from backend.engine.db_storage import get_db_connection

load_dotenv()

class BaseModel:
    """The basemodel class from which classes will be derived"""
    def __init__(self, *args, **kwargs):
        """Initialize the basemodel"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and isinstance(self.created_at, str):
                self.created_at = datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None)is None:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.utcnow()
                self.updated_at = self.created_at

    def __str__(self):
        """String representation of basemodel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """Saves instance to the database"""
        self.updated_at = datetime.utcnow()
        connection = self.get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO models (id, created_at, updated_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET updated_at = EXCLUDED.updated_at;
        """, (self.id, self.created_at, self.updated_at))

        connection.commit()
        cursor.close()
        connection.close()

    def to_dict(self):
        """Return a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        new_dict["__class__"] = self.__class__.__name__
        return new_dict
    
    def delete(self):
        """Delete the current instance from the database"""
        connection = self.get_db_connection()
        cursor = connection.cursor()
        
        # Implement logic to delete instance
        cursor.execute("DELETE FROM models WHERE id = %s;", (self.id,))
        
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def get_db_connection():
        """Create and return a new db connection"""
        return psycopg2.connect(
            host= os.getenv(),
            port= os.getenv(),
            dbname= os.getenv(),
            user= os.getenv(),
            password= os.getenv()
        )