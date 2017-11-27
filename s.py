#Python 2.x program to transcribe an Audio file
import speech_recognition as sr
import cPickle
import gzip

def load(file_name):
    # load the model
    stream = gzip.open(file_name, "rb")
    model = cPickle.load(stream)
    stream.close()
    return model


def save(file_name, model):
    # save the model
    stream = gzip.open(file_name, "wb")
    cPickle.dump(model, stream)
    stream.close()
AUDIO_FILE = ("temp.wav")

# use the audio file as the audio source

r = sr.Recognizer()

with sr.AudioFile(AUDIO_FILE) as source:
    #reads the audio file. Here we use record instead of
    #listen
    audio = r.record(source)

try:
    temp = r.recognize_google(audio)
    print("The audio file contains: " + temp)
    text = load('/home/ako/hcode/final/text')
    text.append(temp)
    save('/home/ako/hcode/final/text',text)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
    text = load('/home/ako/hcode/final/text')
    text.append('junk')
    save('/home/ako/hcode/final/text',text)

except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
