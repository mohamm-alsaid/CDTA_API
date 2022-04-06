import sqlite3
import pandas as pd
import numpy as np
from itertools import cycle

sql_fname = 'mvot_data/MVoTs_schema.sql'
mvots_fname = 'mvot_data/testingMM_1_SimOut.csv'
anon_ids = 'mvot_data/anonymized.csv'
sample_size = 10
# used to rename columns & used to seed the DB
keys = {
    'Actor':'actor',
    'trust score':'trust_score',
    'unexpected message count':'count_unexpected_msgs',
    'distrust score':'distrust_score',
    'certainty':'certainty',
    'average transit time':'avg_tx_time',
    'registration date':'registration_date',
    'communication frequency':'comm_freq',
    'expected message count':'count_expected_msgs',
    'alert count':'alerts_count',
    'other action count':'other_count', 
    'SD transit time':'sdtt',
    'relative factor of certainty':'RFC',
    'message transit time':'tx_time',
    'total message count':'total_msgs',
    'time since last communication':'TSLC',
    'time stamp':'last_timestamp',
    'timeout count':'timeout_count',
}
# read rename columns before seeding
records = pd.read_csv(mvots_fname)
print(records.columns)
records = records.rename(keys,axis='columns')[keys.values()]
ids = pd.read_csv(anon_ids)

sample_ids = ids.iloc[:sample_size]
sample_ids = sample_ids.apply(lambda x: ':'.join(x).replace(' ',''),axis='columns')
# round records
# records = records[list(keys.values())[1:]]
# records = records[records != 'actor'].apply(lambda x: round(x,5))
records['anon_id'] = '*:*:*:*' # add default IDs

connection = sqlite3.connect('database.db')


with open(sql_fname) as f:
    connection.executescript(f.read())

cur = connection.cursor()

for (i,mvot) in records.iloc[:sample_size*4].iterrows():
    print('inserting: ',tuple(mvot)) # exclude actor
    cur.execute(f"INSERT INTO MVoTs VALUES (NULL{', ?'*18})",
                mvot[['anon_id',
                'registration_date',
                'last_timestamp',
                'sdtt',
                'RFC',
                'TSLC',
                'tx_time',
                'comm_freq',
                'certainty',
                'avg_tx_time',
                'trust_score',
                'distrust_score',
                'total_msgs',
                'other_count',
                'alerts_count',
                'timeout_count',
                'count_expected_msgs',
                'count_unexpected_msgs'
                ]]
            )

connection.commit()
connection.close()