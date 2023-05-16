from flask_app.config.mysqlconnection import connectToMySQL
import datetime
from flask import flash, session
from flask_app.models import user, skeptic

class Sighting:
    DB = "beltexam_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.sightingsdate = data['sightingsdate']
        self.sasquatchnumber = data['sasquatchnumber']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.author = None
        self.skeptics = []

    @classmethod
    def save(cls, data ):
        query = """
            INSERT INTO sightings ( location, description, sightingsdate, sasquatchnumber, created_at, updated_at, users_id ) 
            VALUES ( %(location)s, %(description)s, %(sightingsdate)s, %(sasquatchnumber)s, now(), now(), %(users_id)s  );
            """
        result = connectToMySQL(cls.DB).query_db( query, data )
        return result
    
    @classmethod
    def edit(cls, data):
        query = """
            UPDATE sightings SET location=%(location)s, description=%(description)s, sightingsdate=%(sightingsdate)s, sasquatchnumber=%(sasquatchnumber)s, updated_at=now() 
            WHERE sightings.id = %(id)s;
        """
        result = connectToMySQL(cls.DB).query_db( query, data )
        return result

    @classmethod
    def get_all_sightings(cls):
        query = "SELECT * from sightings JOIN users WHERE sightings.users_id = users.id"
        results = connectToMySQL(cls.DB).query_db(query)
        sightingslist = []
        for single_sighting in results:
            this_sighting = cls(single_sighting)
            this_sighting_author = {
                "id": single_sighting['users.id'],
                "first_name": single_sighting['first_name'],
                "last_name": single_sighting['last_name'],
                "email": single_sighting['email'],
                "password": single_sighting['password'],
                "created_at": single_sighting['users.created_at'],
                "updated_at": single_sighting['users.updated_at']
            }
            this_sighting.author = user.User(this_sighting_author)
            this_sighting_id = {
                "id": single_sighting['id']
            }
            skeptics = skeptic.Skeptic.get_all_skeptics(this_sighting_id)
            this_sighting.skeptics = skeptics
            sightingslist.append(this_sighting) 
        return sightingslist
    
    @classmethod
    def get_one_sighting(cls, id):
        query = "SELECT * FROM sightings JOIN users ON sightings.users_id = users.id WHERE sightings.id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})
        for sighting in results:
            this_sighting = cls(sighting)
            this_sighting.skeptics = []
            this_sighting_author = {
                "id": sighting['users.id'],
                "first_name": sighting['first_name'],
                "last_name": sighting['last_name'],
                "email": sighting['email'],
                "password": sighting['password'],
                "created_at": sighting['users.created_at'],
                "updated_at": sighting['users.updated_at']
            }
            this_sighting.author = user.User(this_sighting_author)
            this_sighting_id = {
                "id": sighting['id']
            }
            skeptics = skeptic.Skeptic.get_all_skeptics(this_sighting_id)
            this_sighting.skeptics = skeptics
            print(skeptics)
        return this_sighting
    
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM sightings
            WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,{"id": id})

    @staticmethod
    def validate_sighting(sighting):
        is_valid = True 
        if len(sighting['location']) < 1:
            flash("Location must be provided.", 'sighting')
            is_valid = False
        if len(sighting['description']) < 1:
            flash("Description of what happened must be provided.", 'sighting')
            is_valid = False
        if len(sighting['sightingsdate']) < 1:
            flash("Date of Sighting must be provided.", 'sighting')
            is_valid = False
        if int(sighting['sasquatchnumber']) <= 0:
            flash("Number of Sasquatches must be at least one.", 'sighting')
            is_valid = False
        return is_valid