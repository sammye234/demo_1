from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/CitizenApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.Text)
    contact_number = db.Column(db.String(15))
    profile_picture = db.Column(db.Text)
    password_hash = db.Column(db.Text, nullable=False)

@app.route('/profile', methods=['GET', 'POST', 'PUT'])
def manage_profile():
    if request.method == 'GET':
        user_id = request.args.get('id')
        user = UserProfile.query.get(user_id)
        if user:
            return jsonify({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "contact_number": user.contact_number,
                "profile_picture": user.profile_picture
            })
        return jsonify({"error": "User not found"}), 404

    elif request.method == 'POST':
        data = request.json
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = UserProfile(
            name=data['name'],
            email=data['email'],
            address=data.get('address', ''),
            contact_number=data.get('contact_number', ''),
            profile_picture=data.get('profile_picture', ''),
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User profile created successfully"})

    elif request.method == 'PUT':
        data = request.json
        user = UserProfile.query.get(data['id'])
        if user:
            user.name = data.get('name', user.name)
            user.address = data.get('address', user.address)
            user.contact_number = data.get('contact_number', user.contact_number)
            user.profile_picture = data.get('profile_picture', user.profile_picture)
            if 'password' in data:
                user.password_hash = generate_password_hash(data['password'], method='sha256')
            db.session.commit()
            return jsonify({"message": "User profile updated successfully"})
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=9090)
