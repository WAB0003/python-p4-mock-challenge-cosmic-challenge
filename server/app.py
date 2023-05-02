#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

#!SCIENTISTS
@app.route('/scientists', methods = ['GET', 'POST'])
def scientists():
    all_scientists = Scientist.query.all()
    
    if request.method == 'GET':
        scientist_list = [scientist.to_dict() for scientist in all_scientists]
        response = make_response( scientist_list, 200)              
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        try:
            new_scientist = Scientist(
                name=data.get('name'),
                field_of_study=data.get('field_of_study'), 
                avatar = data.get('avatar'),
            )
            db.session.add(new_scientist)
            db.session.commit()
            return new_scientist.to_dict()
        except ValueError:
            return {'error': '400: Validation error'}, 400
    
    
#!Scientists by ID
@app.route('/scientists/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def scientist_by_id(id):
    scientist= Scientist.query.filter(Scientist.id == id).first()
    
    if request.method == 'GET':
        if scientist:
            scientist_dict = scientist.to_dict()
            response = make_response(scientist_dict, 200)         
            return response
        else:
            return {"error": "404: Scientist not found"}, 404
        
    elif request.method == "PATCH":
        if scientist:
            try:
                data = request.get_json()
                
                for attr in data:
                    setattr(scientist, attr, data.get(attr))
                db.session.add(scientist)
                db.session.commit()
                
                scientist_dict = scientist.to_dict()
                
                response = make_response(scientist_dict, 200)
                
                return response
            except ValueError:
                return {'error': '400: Validation Error'}, 400
        return {"error": "404: Scientist not found"}, 404
    
    elif request.method == "DELETE":
        if scientist:
            db.session.delete(scientist)
            db.session.commit()
            response = make_response("",204)
            return response
            
        return {"error": "404: Scientist not found"}, 404
    
#!PLANETS
@app.route('/planets', methods = ['GET'])
def planets():
    all_planets = Planet.query.all()
    
    if request.method == 'GET':
        planet_list = [planet.to_dict(rules=('-missions',)) for planet in all_planets]
        response = make_response(planet_list, 200)              
        return response

#!MISSIONS
@app.route('/missions', methods = ['POST'])
def missions():      
    if request.method == 'POST':
        data = request.get_json()
        try:
            new_mission = Mission(
                name=data.get('name'),
                scientist_id=data.get('scientist_id'), 
                planet_id = data.get('planet_id'),
            )
            db.session.add(new_mission)
            db.session.commit()
            return new_mission.to_dict()
        except ValueError:
            return {'error': '400: Validation error'}, 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
