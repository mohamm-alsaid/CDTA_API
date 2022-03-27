from flask import Flask, redirect, request, Response
import sqlite3, xml.etree.ElementTree as ET
from xml.dom import minidom

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        # create an Element
        # class object
        child = ET.Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

def mvots_to_xml(mvots:list):
    root = ET.Element("MVoTs")
    root = ET.SubElement(root,"MVoTs")
    root.tag = 'MVoTs'
    for mvot in mvots[:10]:
        root.append(dict_to_xml('MVoT',dict(mvot)))

    return root

@app.route('/MVoT',methods=['POST','GET'])
def index():
    conn = get_db_connection()
    if request.method == 'GET':
        mvots = conn.execute('SELECT * FROM MVoTs').fetchall()
        
        # call create xml for all rows in db
        xml = ET.tostring(mvots_to_xml(mvots),encoding='unicode',method='xml')
        
        print(minidom.parseString(xml).toprettyxml(indent="   "))

        response = Response(minidom.parseString(xml).toprettyxml(indent="   "),mimetype='text/xml')
    else:
        # when request.method == 'POST' 
        # call extract mvot_xml
        print('post request')
        response = ''
    
    conn.close()
    return response


if __name__ == '__main__':
   app.run(debug = True)