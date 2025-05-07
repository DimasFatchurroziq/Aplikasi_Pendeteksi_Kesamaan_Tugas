from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
# from keras.preprocessing.text import tokenizer_from_json
import numpy as np
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer, tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from itertools import chain
import json

class Classification:
    def __init__(self, model_path, tokenizer_path, tester_name, training_name, tester_result, training_result):
        self.tester_name = tester_name
        self.training_name = training_name
        self.tester_result = tester_result
        self.training_result = training_result
        # Memuat model yang telah disimpan
        self.model = load_model(model_path)
        # Memuat tokenizer yang telah digunakan selama pelatihan
        with open(tokenizer_path) as f:
            data = json.load(f)
            self.tokenizer = tokenizer_from_json(json.dumps(data))
    
    def input(self):
        tester_dictionary = {}
        training_dictionary = {}
        
        # Iterasi untuk tester_result dan training_result
        for x in range(2):
            if x == 0:
                # Mengumpulkan hasil untuk tester_result
                for file, name in zip(self.tester_result, self.tester_name):
                    if name not in tester_dictionary:
                        tester_dictionary[name] = {'tester_code_result': [], 'tester_text_result': []}
                    
                    list_code, list_text = self.get_original_texts_grouped_by_label(file)
                    tester_dictionary[name]['tester_code_result'].extend(list_code)
                    tester_dictionary[name]['tester_text_result'].extend(list_text)
    
            elif x == 1:
                # Mengumpulkan hasil untuk training_result
                for file, name in zip(self.training_result, self.training_name):
                    if name not in training_dictionary:
                        training_dictionary[name] = {'training_code_result': [], 'training_text_result': []}
                        
                    list_code, list_text = self.get_original_texts_grouped_by_label(file)
                    training_dictionary[name]['training_code_result'].extend(list_code)
                    training_dictionary[name]['training_text_result'].extend(list_text)
                    
        return self.tester_name, self.training_name, tester_dictionary, training_dictionary

    def get_original_texts_grouped_by_label(self, texts):
        list_code = []
        list_text = []
        predicted_classes = self.predict_texts(texts)
        
        for text, label in zip(texts, predicted_classes):
            if label != 1:
                list_code.append(text)
            else:
                list_text.append(text)
        return list_code, list_text
    
    def predict_texts(self, texts, max_len=100):
        # Flatten nested list jika diperlukan
        if isinstance(texts[0], list):
            texts = [item for sublist in texts for item in sublist]
        
        # Melakukan tokenisasi teks baru
        sequences = self.tokenizer.texts_to_sequences(texts)
        
        # Melakukan padding pada teks baru
        X = pad_sequences(sequences, maxlen=max_len)
        
        # Meminta model untuk melakukan prediksi
        predictions = self.model.predict(X)
        
        # Mendapatkan kelas prediksi
        predicted_classes = np.argmax(predictions, axis=1)
        
        return predicted_classes