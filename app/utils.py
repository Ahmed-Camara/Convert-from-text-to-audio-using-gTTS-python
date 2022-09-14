from email import header
from gtts import gTTS
import os.path
from os import path
import os
import base64
import json
from flask import jsonify
def writeToFile(files,textFiles):
    with open(files, "rb") as f1,open(textFiles, "w") as f2:
        encoded_f1 = base64.b64encode(f1.read())
        f2.write("data:audio/mp4;base64,")
        f2.write(str(encoded_f1))
    

def readFromFile(files):
    text_file = open(files, "r")
    data = text_file.read()
    text_file.close()
    return data


def generateAudio(text,lang,ticket,paths="C:/AUDIO"):
    if not os.path.exists(paths):
        os.makedirs(paths)
    
    AudioFiles = paths+"/audio_"+lang+"_"+ticket+".mp4"
    TxtFiles = paths+"/base64_"+lang+"_"+ticket+".txt"

    print(TxtFiles)
    textSpeechFR = gTTS(text=text, lang=lang, slow=False)
    textSpeechFR.save(AudioFiles)

    
    writeToFile(AudioFiles,TxtFiles)
    data = readFromFile(TxtFiles)
    value = {
        "headers":"data:audio/mp4;base64,",
        "data_"+lang:data
    }
   # writeToFile("C:/AUDIO/audio.mp3","C:/AUDIO/b64.txt")
   # data = readFromFile("C:/AUDIO/b64.txt")

    return data
