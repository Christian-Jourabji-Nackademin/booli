from flask_mysqldb import MySQL
from flask import Flask,render_template
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)


app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ocn217'
app.config['MYSQL_DB'] = 'account'

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
    cur.execute("SELECT * FROM account")
    fetchdata = cur.fetchall()
    cur.close
    return render_template('ready.html', data = fetchdata)



# /metrics endpint is alive and send prometheus metrics
#  
#
#


if __name__ == "__main__":
    app.run(debug=True)