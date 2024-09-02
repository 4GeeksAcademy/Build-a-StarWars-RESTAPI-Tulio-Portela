from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)
    person_favorites = db.relationship('Favorite', back_populates='user_relationship')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    person_by=db.relationship("Favorite",back_populates="person_relationship")

    def __repr__(self):
        return f'<Person {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_relationship = db.relationship('User', back_populates='person_favorites')
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person_relationship = db.relationship('Person', back_populates='person_by')

    def __repr__(self):
        return f'<Favorite user_id={self.user_id} person_id={self.person_id}'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "person_id": self.person_id,
        }
