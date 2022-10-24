import random, numpy, keras, tensorflow

class Train():
    def __init__(self, readjson):
        self.readjson = readjson
        self.readjson.read_data()

    def create_bag(self):
        self.train_sample = []
        output_empty = [0] * len(self.readjson.classes)
        #Training set with a bag of words for each sentence
        for doc in self.readjson.documents:
            bag = []
            #Words in the pattern (already tokenized)
            pattern_words = doc[0]
            pattern_words = [self.readjson.lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            #Set the bag 1's for matched words in current pattern
            for word in self.readjson.words:
                if word in pattern_words: bag.append(1)
                else: bag.append(0)

            output_row = list(output_empty)
            #Output: '1' for the current class, '0' for the rest of the classes
            output_row[self.readjson.classes.index(doc[1])] = 1
            #Append output and bag together in the training sample
            self.train_sample.append([bag, output_row])

    def prepare_sample(self):
        #Shuffle the sample
        random.shuffle(self.train_sample)
        self.train_sample = numpy.array(self.train_sample, dtype=object)
        #Create train lists: X->patterns, Y->intents
        self.train_x = list(self.train_sample[:,0])
        self.train_y = list(self.train_sample[:,1])

    def build_model(self):
        """Model: 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer 
        contains number of neurons equal to number of intents to predict output intent with softmax."""
        self.model = keras.models.Sequential()

        self.model.add(keras.layers.Dense(128, input_shape=(len(self.train_x[0]), ), activation='relu'))
        self.model.add(keras.layers.Dropout(0.5))
        self.model.add(keras.layers.Dense(64, activation='relu'))
        self.model.add(keras.layers.Dropout(0.5))
        self.model.add(keras.layers.Dense(len(self.train_y[0]), activation='softmax'))

        """Compiler: SGD optimizer and Nesterov accelerated gradient"""
        sgd = keras.optimizers.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    def fit_model(self):
        #If each 5 epochs loss doesn't decrease -> Finish the fit
        earlystop = tensorflow.keras.callbacks.EarlyStopping(monitor='loss', patience=5) 
        #Fitting
        print('[INFO]  Fitting the model ...')
        hist = self.model.fit(numpy.array(self.train_x), numpy.array(self.train_y), epochs=200, callbacks=[earlystop], batch_size=5, verbose=1)
        #Saving the model    
        self.model.save('chatbot_model.h5', hist)
        print("[INFO]  Model saved: 'chatbot_model.h5'")

    def run(self):
        self.create_bag()
        self.prepare_sample()
        self.build_model()
        self.fit_model()
