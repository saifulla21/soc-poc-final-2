from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from os import getenv
import pymssql
import time
from random import randint



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False
socketio = SocketIO(app,engineio_logger=False,log_output=False,async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/test')
def test():
   return  db_connect()
    
    
# def intense_cpu():
#     x = 1
#     threshold = randint(1, 10)
#     start = int(time.time())
#     while True:
#         delta = int(time.time()) - start
#         if (delta > threshold):
#             break
#         x= x*x
#     return 'threshold : '+str(threshold)

def db_connect():
    server = '10.62.136.217'
    user = 'sa'
    password = 'Passw0rd'

    conn = pymssql.connect(server, user, password, "cas-sqldev-tenant-007")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sites where product_type = %s','XenDesktop')
    row = cursor.fetchone()
    str_my = ''
    while row:    
        str_my = str_my + row[0] + ' , '
        print("tenant_ID=%s, Name=%s" % (row[0], row[1]))
        row = cursor.fetchone()
    conn.close()
    return str_my

@socketio.on('myevent')
def test_message(message):
    resp = db_connect()
    emit('myresponse', {'data': message, 'resp': resp})
    
@socketio.on('chat message')
def test_message(message):
    emit('chat message', 'server response')

if __name__ == '__main__':
    socketio.run(app)
