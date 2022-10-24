import nltk, json, pickle

class ReadJSON():
    def __init__(self):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        self.intents_json = json.loads(open('intents.json').read())
        self.ignored_words = ['?', '!']

        self.words = []
        self.classes = []
        self.documents = []

    def preprocess_data(self):
        for intent in self.intents_json['intents']:
            for pattern in intent['patterns']:
                
                tokenized_words = nltk.word_tokenize(pattern)

                self.words.extend(tokenized_words)
                self.documents.append((tokenized_words, intent['tag']))

                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

    def lemmatize(self):
        self.words = [self.lemmatizer.lemmatize(word.lower()) for word in self.words if word not in self.ignored_words]
        #Remove duplicates and sort unique lists
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

    def create_file(self, data, name):
        pickle.dump(data, open(name, 'wb'))

    def read_data(self):
        self.preprocess_data()   
        self.lemmatize()
    
    def save_files(self):
        self.create_file(self.words, 'words.pkl')
        self.create_file(self.classes, 'classes.pkl')
        print("[INFO]  Files saved: 'words.pkl' and 'classes.pkl")
