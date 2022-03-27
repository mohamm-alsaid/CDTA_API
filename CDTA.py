from flask import Flask, redirect, request
import sqlite3
from dict2xml import dict2xml

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def mvots_to_xml(mvots:list):
    for mvot in mvots:
        print(dict2xml(dict(mvot)))

@app.route('/MVoT',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        # call extract mvot_xml
        print('post request')
        return 'post'
        pass
    elif request.method == 'GET':
        # call create xml for all rows in db
        conn = get_db_connection()
        conn = get_db_connection()
        mvots = conn.execute('SELECT * FROM MVoTs').fetchall()
        conn.close()
        
        mvots_to_xml(mvots)
        return 'mvots'
    return 'error!'


if __name__ == '__main__':
   app.run(debug = True)