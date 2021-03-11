from flask_mysqldb import MySQL
from flask import Flask,render_template,request
from prometheus_flask_exporter import PrometheusMetrics
import os
import urllib.request


app = Flask(__name__)
metrics = PrometheusMetrics(app)

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DATABASE']


mysql = MySQL(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'

#
# This is the check to keep the pod alive
# if this fails k8s will restart the pod
@metrics.do_not_track()
@app.route('/health')
def health():
    return  "alright"

#
# This is the check that lets the pod accepts trafffic
# if this fails k8s will not send any more traffic to this pod
@metrics.do_not_track()
@app.route('/ready')
def ready():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM acc")
    fetchdata = cur.fetchall()
    cur.close
    return render_template('ready.html', data = fetchdata)




@app.route('/status/<url>')
def status(url):
    host = request.args.get('host')
    status = urllib.request.urlopen(url).getcode()
    if status == 200 :
        print('We are all good')
    else:
        print("Site is down")

    return '''
              <h1>The website value is: {}'''.format(host, status)




if __name__ == "__main__":
    app.run(debug=True)
