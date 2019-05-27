from textgenrnn import textgenrnn
from datetime import datetime
import sys
import os 
from getdadjoketweet import getData

today = datetime.now().strftime("%Y-%m-%d")
filename = 'data/dadjokes-'+today+'.txt'
trained_model_filename = 'weights/textgenrnn_weights.hdf5'

def train(epochs=1):
    print("Epochs "+str(epochs))
    textgen = textgenrnn()
    if not os.path.isfile(filename):
        getData()
    textgen.train_from_file(filename, num_epochs=epochs)
    os.rename('textgenrnn_weights.hdf5',trained_model_filename)
def generate():
    if not os.path.isfile(trained_model_filename): 
        train()
    textgen2 = textgenrnn(trained_model_filename)
    return textgen2.generate()

def main():
    # print command line arguments
    arg = sys.argv[1]
    if arg == "generate": 
        generate()
    elif arg == "train":
        train(epochs=sys.argv[2])
    else: 
        raise ValueError(arg+" not a valid operator. Please enter argument \'generate\' or \'train\'")
        
if __name__ == "__main__":
    main()
    pass