from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from os import getenv
import pymssql


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False
socketio = SocketIO(app,engineio_logger=False,log_output=False,async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/test')
def test():
    server = 'cas-sqldb-dev.database.windows.net'
    user = 'casroot'
    password = 'db123$%^'

    conn = pymssql.connect(server, user, password, "cas-sqldev-tenant-44")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sites where product_type = %s','XenDesktop')
    row = cursor.fetchone()
    str_my = ''
    while row:    
        str_my = str_my + row[0] + ' , '
        print("tenant_ID=%s, Name=%s" % (row[0], row[1]))
        row = cursor.fetchone()
    print str_my
    conn.close()
    return str_my

@socketio.on('myevent')
def test_message(message):
    emit('myresponse', {'data': message})
    
@socketio.on('chat message')
def test_message(message):
    emit('chat message', 'server response')

if __name__ == '__main__':
    socketio.run(app)
