from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reminders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Reminder model
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Reminder({self.title}, {self.date_time})'

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    reminders = Reminder.query.all()
    return render_template('index.html', reminders=reminders)

@app.route('/add_reminder', methods=['POST'])
def add_reminder():
    title = request.form['title']
    date_time_str = request.form['datetime']
    date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')

    reminder = Reminder(title=title, date_time=date_time)
    db.session.add(reminder)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

