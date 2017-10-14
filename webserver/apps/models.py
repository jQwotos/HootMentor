from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
    job = db.Column(db.String())
    skillHash = db.Column(db.String())
    val = db.Column(db.Float())


class Job(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    uuid = db.Column(db.String())
    title = db.Column(db.String())
    link = db.Column(db.String())
    proficiency = db.Column(db.String())
