from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from functools import wraps
from config import Config
from models import *
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config())
db.init_app(app)
sess = Session()
sess.init_app(app)

with app.app_context():
    db.create_all()

import helpers

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("uid"):
            return redirect(url_for("login"))    
        return view(*args, **kwargs)
    return wrapped_view

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            is_validated, message = helpers.are_params_valid(request.json, user_schema())
            if not is_validated:
                return {"success": False, "message": message}
            username = request.json['username']
            password = request.json['password'] 
            user_data = User.query.get(username)
            password = helpers.encode_password(password) if password else None
            if user_data is None:
                user_data = User(username=username, password=password)
                db.session.add(user_data)
                db.session.commit()
            elif user_data.password != password:
                return {"success": False, "message": "Password doesn't match"}
            session["uid"] = username
            return {"success": True, "message": ""}
        except Exception:
            message = "Some error occured"
            app.logger.exception(message)
            return {"success": False, "message": message}
    else:
        return render_template('login.html')
    
    
@app.route("/dashboard", methods=["GET"])
@app.route("/", methods=["GET"])
@login_required
def dashboard():
    uid = session.get("uid")
    trackers = Tracker.query.filter_by(user_id=uid).order_by(Tracker.last_tracked.desc()).all()
    return render_template("dashboard.html", response={"uid": uid, "trackers": trackers}) 


@app.route("/logout")
@login_required
def logout():
    session["uid"] = None
    return redirect(url_for("login"))


@app.route("/create_tracker", methods=["GET", "POST"])
@app.route("/edit_tracker", methods=["GET", "POST"])
@login_required
def upsert_tracker():
    uid = session.get("uid")
    tracker_id = request.args.get('tracker_id')
    tracker_info = Tracker.query.filter(Tracker.user_id == uid, Tracker.id == tracker_id).first() if tracker_id else None
    if request.method == 'POST':
        try:
            schema = edit_tracker_schema() if tracker_info else add_tracker_schema()
            is_validated, message = helpers.are_params_valid(request.json, schema)
            if not is_validated:
                return {"success": False, "message": message}
            if not tracker_info:
                id_ = 'tracker_' + helpers.get_random_id()
                tracker_info = Tracker(id=id_, user_id=uid, name=request.json['name'], description=request.json['description'], tracker_type=request.json['tracker_type'], settings=request.json['settings'] if request.json['tracker_type'] == 'choices' else None, last_tracked=None)
                db.session.add(tracker_info)
            else:
                tracker_info.name = request.json['name']
                tracker_info.description = request.json['description']
                tracker_info.tracker_type = request.json['tracker_type']
                tracker_info.settings = request.json['settings'] if request.json['tracker_type'] == 'choices' else None
            db.session.commit()
            return {"success": True, "message": ""}
        except Exception:
            message = "Some error occured"
            app.logger.exception(message)
            return {"success": False, "message": message}
    else:
        return render_template("add_tracker.html", response={"uid": uid, "tracker_info": tracker_info})


@app.route("/remove_tracker", methods=["GET"])
@login_required
def remove_tracker():
    uid = session.get("uid")
    tracker_id = request.args.get('tracker_id')
    try:
        tracker = Tracker.query.filter(Tracker.user_id == uid, Tracker.id == tracker_id).first()
        db.session.delete(tracker)
        db.session.commit()
    except Exception:
        message = 'Some error occured'
        app.logger.exception(message)
    return redirect(url_for("dashboard"))


@app.route("/tracker_info")
@login_required
def tracker_info():
    uid = session.get("uid")
    tracker_id = request.args.get('tracker_id')
    tracker_info = Tracker.query.filter(Tracker.user_id == uid, Tracker.id == tracker_id).first()
    return render_template("tracker_info.html", response={"uid": uid, "tracker_info": tracker_info})


@app.route("/create_log", methods=["GET", "POST"])
@app.route("/edit_log", methods=["GET", "POST"])
@login_required
def upsert_log():
    uid = session.get("uid")    
    tracker_id = request.args.get("tracker_id")
    log_id = request.args.get("log_id")
    tracker_info = Tracker.query.filter(Tracker.user_id == uid, Tracker.id == tracker_id).first() 
    log_info = TaskLog.query.filter(TaskLog.user_id == uid, TaskLog.id == log_id).first() if log_id else None
    if request.method == 'POST':
        try:
            schema = edit_log_schema() if log_info else add_log_schema()
            is_validated, message = helpers.are_params_valid(request.json, schema)
            if not is_validated:
                return {"success": False, "message": message}
            if not log_info:
                id_ = 'log_' + helpers.get_random_id()
                log_info = TaskLog(id=id_, user_id=uid, tracker_id=tracker_id, timestamp=request.json['timestamp'], value=request.json['value'], note=request.json['note'])
                db.session.add(log_info)
            else:
                log_info.timestamp = request.json['timestamp']
                log_info.value = request.json['value']
                log_info.note = request.json['note']
            db.session.flush()
            last_tracked_log = TaskLog.query.filter(TaskLog.user_id == uid, TaskLog.id == log_info.id).order_by(TaskLog.timestamp.desc()).first()
            tracker_info.last_tracked = last_tracked_log.timestamp
            db.session.commit()
            return {"success": True, "message": ""}
        except Exception:
            message = "Some error occured"
            app.logger.exception(message)
            return {"success": False, "message": message}
    else:
        return render_template("add_log.html", response={"uid": uid, "tracker_info": tracker_info, "log_info": log_info})
    
    
@app.route("/remove_log", methods=["GET"])
@login_required
def remove_log():
    uid = session.get("uid")  
    tracker_id = request.args.get("tracker_id")  
    log_id = request.args.get("log_id")
    try:
        tracker_info = Tracker.query.filter(Tracker.user_id == uid, Tracker.id == tracker_id).first()
        log = TaskLog.query.filter(TaskLog.user_id == uid, TaskLog.id == log_id).first()
        db.session.delete(log)
        db.session.flush()
        last_tracked_log = TaskLog.query.filter(TaskLog.user_id == uid, TaskLog.id == log_id).order_by(TaskLog.timestamp.desc()).first()
        tracker_info.last_tracked = last_tracked_log.timestamp if last_tracked_log else None 
        db.session.commit()
    except Exception:
        message = 'Some error occured'
        app.logger.exception(message)
    return redirect(url_for('tracker_info', tracker_id=tracker_id))
        
@app.template_filter()
def from_timestamp(val):
    timestamp = int(int(val)/1000)
    return str(datetime.fromtimestamp(timestamp))

if __name__ == '__main__':
    app.run(port="5000")