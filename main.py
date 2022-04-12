from flask_restful import Api
from datetime import date
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Message(db.Model):
    sender = db.Column(db.String)
    receiver = db.Column(db.String(50))
    message = db.Column(db.String(200))
    subject = db.Column(db.String(80))
    creation_date = db.Column(db.Integer)
    is_Read = db.Column(db.String)
    column_not_exist = db.Column(db.Integer, primary_key=True)

    def __init__(self, sender, receiver, message, subject):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.subject = subject
        self.creation_date = date.today().strftime("%d/%m/%Y")
        self.is_Read = "False"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))


@app.route('/newMessage', methods=['POST'])
def newMessage():
    sender = request.json['sender']
    receiver = request.json['receiver']
    message = request.json['message']
    subject = request.json['subject']

    new_massage = Message(sender, receiver, message, subject)

    db.session.add(new_massage)
    db.session.commit()

    return jsonify({'message': 'Message received!'})


@app.route('/all/<sender>', methods=['GET'])
def all(sender):
    messages = Message.query.filter_by(sender=sender).all()

    output = []

    for message in messages:
        message_data = create_msg(message)
        output.append(message_data)

    return jsonify({'all messages': output})


@app.route('/all_unread/<sender>', methods=['GET'])
def all_unread(sender):
    messages = Message.query.filter_by(sender=sender, is_Read='False').all()
    output = []

    for message in messages:
        message_data = create_msg(message)
        output.append(message_data)

    return jsonify({'all messages': output})


@app.route('/one_msg/<user>', methods=['GET'])
def read_msg(user):
    message = Message.query.filter_by(sender=user, is_Read='False').first()
    if not message:
        return jsonify({'message': 'No message found!'})
    message_data = create_msg(message)

    return jsonify({'message for you:': message_data})


@app.route('/delete_owner/<user>', methods=['DELETE'])
def delete_owner(user):
    message = Message.query.filter_by(sender=user).first()

    if not message:
        return jsonify({'message': 'No message found!'})

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'one message deleted!'})


@app.route('/delete_receiver/<user>', methods=['DELETE'])
def delete_receive(user):
    message = Message.query.filter_by(receiver=user).first()

    if not message:
        return jsonify({'message': 'No message found!'})

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'one message deleted!'})


def create_msg(message):
    message_data = {}
    message_data['sender'] = message.sender
    message_data['receiver'] = message.receiver
    message_data['message'] = message.message
    message_data['subject'] = message.subject
    message_data['creation_date'] = message.creation_date

    return message_data


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5000)
