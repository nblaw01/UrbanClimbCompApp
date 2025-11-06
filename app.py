from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime
import os


app = Flask(__name__)


DB_URL = os.getenv("DATABASE_URL", "sqlite:///scoring.db")
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


NUM_CLIMBS = int(os.getenv("NUM_CLIMBS", 10)) # default to 10, can override with env var


class Competitor(db.Model):
id = db.Column(db.Integer, primary_key=True) # competitor number
created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Score(db.Model):
__tablename__ = "scores"
id = db.Column(db.Integer, primary_key=True)
competitor_id = db.Column(db.Integer, db.ForeignKey("competitor.id"), nullable=False)
climb_number = db.Column(db.Integer, nullable=False)
attempts = db.Column(db.Integer, nullable=False, default=0)
topped = db.Column(db.Boolean, nullable=False, default=False)
updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


__table_args__ = (UniqueConstraint("competitor_id", "climb_number", name="uq_competitor_climb"),)


competitor = db.relationship("Competitor", backref=db.backref("scores", lazy=True))


@app.before_first_request
def create_tables():
db.create_all()


@app.route("/")
def index():
return render_template("index.html")


@app.route("/competitor", methods=["POST"]) # form posts competitor number
def enter_competitor():
app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))