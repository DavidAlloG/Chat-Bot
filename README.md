# Chat Bot

#### Author: David García Allo
#### Date: 24/10/2022

#### Description
The app saves the data contained in 'intents.json' in the files 'classes.pkl' and 'words.pkl' if not exist yet.

Then trains a Sequential Neural Network model 'chatbot_model.h5' if not exist yet.

I included in this model an early stop clause if the model does not improve the loss in 5 epochs.

When the send button is pressed we use the saved model to predict the tag that fits better and the show a random 
response in the responses pool of the tag.


#### Modules needed
nltk, keras, pickle, numpy, random, tkinter, tensorflow, json

#### Ideas to improve
- Try to improve the GUI, it looks very simple.
- The bot does not work correctly when no tag is predicted.
- Also it has problems with some typing misspells.