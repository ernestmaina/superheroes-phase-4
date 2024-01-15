
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

hero_power_association = db.Table(
    'hero_power_association',
    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id')),
    db.Column('power_id', db.Integer, db.ForeignKey('power.id'))
)

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    powers = db.relationship('Power', secondary=hero_power_association, backref='heroes')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name
        }

    def serialize_with_powers(self):
        return {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
            'powers': [power.serialize() for power in self.powers]
        }
        
        
class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

    hero = db.relationship('Hero', backref=db.backref('hero_powers', lazy=True))
    power = db.relationship('Power', backref=db.backref('hero_powers', lazy=True))

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be one of: 'Strong', 'Weak', 'Average'")
        return value
