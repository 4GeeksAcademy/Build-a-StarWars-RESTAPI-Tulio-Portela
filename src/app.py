import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Person, Planet, Favorite
from utils import generate_sitemap
from admin import setup_admin

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuração da base de dados
db_url = os.getenv("DATABASE_URL")
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
MIGRATE = Migrate(app, db)
CORS(app)
setup_admin(app)

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    response = {"message": str(error)}
    return jsonify(response), 400

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoints para Person
@app.route('/people', methods=['GET'])
def get_people():
    try:
        people = Person.query.all()
        if not people:
            app.logger.info("No people found")
        return jsonify([person.serialize() for person in people]), 200
    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"message": "Internal Server Error"}), 500

@app.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get(person_id)
    if person:
        return jsonify(person.serialize()), 200
    return jsonify({"message": "Person not found"}), 404

# Endpoints para Planet
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify(planet.serialize()), 200
    return jsonify({"message": "Planet not found"}), 404

# Endpoints para User
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID required"}), 400
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID required"}), 400

    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID required"}), 400

    favorite = Favorite(user_id=user_id, person_id=person_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID required"}), 400

    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite removed"}), 200
    return jsonify({"message": "Favorite not found"}), 404

@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID required"}), 400

    favorite = Favorite.query.filter_by(user_id=user_id, person_id=person_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite removed"}), 200
    return jsonify({"message": "Favorite not found"}), 404

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
