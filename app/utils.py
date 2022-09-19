from gtts import gTTS
import os.path
import os
import common as c
import base64
import shutil

def FlushRepository():

    f = "C:/xampp/htdocs/AUDIO"
    with os.scandir(f) as entries:
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


def getAudioAndTxtFiles(lang,ticket):
    return None

def generateAudio(text,lang,ticket,paths):
   
    if not os.path.exists(c.PATH_FOLDER):
        FlushRepository()
        os.makedirs(c.PATH_FOLDER)

        
    audioName = "/audio_"+lang+"_"+ticket+".mp4"
    
    AudioFiles = c.PATH_FOLDER + audioName

    TxtFiles = c.PATH_FOLDER+"/base64_"+lang+"_"+ticket+".txt"

    textSpeechFR = gTTS(text=text, lang=lang, slow=False)
    textSpeechFR.save(AudioFiles)

    lists = paths.split("/")
    print(lists)
    audio = lists[0]
    subFold = lists[1]

    audioURL = c.http+c.address+"/"+audio+"/"+subFold+audioName

    writeToFile(AudioFiles,TxtFiles)
    data = readFromFile(TxtFiles)

    return audioURL,data


