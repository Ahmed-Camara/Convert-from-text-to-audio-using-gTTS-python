from flask import Flask,request,jsonify
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import shutil
import utils
from flask_cors import CORS
import common

app = Flask(__name__)
CORS(app)

def FlushRepository():
    folder = common.PATH_FOLDER

    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)

scheduler = BackgroundScheduler()
scheduler.add_job(func=FlushRepository, trigger="interval", seconds=20)
scheduler.start()


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: scheduler.shutdown())


@app.route("/convert", methods=['GET', 'POST'])
def convertFromTextToAudio():
    
    try:
        textFR = request.json['textFR']
        textEN = request.json['textEN']
        TicketNum = request.json['TicketNum']
        path = request.json['path']

        if textFR is not None and textEN is not None and TicketNum is not None:
            
            dataFR = utils.generateAudio(textFR,'fr',TicketNum,path)
            dataEN = utils.generateAudio(textEN,'en',TicketNum,path)

    except Exception as e:
        common.status = "0"
        common.ERROR_MSG = "Une erreur s'est produite, veuillez contacter l'administrateur :\n"
        
        return jsonify({
            "status":common.status,
            "message":common.ERROR_MSG+ str(e)
        })
    
    
    return jsonify({
        "data_french":dataFR,
        "data_english":dataEN
    })

if __name__ == "__main__":
    app.run(host=common.host,port=common.port, debug=True, threaded=True)