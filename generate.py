from textgenrnn import textgenrnn
from datetime import datetime
import sys
import os 
from getdadjoketweet import getData

today = datetime.now().strftime("%Y-%m-%d")
filename = 'data/dadjokes-'+today+'.txt'
version = 0
trained_model_filename = 'weights/textgenrnn_weights_'+str(version)+'.hdf5'
latest_version =0
def train(epochs=1,tweet_count=500):
    print("Epochs "+str(epochs))
    trained_model_filename = updateCurrentModelFilename()
    textgen = textgenrnn()
    if not os.path.isfile(filename):
        getData(tweet_count)
    textgen.train_from_file(filename, num_epochs=epochs)
    os.rename('textgenrnn_weights.hdf5',trained_model_filename)
    print("Generated Model to file "+ trained_model_filename)
def generate(model_version=0):
    trained_model_filename = 'weights/textgenrnn_weights_'+str(model_version)+'.hdf5'
    if not os.path.isfile(trained_model_filename): 
        train()
    textgen2 = textgenrnn(trained_model_filename)
    return textgen2.generate()

def updateCurrentModelFilename():
    trained_model_filename = 'weights/textgenrnn_weights_'+str(version)+'.hdf5'
    while os.path.isfile(trained_model_filename):
        version +=1
        trained_model_filename = 'weights/textgenrnn_weights_'+str(version)+'.hdf5'
    return trained_model_filename
def getLatestVersionNumber():
    latest_version = 0
    while os.path.isfile('weights/textgenrnn_weights_'+str(latest_version)+'.hdf5'):
        latest_version += 1
    return latest_version - 1 if latest_version > 0 else 0
def main():
    # print command line arguments
    latest_version = getLatestVersionNumber()    
    print("Current latest version "+ str(latest_version))
    arg = sys.argv[1]
    if arg == "generate": 
        generate(model_version=int(sys.argv[2]))
    elif arg == "train":
        train(epochs=int(sys.argv[2]),tweet_count=int(sys.argv[3]))
    else: 
        raise ValueError(arg+" not a valid operator. Please enter argument \'generate\' or \'train\'")
        
if __name__ == "__main__":
    main()
    pass