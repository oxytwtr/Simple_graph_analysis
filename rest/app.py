from flask import Flask
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

app = Flask(__name__)

HOST = '192.168.9.109'
PORT = 9669
USERNAME = 'root'
PSSWD = 'nebula'
SCHEMA = 'csv'

def conn(_host, _port):
    # define a config
    config = Config()
    # init connection pool
    connection_pool = ConnectionPool()
    # if the given servers are ok, return true, else return false
    ok = connection_pool.init([(_host, _port)], config)
    return connection_pool
    
def request(_c_pool, _query):  
    with _c_pool.session_context(USERNAME, PSSWD) as session:
        result = session.execute_json(_query)
    return result
   
#@app.route('/', methods=['GET'])
@app.route('/<fio>')
def get_tasks(fio):
    query_0 = f'USE {SCHEMA};\n\
              MATCH (m1:member)\n\
              WHERE id(m1) == "{fio}"\n\
              RETURN properties(m1) AS node_properties;' 
              
    query_1 = f'USE {SCHEMA};\n\
              MATCH (m1:member)-[r]-(m2:member)\n\
              WHERE id(m1) == "{fio}"\n\
              RETURN properties(m1) AS node_prop,\n\
              properties(r) AS rel_prop;'
              
    query = f'USE {SCHEMA};FETCH PROP ON * "{fio}" YIELD properties(vertex)'
    c_pool = conn(HOST, PORT)
    return request(c_pool, query)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
