from flask_app.config.mysqlconnection import connectToMySQL
import datetime
from flask import flash, session
from flask_app.models import user

class Skeptic:
    DB = "beltexam_schema"
    def __init__( self , data ):
        self.sightings_id = data['sightings_id']
        self.users_id = data['users_id']
        self.skeptic_info = None

    @classmethod
    def save(cls, data ):
        query = """
            INSERT INTO skeptics ( sightings_id, users_id ) 
            VALUES ( %(sightings_id)s, %(users_id)s  );
            """
        result = connectToMySQL(cls.DB).query_db( query, data )
        return result
    
    @classmethod
    def get_all_skeptics(cls, data):
        query = """
            SELECT * from skeptics 
            JOIN users ON skeptics.users_id = users.id 
            JOIN sightings ON skeptics.sightings_id = sightings.id 
            WHERE sightings_id = %(id)s
            """
        results = connectToMySQL(cls.DB).query_db(query, data)
        skepticslist = []
        for single_skeptic in results:
            this_skeptic = cls(single_skeptic)
            this_skeptic_info = {
                "id": single_skeptic['id'],
                "first_name": single_skeptic['first_name'],
                "last_name": single_skeptic['last_name'],
                "email": single_skeptic['email'],
                "password": single_skeptic['password'],
                "created_at": single_skeptic['created_at'],
                "updated_at": single_skeptic['updated_at']
            }
            info = user.User(this_skeptic_info)
            this_skeptic.skeptic_info = info
            skepticslist.append(this_skeptic) 
        return skepticslist
    
    @classmethod
    def get_one_skeptic(cls, data):
        query = """
            SELECT * from skeptics 
            JOIN users ON skeptics.users_id = users.id 
            JOIN sightings ON skeptics.sightings_id = sightings.id 
            WHERE sightings_id = %(sightings_id)s AND skeptics.users_id = %(users_id)s
            """        
        results = connectToMySQL(cls.DB).query_db(query, data)
        for skeptic in results:
            this_skeptic = cls(skeptic)
            this_skeptic_info = {
                "id": skeptic['users.id'],
                "first_name": skeptic['first_name'],
                "last_name": skeptic['last_name'],
                "email": skeptic['email'],
                "password": skeptic['password'],
                "created_at": skeptic['users.created_at'],
                "updated_at": skeptic['users.updated_at']
            }
            this_skeptic.skeptic_info = user.User(this_skeptic_info)
        return this_skeptic
    
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM skeptics
            WHERE users_id = %(users_id)s AND sightings_id = %(sightings_id)s;"""
        return connectToMySQL(cls.DB).query_db(query, data)