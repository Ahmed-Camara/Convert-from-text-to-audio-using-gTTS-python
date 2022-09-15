from gtts import gTTS
import os.path
import os
import common as c
import base64
import shutil
import requests
import urllib

def FlushRepository():
    folder = c.PATH_FOLDER
    with os.scandir(folder) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)


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



def generateAudio(text,lang,ticket,paths=c.PATH_FOLDER):
    
    if not os.path.exists(paths):
        FlushRepository()
        os.makedirs(paths)
    
    audioName = "/audio_"+lang+"_"+ticket+".mp4"
    AudioFiles = paths+audioName
    TxtFiles = paths+"/base64_"+lang+"_"+ticket+".txt"

    print(TxtFiles)
    textSpeechFR = gTTS(text=text, lang=lang, slow=False)
    textSpeechFR.save(AudioFiles)

    audioURL = requests.compat.urljoin("http://"+c.address+"/audio/",audioName)

    writeToFile(AudioFiles,TxtFiles)
    data = readFromFile(TxtFiles)

    return audioURL,data


