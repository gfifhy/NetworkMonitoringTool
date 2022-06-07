import win32api
from flask import *
from NETWORKING import *

app = Flask(__name__)



@app.route('/')
def overview():
    return render_template('index.html')


@app.route('/update_hostLists')
def updateHostLists():
    network = "192.168.1.1/24"
    upHosts = upHostsList(network)
    writeJSON("hostList.json", upHosts)
    return redirect('cping')


@app.route('/update_ping', methods=['POST'])
def updatePing():
    upHosts = readJSON("hostList.json")
    pingInfo = pingList(upHosts)
    return jsonify('', render_template('ping_result_model.html', x=pingInfo, hosts = upHosts))


@app.route('/cping')
def cping():
    return render_template('cping.html')

if __name__ == "__main__":
    app.run(debug=True)