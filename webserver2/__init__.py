import logging
import json

from random import randint

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from fuzzywuzzy import fuzz

from webserver2 import empathetic
from api_chatbot.chatbot import Chatbot

cb = Chatbot()
# cb.main('--test ['{}']')
# cb.main('Daemon')
# cb.main(['--modelTag', 'server', '--test', 'daemon', '--rootDir', chatbotPath])

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
        print("The ratio for %s and %s is %s" % (pos.occupation.lower(), strPosition.lower(), str(ratio)))
        if strPosition.lower() in pos.occupation.lower():
            return pos
        if ((ratio > 45) and (result is None or ratio > result.get('ratio')) or strPosition.lower() in (pos.occupation.lower())):
            result = {
                'ratio': ratio,
                'obj': pos
            }
    if result is not None: print(result.get('obj').occupation)
    return result.get('obj') if result is not None else None

def fuzzySearchNMatch(strPosition):
    return match(fuzzySearch(strPosition))


def search(strPosition):
    return Position.query.filter(
        Position.occupation == strPosition
    ).first()


def match(position):
    if position is not None:
        # Position is from database
        # position is the user's current job
        return Position.query.filter(and_(
            Position.group == position.group,
            Position.level_of_education == position.level_of_education,
            Position.occupation != position.occupation,
            Position.automation_risk < position.automation_risk,
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

def getSalary(position):
    return position.average_income


def parse(query):
    matching_pharses = [{
        'phrase': '{{SALARY}}',
        'function': getSalary,
    }]
    output = query
    position_pat = r'\^(.*)\^'

    positionRe = re.findall(position_pat, query)

    if len(positionRe) > 0:
        position = positionRe[0]
        databasePosition = fuzzySearch(position)

        if databasePosition is not None:
            for phrase in matching_phrases:
                output.replace(phrase.get('phrase'), phrase.get('function')(databasePosition))
            return output
    return cb.speak("This is a bad phrase.")

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.form.get('response')
    #print(data)
    #return cb.daemonPredict(str(data))
    reply = cb.speak(data)

    return cb.speak(data)

def random_job():
    data = Position.query.order_by(Position.automation_risk).limit(10).all()
    return data[randint(0, len(data) - 1)]


@app.route('/job_recommender', methods=['POST'])
def job_recommender():
    data = request.form.get('response')
    original = fuzzySearch(data)
    matches = sortMatches(match(original))
    if matches is not None:
        # If the person's job is in the database
        # and can be matched to other jobs then
        # we reply back with other jobs.
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
        job = random_job().occupation
        return json.dumps({
            'jobs':[job],
            'sentences': ["I can say that %s has an extremly low chance of automation, if your interested in a different career."
            % job],
        })


@app.route('/automation_percentage', methods=['POST'])
def automation_percentage():
    data = request.form.get('response')
    position = fuzzySearch(data)
    if position is not None:
        percentage = position.automation_risk
        return empathetic.generate(percentage)
    else:
        return("Sadly I can't seem to find your job.")
