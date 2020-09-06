from flask import Flask, jsonify, request, redirect, url_for, session, render_template, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret'

def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    session.pop('name', None)
    return "<h1>Hello, World!</h1>"

@app.route('/home', methods=['POST', 'GET'], defaults={'name': "Default"})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return render_template('home.html', name=name, display=False,
                           mylist=['one', 'two', 'three', 'four'],
                           listofdicts= [{'name' : 'Zach'}, {'name' : 'Joey'}], results=results)

@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'Notinthesession'
    return jsonify({'key': 'value', 'key2': [1, 2, 3], 'name': name})

@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return f'<h1>Hi {name}. You are from {location}!</h1>'

@app.route('/theform', methods=['GET', 'POST'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        # return f'<h1>Hello {name}. You are from {location}. You are submitted the form successfully!</h1>'
        return redirect(url_for('home', name=name, location=location))
'''
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']
    return f'<h1>Hello {name}. You are from {location}. You are submitted the form successfully!</h1>'
'''

@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']
    randomlist = data['randomlist']

    return jsonify({"result" : "success", "name" : name, "location" : location, "randomkeyinlist" : randomlist[1]})

@app.route('/viewresults')
def viewresults():
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h2>The ID is {0}. The name is {1}. The location is {2}.</h2>'.format(results[1]['id'], results[1]['name'], results[1]['location'])

if __name__ == '__main__':
    app.run(debug=True)