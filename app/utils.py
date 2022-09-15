from gtts import gTTS
import os.path
import os
import common as c
import base64
import helper as h

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

def flushDirectory():
    return None

def generateAudio(text,lang,ticket,paths=c.PATH_FOLDER):
    
    if not os.path.exists(paths):
        h.FlushRepository()
        os.makedirs(paths)
    
    AudioFiles = paths+"/audio_"+lang+"_"+ticket+".mp4"
    TxtFiles = paths+"/base64_"+lang+"_"+ticket+".txt"

    print(TxtFiles)
    textSpeechFR = gTTS(text=text, lang=lang, slow=False)
    textSpeechFR.save(AudioFiles)

    
    writeToFile(AudioFiles,TxtFiles)
    data = readFromFile(TxtFiles)

    return data


