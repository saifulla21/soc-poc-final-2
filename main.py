from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from os import getenv
import pymssql
import time
import logging
from random import randint


logging.basicConfig(filename='soc-poc.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False
socketio = SocketIO(app,engineio_logger=False,log_output=False,async_mode='eventlet')

@app.route('/')
def index():
    logging.info('rendering index page')
    return render_template('index.html')
    
@app.route('/test')
def test():
   logging.info('running intense cpu operation')
   return  intense_cpu()
    
    
def intense_cpu():
    x = 1
    threshold = randint(1, 10)
    logging.debug('threshold value', str(threshold))
    start = int(time.time())
    while True:
        delta = int(time.time()) - start
        if (delta > threshold):
            break
        x= x*x
    return 'threshold : '+str(threshold)

def db_connect():
    logging.info('connecting to database')
    conn = pymssql.connect("10.62.136.217", "sa", "Passw0rd", "cas-sqldev-tenant-007")
#     conn = pyodbc.connect(r'DRIVER={SQL Server};SERVER=10.62.136.217;DATABASE=cas-sqldev-tenant-007;UID=sa;PWD=Passw0rd')
    cursor = conn.cursor()
    logging.info('connected to database')
    cursor.execute('SELECT * FROM sites where product_type = %s','XenDesktop')
   
    str_my = ''
    for row in cursor.fetchall():
        str_my = str_my + row[0]
    conn.close()
    return str_my

@socketio.on('myevent')
def test_message(message):
    logging.info('socket request received on myevent'+request.headers.get('Authorization'))
    try:
        resp = db_connect()
        emit('myresponse', {'data': message, 'resp': resp})
        socketio.sleep(0)
    except Exception as e:
        logging.exception(e)
        emit('myresponse', {'data': message, 'resp': 'error'})
        socketio.sleep(0)
    
@socketio.on('chat message')
def test_message(message):
    logging.info('socket request received on chatmessage')
    emit('chat message', 'server response')

if __name__ == '__main__':
    socketio.run(app)
