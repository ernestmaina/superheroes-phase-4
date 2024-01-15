#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower  # Import your models
from marshmallow import ValidationError  # Import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Routes
@app.route('/')
def home():
    return 'Flask is running'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.serialize() for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.serialize_with_powers())
    else:
        return jsonify({"error": "Hero not found"}), 404

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.serialize() for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.serialize())
    else:
        return jsonify({"error": "Power not found"}), 404
    
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        power_schema = PowerSchema()
        try:
            updated_data = power_schema.load(data)
        except ValidationError as err:
            return jsonify({'errors': err.messages}), 400
        power.description = updated_data['description']
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    else:
        return jsonify({'error': 'Power not found'}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        # Validate the incoming JSON data
        new_hero_power = {
            'hero_id': data['hero_id'],
            'power_id': data['power_id'],
            'strength': data['strength']
        }
    except KeyError:
        return jsonify({'error': 'Invalid data format'}), 400

    hero = Hero.query.get(new_hero_power['hero_id'])
    power = Power.query.get(new_hero_power['power_id'])

    if hero and power:
        hero_power = HeroPower(strength=new_hero_power['strength'], hero=hero, power=power)
        db.session.add(hero_power)
        db.session.commit()

        return jsonify({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': [{'id': power.id, 'name': power.name, 'description': power.description}
                       for power in hero.powers]
        })
    else:
        return jsonify({'error': 'Hero or Power not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5555)