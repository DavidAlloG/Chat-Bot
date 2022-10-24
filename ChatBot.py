import nltk, keras, pickle, numpy, random
from gui import GUI
from train import  Train
from read import ReadJSON

class APP():
    def __init__(self):
        #Data load
        self.readjson = ReadJSON()
        self.load_data()
        self.load_model()
            
        #GUI init passing the response function
        self.gui = GUI(self.chatbot_response)

    def load_data(self):
        try:
            #Load existing files
            self.words = pickle.load(open('words.pkl', 'rb'))
            self.classes = pickle.load(open('classes.pkl', 'rb'))
        except:
            try:
                #Read the JSON and create the files
                self.readjson.read_data()
                self.readjson.save_files()
                #Load the created files
                self.words = pickle.load(open('words.pkl', 'rb'))
                self.classes = pickle.load(open('classes.pkl', 'rb'))
            except:
                print('[ERROR]  Data can not be loaded')

    def load_model(self):
        try:
            #Load existing model
            self.model = keras.models.load_model('chatbot_model.h5')
        except:
            try:
                #Train a new model
                train = Train(self.readjson)
                train.run()
                #Load the new model
                self.model = keras.models.load_model('chatbot_model.h5')
            except:
                print('[ERROR]  Model can not be loaded')

    def bagging(self, sentence, debug=False):
        #Tokenize and stemming
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.readjson.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        #Create bag
        bag = [0]*len(self.words)
        #Loop through all words in sentence and all words in json file
        for sentence_word in sentence_words:
            for index, word in enumerate(self.words):
                #If there is a match we create 1 in the bag
                if sentence_word == word:
                    bag[index] = 1
                #Debug option
                if debug:
                    print('Word matched: %s' % word)
        #Turn the bag into an array: 1 for each word in the bag that exists in the sentence
        bag = numpy.array(bag)
        return bag

    def predict_class(self, sentence):
        bag = self.bagging(sentence)
        #Prediction
        results = self.model.predict(numpy.array([bag]), verbose=1)[0]
        """Notes: I need this array into array for layers compatibility. 
        Then I have to call back the array which it is the firs row of the matrix.
        The results contain the probabilities of each class to be the right one"""
        #Filter out predictions below a probabilty threshold
        error_threshold = 0.25
        results = [[index, result] for index, result in enumerate(results) if result > error_threshold]
        #We saved the index in the results for probability strength sorting without information loss
        results.sort(key= lambda x: x[1], reverse=True)
        #Return a list of dictionaries with the predicted classes and its probabilities
        results_dicts = []
        for result in results:
            results_dicts.append({'intent': self.classes[result[0]], 'probability': str(result[1])})

        return results_dicts

    def get_response(self, prediction):
        """Get a random response from responses of the predicted class.
        The first element in the prediction list is the most probable class"""
        tag = prediction[0]['intent']
        #Loop to obtain the responses of the prediced tag and choose one of them
        for intent in self.readjson.intents_json['intents']:
            if intent['tag'] == tag:
                result = random.choice(intent['responses'])
                break
        
        return result

    def chatbot_response(self, sentence):
        """Obtain the prediction and a response"""
        pred = self.predict_class(sentence)
        result = self.get_response(pred)
        return result
    
    def run(self):
        self.gui.update()

if __name__ == '__main__':
    app = APP()
    app.run()