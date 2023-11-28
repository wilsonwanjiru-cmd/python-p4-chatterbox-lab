from flask import Flask, request, make_response, jsonify, json
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET','POST'])
def messages():

    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        # messages = [message.to_dict() for message in messages.query.all()]

        response = make_response(
            jsonify(messages),
            200
        )
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body = data["body"],
            username = data["username"]
        )

        db.session.add(new_message)
        db.session.commit()

        response = make_response(
            jsonify(new_message.to_dict()),
            201
        )
        return response


@app.route('/messages/<int:id>', methods=['PATCH','DELETE'])
def messages_by_id(id):
    update = Message.query.filter_by(id=id).first()


    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(update,attr,data[attr])

            db.session.add(update)
            db.session.commit()

            response = make_response(
                jsonify(update.to_dict()),
                200
            )
            return response
    # elif request.method == 'GET':
    elif request.method == 'DELETE':
        # update = Message.query.filter_by(id=id).first()
        db.session.delete(update)
        db.session.commit()

        response = make_response(
            jsonify(
                # update.to_dict()
                {
                "delete_successful" : True,
                "message": "Message deleted."
            }
            ),
            200
        )
        # response.headers["Content-Type"] = "application/json"
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
