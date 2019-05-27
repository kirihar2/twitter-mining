from textgenrnn import textgenrnn
from datetime import datetime
import sys
import os 
from .getdadjoketweet import getData


    # today = datetime.now().strftime("%Y-%m-%d")
    # filename = 'data/dadjokes-'+today+'.txt'
    # version = 0
    # trained_model_filename = 'weights/textgenrnn_weights_'+str(version)+'.hdf5'
    # latest_version =0
def getDataFilename(data_filename):
    today = datetime.now().strftime("%Y-%m-%d")
    return data_filename+'-'+today+'.txt'

def train(epochs=1,tweet_count=500,data_filename='data/dadjokes',output_filename='weights/textgenrnn_weights'):
    print("Epochs "+str(epochs))
    trained_model_filename = updateCurrentModelFilename(output_filename)
    textgen = textgenrnn()
    if not os.path.isfile(data_filename):
        filename = getData(tweet_count,data_filename)
    textgen.train_from_file(filename, num_epochs=epochs)
    os.rename('textgenrnn_weights.hdf5',trained_model_filename)
    print("Generated Model to file "+ trained_model_filename)
    return trained_model_filename
def generate(model_version=0,count=1,filename='weights/textgenrnn_weights'):
    trained_model_filename = os.getcwd()+'/'+filename+'_'+str(model_version)+'.hdf5'
    if not os.path.isfile(trained_model_filename): 
        _ = train(output_filename = filename)
    textgen2 = textgenrnn(trained_model_filename)
    return textgen2.generate(count)

def updateCurrentModelFilename(filename):
    version = getLatestVersionNumber(filename)
    trained_model_filename = os.getcwd()+'/'+filename+'_'+str(version)+'.hdf5'
    while os.path.isfile(trained_model_filename):
        version +=1
        trained_model_filename =  os.getcwd()+'/'+filename+'_'+str(version)+'.hdf5'
    return trained_model_filename
def getLatestVersionNumber(filename):
    latest_version = 0
    filename = os.getcwd()+'/'+filename
    while os.path.isfile(filename+'_'+str(latest_version)+'.hdf5'):
        latest_version += 1
    return latest_version - 1 if latest_version > 0 else 0
