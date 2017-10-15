import logging
import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from fuzzywuzzy import fuzz

#import empathetic

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


class Position(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    noc_code = db.Column(db.Integer())
    group = db.Column(db.String())
    occupation = db.Column(db.String())
    automation_risk = db.Column(db.Float())
    average_income = db.Column(db.Integer())
    level_of_education = db.Column(db.String())


def searchNMatch(strPosition):
    return match(search(strPosition))


def search(strPosition):
    return Position.query.filter(
        Position.occupation == strPosition
    ).first()


def match(position):
    data = Position.query.filter(and_(
        Position.group == position.group,
    )).all()
    output = []
    for x in data:
        if fuzz.ratio(x.level_of_education, position.level_of_education) > 80:
            output.append(x)
    return output

def sortMatches(matches):
    return sorted(
        matches,
        key=lambda x: x.automation_risk,
        reverse=False
    )


@app.route('/chatbot', methods=['POST'])
def chatbot():
    return reply


@app.route('/job_recommender', methods=['POST'])
def job_recommender():
    data = request.form.get('response')
    matches = sortMatches(searchNMatch(data))
    output = ""
    for match in matches:
        output += match.occupation + ","
    output = output[:-1]
    return output


@app.route('/automation_percentage', methods=['POST'])
def automation_percentage():
    data = request.form.get('response')
    position = search(data)
    percentage = position.automation_risk()
    #return empathetic.generate(percentage)
