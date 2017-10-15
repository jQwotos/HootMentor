import logging
import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from fuzzywuzzy import fuzz

from webserver2 import empathetic
from chatbot.chatbot import Chatbot

chatbot = Chatbot()

app = Flask(__name__)
db = SQLAlchemy(app)

# chatbot =

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


def fuzzySearch(strPosition):
    positions = Position.query.all()
    result = None
    for pos in positions:
        ratio = fuzz.ratio(pos.occupation, strPosition)
        if (ratio > 85) and (result is None or ratio > result.get('ration')):
            result = {
                'ratio': ratio,
                'obj': pos
            }
    return result.get('obj') if result is not None else None

def fuzzySearchNMatch(strPosition):
    return match(fuzzySearch(strPosition))


def search(strPosition):
    return Position.query.filter(
        Position.occupation == strPosition
    ).first()


def match(position):
    if position is not None:
        return Position.query.filter(and_(
            Position.group == position.group,
            Position.level_of_education == position.level_of_education,
            Position.occupation != position.occupation,
        )).all()
    else:
        return None


def sortMatches(matches):
    if matches is not None:
        return sorted(
            matches,
            key=lambda x: x.automation_risk,
            reverse=False
        )
    else:
        return None


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.form.get('response')
    return chatbot.speak(data)


@app.route('/job_recommender', methods=['POST'])
def job_recommender():
    data = request.form.get('response')
    original = fuzzySearch(data)
    matches = sortMatches(match(original))
    if matches is not None:
        # If the person's job is in the database
        # and can be matched to other jobs then
        # we reply back with other jobs.
        '''
        output = ""
        for match in matches:
            output += match.occupation + ","
        output = output[:-1]
        return output
        '''
        output = {
            'jobs':[],
            'sentences':[],
        }
        for m in matches:
            output['jobs'].append(m.occupation)
            output['sentences'].append(empathetic.job_phrase(m, original))
        return json.dumps(output)
    else:
        # Otherwise we just
        # give them a random job
        return json.dumps({
            'jobs':[],
            'sentences': ["Sorry, I couldn't find you an amazing match to your current job."]
        })


@app.route('/automation_percentage', methods=['POST'])
def automation_percentage():
    data = request.form.get('response')
    position = search(data)
    percentage = position.automation_risk()
    #return empathetic.generate(percentage)
