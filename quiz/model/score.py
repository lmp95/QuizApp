from quiz import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100))
    score = db.Column(db.Integer)
    module = db.Column(db.String(1000))
