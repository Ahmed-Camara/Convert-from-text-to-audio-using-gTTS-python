from flask import Flask,request,jsonify
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import shutil
import utils

app = Flask(__name__)

def FlushRepository():
    folder = 'C:/AUDIO'
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)

scheduler = BackgroundScheduler()
scheduler.add_job(func=FlushRepository, trigger="interval", hours=23)
scheduler.start()


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: scheduler.shutdown())


@app.route("/convert", methods=['GET', 'POST'])
def convertFromTextToAudio():
    
    try:
        textFR = request.json['textFR']
        textEN = request.json['textEN']
        TicketNum = request.json['TicketNum']

        if textFR is not None and textEN is not None and TicketNum is not None:
            print("Not none")
            dataFR = utils.generateAudio(textFR,'fr',TicketNum)
            dataEN = utils.generateAudio(textEN,'en',TicketNum)

    except Exception as e:
        return jsonify({
            "status":"0",
            "message":"Une erreur s'est produite, veuillez contacter l'administrateur :\n"+ str(e)
        })
    

    return jsonify({
        "data_french":dataFR,
        "data_english":dataEN
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True, threaded=False)