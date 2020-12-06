from flask import Flask, render_template, url_for, request, jsonify, make_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

