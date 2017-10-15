import logging
import json
from uuid import uuid4
import hashlib

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
# from webserver.apps.models import db, Job, Skill, JobSkill

#from chatbot.chatbot import chatbot
from scripts import skill_eliminator as se

app = Flask(__name__)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


class Skill(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    skillHash = db.Column(db.String())
    skillStr = db.Column(db.String())

class UserSkill(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_uuid = db.Column(db.String(), unique=True)
    skill = db.Column(db.String())


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_uuid = db.Column(
        db.String(),
        unique = True
    )
    username = db.Column(db.String())
    positionHash = db.Column(db.String())
    hashPassword = db.Column(db.String())


class JobSkill(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    jobHash = db.Column(db.String())
    skillHash = db.Column(db.String())
    val = db.Column(db.Float())


class Job(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String())
    title = db.Column(db.String())
    link = db.Column(db.String())
    proficiency = db.Column(db.String())
    noc_code = db.Column(db.String())


def _generate_token():
    token = str(uuid4())
    # Possible token generation here
    return token

data = (
    ['0012', '0013', '0014'],
    [[0, 0, 0, 1], [0, 1, 0 ,1], [0, 1, 1, 1]],
    [1,0,0,1],
[''])
'''
@app.route('/token', methods=['POST'])
def token():
    token = _generate_token()
    newUser = User(
        user_uuid = token,
        username = ,
    )
    return json.loads({'token': _generate_token})
'''
# Handles' the initial questions
@app.route('/questions', methods=['POST'])
def questions():
    if request.method == 'POST':
        return json.dumps({'response': 'I got %s' % request.form.get('response')})
    else:
        logging.debug('I received a non-post packet.')

@app.route('/response', methods=["POST"])
def response():
    if request.method == 'POST':
        return json.dumps({'response': 'I got %s' % request.form.get('response')})
    else:
        logging.debug('I received a non-post packet.')

@app.route('/survey', methods=['POST'])
def survey():
    if request.method == 'POST':
        data = json.request.form.get('response')
        return json.dumps({

        })
    else:
        logging.debug("I received a non-post packet on survey.")

@app.route('/job', methods=['POST'])
def job():
    if request.method == 'POST':
        jobName = str(request.form.get('data'))
        job = Job.query.filter_by(title=jobName).first()
        objSkills = JobSkill.query.filter_by(
            jobHash=hashlib.md5(job.title.encode()).hexdigest()
        ).all()
        skills = []
        for x in objSkills:
            if objSkills is None:
                print('MASSIVE ERROR!')
            else:
                skills.append(
                    Skill.query.filter_by(skillHash = x.skillHash).first().skillStr
                )
        udpatedSkills = [
            Skill.query.filter_by(
                skillHash = x.skillHash
            ).first().skillStr for x in objSkills
        ]
        print(skills)
        skills = se.eliminate(udpatedSkills, se._load_rel_skills())

        return json.dumps({
            'test': skills,
        })

if __name__ == "__main__":
        app.run()
