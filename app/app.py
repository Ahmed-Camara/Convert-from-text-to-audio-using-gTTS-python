from flask import Flask,request,jsonify
import utils
from flask_cors import CORS
import common as c
from waitress import serve

app = Flask(__name__)
CORS(app)


@app.route("/convert", methods=['GET', 'POST'])
def convertFromTextToAudio():
    
    try:
        textFR = request.json['textFR']
        textEN = request.json['textEN']
        TicketNum = request.json['TicketNum']
        path = request.json['path']
        address = request.json['address']

        c.address = address

        if textFR is None or len(textFR) == 0:
            c.dataENURL,c.dataEN = utils.generateAudio(textEN,'en',TicketNum,path)
            c.dataFRURL = c.dataFR = ""
        
        elif textEN is None or len(textEN) == 0:
            c.dataFRURL,c.dataFR = utils.generateAudio(textFR,'fr',TicketNum,path)
            c.dataENURL = c.dataEN = ""
            

        elif textFR is not None and textEN is not None and TicketNum is not None:
            
            c.dataFRURL,c.dataFR = utils.generateAudio(textFR,'fr',TicketNum,path)
            c.dataENURL,c.dataEN = utils.generateAudio(textEN,'en',TicketNum,path)

    except Exception as e:
        c.status = "0"
        c.ERROR_MSG = "Une erreur s'est produite, veuillez contacter l'administrateur :\n"

        return jsonify({
            "status":c.status,
            "message":c.ERROR_MSG+ str(e)
        })
    
    
    return jsonify({
        "data_french":c.dataFR,
        "data_english":c.dataEN,
        "data_french_url":c.dataFRURL,
        "data_english_url":c.dataENURL
    })
#serve(app,host=c.host,port=c.port,threads=1)
if __name__ == "__main__":
    app.run(host=c.host,port=c.port, debug=True, threaded=True)