#make a POST request
import requests, xml.etree.ElementTree as ET
port = 80

res = requests.get(f'http://localhost:{port}/MVoT')
print('GET response status from server:',res)
print('GET response data from server (last 2):')
# print last 2
root = ET.fromstring(res.text)
for child in root[-2:]: 
   print(ET.tostring(child).decode())



xml = """<?xml version='1.0'?>
    <MVoT>
      <anon_id>test-test-test-*</anon_id>
      <registration_date>1629393715.096357</registration_date>
      <last_timestamp>1629394315.096386</last_timestamp>
      <sdtt>0.1112444366039249</sdtt>
      <RFC>1.0</RFC>
      <TSLC>300.00001287460327</TSLC>
      <tx_time>0.17</tx_time>
      <comm_freq>0.0049999997595946</comm_freq>
      <certainty>0.0002321533514997</certainty>
      <avg_tx_time>0.131038961038961</avg_tx_time>
      <trust_score>0.0006344171455322</trust_score>
      <distrust_score>0.0</distrust_score>
      <total_msgs>3</total_msgs>
      <other_count>0</other_count>
      <alerts_count>0</alerts_count>
      <timeout_count>0</timeout_count>
      <count_expected_msgs>3</count_expected_msgs>
      <count_unexpected_msgs>0</count_unexpected_msgs>
   </MVoT>
"""
headers = {'Content-Type': 'application/xml'} # set what your server accepts
# print requests.post('http://httpbin.org/post', data=xml, headers=headers).text
res = requests.post(f'http://localhost:{port}/MVoT', data=xml, headers=headers)

print('POST response from server:',res)
print('POST response data from server:',res.text)



res = requests.get(f'http://localhost:{port}/MVoT')
print('GET response status from server:',res)
print('GET response data from server (last 2):')
# print last 2
root = ET.fromstring(res.text)
for child in root[-2:]: 
   print(ET.tostring(child).decode())