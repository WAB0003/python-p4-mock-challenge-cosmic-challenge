from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #*Relationships
    missions = db.relationship('Mission', back_populates='planet')  
    #Throughrelationship 
    scientists = association_proxy('missions', 'scientist')
    
    # #Serialization rules
    serialize_rules = ('-missions.planet', '-scientists.planets','-created_at','-updated_at',)
    
   
    
    
    
class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id")) 
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id")) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #*Relationships
    planet = db.relationship('Planet', back_populates='missions') 
    scientist = db.relationship('Scientist', back_populates='missions') 
    
    # #Serialization rules
    serialize_rules = ('-created_at','-updated_at', '-planet.missions', '-scientist.missions')
    
    #!Validations
    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Must have name")
        return name
    
    @validates('scientist_id')
    def validates_name(self, key, scientist_id):
        if not scientist_id:
            raise ValueError("Must have scientist_id")
        return scientist_id
    
    @validates('planet_id')
    def validates_name(self, key, planet_id):
        if not planet_id:
            raise ValueError("Must have planet_id")
        return planet_id
    
    
    

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    field_of_study=db.Column(db.String, nullable=False)
    avatar=db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #*Relationships
    missions = db.relationship('Mission', back_populates='scientist')  
    #Throughrelationship 
    planets = association_proxy('missions', 'planet')
    
    #Serialization rules
    serialize_rules = ('-missions.scientist','-planets.scientists''-created_at','-updated_at',)
    
    # !Validations
    @validates('name')
    def validates_name(self, key, name):
        if not name:
            raise ValueError("Must have name")
        return name
    
    @validates('field_of_study')
    def validates_name(self, key, field_of_study):
        if not field_of_study:
            raise ValueError("Must have a field of study")
        return field_of_study
    
  
            
            
            
    
    
        
        
    
    
    
    



# add any models you may need. 