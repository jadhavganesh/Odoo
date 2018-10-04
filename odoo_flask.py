from flask import Flask,jsonify
from flask import request
from xmlrpc import client as xmlrpclib
 
app = Flask(__name__)
app.config['DEBUG']=True


@app.route('/login', methods = ['GET'])
def get_odoo_instance():
	models = {
		'odoo_instance' : None
	    }
	username = 'admin'
	password = 'admin'
	dbname = 'demo'
	port = '8069'
	host = 'localhost'
	sock_common = xmlrpclib.ServerProxy('http://' +host + ':' + port +'/xmlrpc/common')
	uid = sock_common.login(dbname, username, password)
	sock = xmlrpclib.ServerProxy('http://' +host + ':' +port +'/xmlrpc/object', allow_none=True)
	contact_ids = sock.execute(dbname, uid, password, 'res.users', 'search', [('id','=',1)])
	for contact_id in contact_ids:
		contact = sock.execute(dbname, uid, password, 'res.users', 'read', contact_id, [])
		print('Contact name: ',contact[0]['name'])
        
	return jsonify(contact[0])
 
app.run(host='0.0.0.0', port= 8090)
