from flask import Flask
from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

app = Flask(__name__)

DB_HOST = '192.168.0.1'
DB_PORT = 9669
DB_USERNAME = 'root'
DB_PSSWD = 'nebula'
SCHEMA = 'csv'

def conn(_host, _port):
    # define a config
    config = Config()
    # init connection pool
    connection_pool = ConnectionPool()
    # if the given servers are ok, return true, else return false
    ok = connection_pool.init([(_host, _port)], config)
    return connection_pool
    
def request(_c_pool, _query, _username, _psswd):  
    with _c_pool.session_context(_username, _psswd) as session:
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
    c_pool = conn(DB_HOST, DB_PORT)
    return request(c_pool, query, DB_USERNAME, DB_PSSWD)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
