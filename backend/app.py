# backend/api/app.py
import os
from flask import Flask, flash, redirect, jsonify
from worker.tasks import add

app = Flask(__name__)
app.secret_key = os.getenv('CELERY_BROKER_URL', "super-secret")

@app.route('/')
def main():
    return jsonify('{message: "main!"}')

@app.route('/add/<int:x>/<int:y>')
def add_inputs(x, y):
    x = int(x or 0)
    y = int(y or 0)
    add.delay(x, y)
    flash("Your addition job has been submitted.")
    return redirect('/')

if __name__ == '__main__':
    app.run(app)
