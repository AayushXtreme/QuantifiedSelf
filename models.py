from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(64), nullable=True)

class Tracker(db.Model):
    __tablename__ = 'tracker'
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    tracker_type = db.Column(db.String(20), nullable=False)
    settings = db.Column(db.Text, nullable=True)
    last_tracked = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    logs = db.relationship('TaskLog', backref='tracker', lazy="dynamic")
    
class TaskLog(db.Model):
    __tablename__ = 'tasklog'
    id = db.Column(db.String(20), primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    value = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text, nullable=True)
    tracker_id = db.Column(db.String(20), db.ForeignKey('tracker.id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    
def user_schema():
    return {"username": {"type": str, "regex": "^(?=.{3,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"}, 
            "password": {"type": str}}
    
def add_tracker_schema():
    return {
        "name": {"type": str, "regex": "^.{3,20}"},
        "description": {"type": str, "regex": "^.{0,120}"},
        "tracker_type": {"type": str, "allowed": ['numerical', 'choices', 'time', 'bool']},
        "settings": {"type": str, "regex": "^.{0,120}"}
    }
    
def edit_tracker_schema():
    return {
        "name": {"type": str, "regex": "^.{3,20}"},
        "description": {"type": str, "regex": "^.{0,120}"},
        "tracker_type": {"type": str, "allowed": ['numerical', 'choices', 'time', 'bool']},
        "settings": {"type": str, "regex": "^.{0,120}"}
    }
    
def add_log_schema():
    return {
        "timestamp": {"type": int},
        "value": {"type": str, "regex": "^.{1,50}"},
        "note": {"type": str, "regex": "^.{0,120}"}
    }
    
def edit_log_schema():
    return {
        "timestamp": {"type": int},
        "value": {"type": str, "regex": "^.{1,50}"},
        "note": {"type": str, "regex": "^.{0,120}"}
    }