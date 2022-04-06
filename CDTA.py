from flask import Flask, redirect, request, Response
import sqlite3, xml.etree.ElementTree as ET
from xml.dom import minidom
import traceback
tags = {
  'anon_id': str,
  'registration_date': float,
  'last_timestamp': float,
  'sdtt': float,
  'RFC': float,
  'TSLC': float,
  'tx_time': float,
  'comm_freq': float,
  'certainty': float,
  'avg_tx_time': float,
  'trust_score': float,
  'distrust_score': float,
  'total_msgs': int,
  'other_count': int,
  'alerts_count': int,
  'timeout_count': int,
  'count_expected_msgs': int,
  'count_unexpected_msgs': int
}
ordering = {v: i for i, v in enumerate(tags)}
#TODO: change to port 443 when self-signed certs are set up
port = 80 
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
def insert_to_db(conn, data):
    conn.execute(f"INSERT INTO MVoTs VALUES (NULL{', ?'*18})",
                tuple(data.values()) # becuase order is preserved, we can just pass the values
            )
    conn.commit()
    return
def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        # create an Element
        # class object
        child = ET.Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

def xml_to_dict(xml):
    result = {}
    root =  ET.fromstring(xml)
    assert root.tag == 'MVoT'
    assert len(root) == len(tags)
    for child in root:
        assert child.tag in tags
        result[child.tag] = tags[child.tag](child.text)
        if tags[child.tag] == float or tags[child.tag] == int:
            result[child.tag] = round(result[child.tag],5)
    # ensure data is sorted
    ordering = {v: i for i, v in enumerate(tags)}

    # dicts in python 3.7+ guarantee order is preserved
    result = dict(sorted(result.items(), key=lambda x: ordering[x[0]]))
    return result

def mvots_to_xml(mvots:list):
    root = ET.Element("MVoTs")
    root = ET.SubElement(root,"MVoTs")
    root.tag = 'MVoTs'
    for mvot in mvots:
        root.append(dict_to_xml('MVoT',dict(mvot)))
    return root

@app.route('/MVoT',methods=['POST','GET'])
def index():
    conn = get_db_connection()
    if request.method == 'GET':
        mvots = conn.execute('SELECT * FROM MVoTs').fetchall()
        
        # call create xml for all rows in db
        xml = ET.tostring(mvots_to_xml(mvots), method='xml')
        
        # print(minidom.parseString(xml).toprettyxml(indent="   "))

        response = Response(
            minidom.parseString(xml).toprettyxml(),
            mimetype='text/xml',
            status=200
            )
    else:
        # when request.method == 'POST' 
        # call extract mvot_xml
        xml = request.data
        status = 200
        try:
            data = xml_to_dict(xml)
            print('received: \n',xml.decode())
            insert_to_db(conn,data)
        except Exception as e:
            print('error: ',e)
            traceback.print_exc()
            status = 400 # error
            pass
        response = Response(status=status)
    
    conn.close()
    return response


if __name__ == '__main__':
   app.run(debug = True,port=port)