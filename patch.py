import os
import time
import string
#time.sleep(5)
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
text = load('/home/ako/hcode/final/text')
text.pop()
save('/home/ako/hcode/final/text',text)
