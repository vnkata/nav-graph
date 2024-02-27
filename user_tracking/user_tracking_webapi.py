from flask import Flask, render_template
from flask import request
from flask import jsonify
from flask_cors import CORS,cross_origin
import sqlite3
import threading
lock = threading.Lock()

connection = sqlite3.connect("event_db.db", check_same_thread=False)
cursor = connection.cursor()
# cursor.execute("DROP TABLE IF EXISTS events")
cursor.execute("""CREATE TABLE IF NOT EXISTS events (timestamp TEXT, event TEXT, session TEXT,
        target_selector TEXT,
        target_attributes_text TEXT,
        target_attributes_value TEXT,
        target_attributes_tagName TEXT,
        target_attributes_id TEXT,
        target_attributes_name TEXT)""")

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    cursor.execute("SELECT session, timestamp, event, target_selector, target_attributes_tagName, target_attributes_text, target_attributes_id, target_attributes_value, target_attributes_name FROM events ")
    result = cursor.fetchall()
    print (f"results=", result)
    return render_template("index.html", result = result)

@app.route('/push_data/', methods = ['POST'])
def user():
    data = dict(request.form)
    print ("data=", data)
    if 'target[selector]' in data:
        new_data = {
            'timestamp': data['timestamp'],
            'event': data['event'],
            'session': data['session'],
            'target_selector': data['target[selector]'],
            'target_attributes_text': data.get('target[attributes][text]', None),
            'target_attributes_value': data.get('target[attributes][value]', None),
            'target_attributes_tagName':data.get('target[attributes][tagName]', None),
            'target_attributes_id':data.get('target[attributes][id]', None),
            'target_attributes_name': data.get('target[attributes][name]', None),
        }
        lock.acquire(True)
        cursor.execute(
            """INSERT INTO events (timestamp, event, session, target_selector, 
                target_attributes_text, 
                target_attributes_value,
                target_attributes_tagName,
                target_attributes_id,
                target_attributes_name)
                VALUES (:timestamp, :event, :session, :target_selector, :target_attributes_text,
                 :target_attributes_value,
                 :target_attributes_tagName,
                 :target_attributes_id,
                 :target_attributes_name);""", new_data)
        connection.commit()
        lock.release()
        return_data = {'message': 'Login sucessful'}
        print ("===="*10)
        print ("\n\nnew_data=", new_data)
        return jsonify(return_data), 201
    else:
        print ('no target found....')
        return jsonify({}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=6200)