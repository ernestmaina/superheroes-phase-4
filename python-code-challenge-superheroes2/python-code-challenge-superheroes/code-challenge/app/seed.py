from flask import Flask
import random
from models import db, Power, Hero, HeroPower
from app import app
from faker import Faker


with app.app_context():
    
    db.drop_all()
    db.create_all()
    
    fake = Faker()

    print("🦸‍♀️ Seeding powers...")
    powers = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]
    for power_data in powers:
        power = Power(**power_data)
        db.session.add(power)

    print("🦸‍♀️ Seeding heroes...")
    heroes = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"},
        {"name": "Ernest Kamau", "super_name": "Mr.Maina"}
    ]
    for hero_data in heroes:
        hero = Hero(**hero_data)
        db.session.add(hero)

    print("🦸‍♀️ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]
    for hero in Hero.query.all():
        for _ in range(random.randint(1, 3)):
            power = Power.query.order_by(db.func.random()).first()
            hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=random.choice(strengths))
            db.session.add(hero_power)

    db.session.commit()
    print("🦸‍♀️ Done seeding!")

