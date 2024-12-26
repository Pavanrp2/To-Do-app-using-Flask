from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tittle = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = True)
    completed = db.Column(db.Boolean, default = False)
    
    def Tasks_details(self):
       return {
           "id" : self.id,
           "tittle" : self.tittle,
           "description" : self.description,
           "completed" : self.completed
           }