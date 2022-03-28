import unittest
import requests, xml.etree.ElementTree as ET
from uuid import uuid4
from CDTA import *

port = 80
url = f'http://localhost:{port}/MVoT'
class TestEndpoints(unittest.TestCase):

    def test_get(self):
        print('Tesing GET method for endpoint: /MVoT')

        res = requests.get(f'http://localhost:{port}/MVoT')

        self.assertEqual(res.status_code,200)        
        root = ET.fromstring(res.text)    
        self.assertTrue(root.tag=='MVoTs')
        self.assertNotEqual(len(root),0)

        for child in root: 
            self.assertTrue(child.tag == 'MVoT')
            for e in child[1:]:
                self.assertTrue(e.tag in tags.keys())
                # cast value
                val = tags[e.tag](e.text)
                self.assertIs(type(val),tags[e.tag])
        return
    
    def test_post(self):
        print('Tesing POST method for endpoint: /MVoT')

        res = requests.get(url)
        self.assertEqual(res.status_code,200)
        
        root = ET.fromstring(res.text)    
        self.assertTrue(root.tag=='MVoTs')
        self.assertNotEqual(len(root),0)
        # grab last element
        element = root[-1]
        # remove mvot_id
        element.remove(element.find('mvot_id'))

        string = ET.tostring(element)

        new = ET.fromstring(string)

        self.assertEqual(new.find('anon_id').text,element.find('anon_id').text)

        # update new record before testing POST
        new.find('anon_id').text = str(uuid4())
        self.assertNotEqual(new.find('anon_id').text,element.find('anon_id').text)

        # post it 
        headers = {'Content-Type': 'application/xml'}
        res = requests.post(url,data=ET.tostring(new,encoding='utf8'),headers=headers)
        self.assertEqual(res.status_code,200)

        # get new records and check
        res = requests.get(url)
        self.assertEqual(res.status_code,200)

        root = ET.fromstring(res.text)
        returned = root[-1]
        # remove mvot_id
        returned.remove(returned.find('mvot_id'))

        # assert returned value (when convert) is equal to the new value not the elem value
        self.assertEqual(ET.tostring(new),ET.tostring(returned)[:-1])
        prev = root[-2]
        prev.remove(prev.find('mvot_id'))
        self.assertEqual(ET.tostring(element),ET.tostring(prev)[:-1])



        
                
        return
   
   
if __name__ == '__main__':
    unittest.main()