from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Enable CORS
CORS(app)

# Set up DB and migrations
db.init_app(app)
migrate = Migrate(app, db)

# ---------------------
# ROUTES
# ---------------------

# GET /messages - list all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages]), 200

# POST /messages - create a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    try:
        new_message = Message(
            body=data['body'],
            username=data['username']
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# PATCH /messages/<id> - update a message's body
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)

    if message:
        data = request.get_json()
        message.body = data.get('body', message.body)
        db.session.commit()
        return jsonify(message.to_dict()), 200
    else:
        return jsonify({'error': 'Message not found'}), 404


# DELETE /messages/<id> - delete a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)

    if message:
        db.session.delete(message)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Message not found'}), 404

# Run the app
if __name__ == '__main__':
    app.run(port=5555)
