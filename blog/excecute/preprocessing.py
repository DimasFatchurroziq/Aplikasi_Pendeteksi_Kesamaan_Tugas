import os
import re

from nltk.util import ngrams
from nltk.tokenize import word_tokenize

class Preprocessing:
    
    def __init__(self, tester_name, training_name, tester_dictionary, training_dictionary):
        self.tester_name = tester_name
        self.training_name = training_name
        self.tester_dictionary = tester_dictionary
        self.training_dictionary = training_dictionary
        
    def input(self):        
        tester_dictionary_2 = {}
        training_dictionary_2 = {}
        
        for name in self.tester_name:
            if name in self.tester_dictionary:
                test_code_tester = self.tester_dictionary[name]['tester_code_result']
                content_rollinghash_code_tester = self.preprocess_file_code(test_code_tester)
                        
                test_text = self.tester_dictionary[name]['tester_text_result']
                text_join = ' '.join(map(str, test_text))
                content_rollinghash_text_tester, test_text_tester = self.preprocess_file_text_tester(text_join)
                
                tester_dictionary_2[name] = {
                    'tester_code_result': content_rollinghash_code_tester,
                    'tester_text_result': content_rollinghash_text_tester,
                    'list_code':test_code_tester,
                    'list_text':test_text_tester
                }
                
        for name in self.training_name:
            if name in self.training_dictionary:
                test_code = self.training_dictionary[name]['training_code_result']
                content_rollinghash_code_training = self.preprocess_file_code(test_code)
                        
                test_text = self.training_dictionary[name]['training_text_result']
                text_join = ' '.join(map(str, test_text))
                content_rollinghash_text_training = self.preprocess_file_text_training(text_join)

                training_dictionary_2[name] = {
                    'training_code_result': content_rollinghash_code_training,
                    'training_text_result': content_rollinghash_text_training,
                }       
                        
                    
        return self.tester_name, self.training_name, tester_dictionary_2, training_dictionary_2
    
    def preprocess_file_code(self, file_content):
        list_code = []
        for content in file_content:
            content_replace = content.replace(' ', '')
            content_rollinghash = self.rollinghash_code(content_replace)
            list_code.append(content_rollinghash)
        return list_code
        
    def rollinghash_code(self, item_list):
        hash_value = 0
        window_size = len(item_list)
        base = 4  # Basis ASCII
        for i in range(window_size):
            hash_value = (hash_value * base + ord(item_list[i]))
        return hash_value   #hash_value
    
    def preprocess_file_text_tester(self, file_content):
        content = file_content.replace('\n', '')
        content_lower = self.lowercase_text(content)
        content_remove = self.remove(content_lower)
        content_tokenisasi = self.tokenisasi(content_remove)
        content_rollinghash = self.rollinghash_text(content_tokenisasi) #content_tokenisasi
        return content_rollinghash, content_tokenisasi #content_rollinghash
    
    def preprocess_file_text_training(self, file_content):
        content = file_content.replace('\n', '')
        content_lower = self.lowercase_text(content)
        content_remove = self.remove(content_lower)
        content_tokenisasi = self.tokenisasi(content_remove)
        content_rollinghash = self.rollinghash_text(content_tokenisasi) #content_tokenisasi
        return content_rollinghash #content_rollinghash
    
    def lowercase_text(self, text):  # Tambahkan self di sini
        lowercased_text = text.lower()
        return lowercased_text

    def remove(self,text):
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return clean_text

    def tokenisasi(self,text):
        words = word_tokenize(text)
        tokenisasi = list(ngrams(words, 3))
        return(tokenisasi)
    
    def rollinghash_text(self,list):
        base = 4 # Basis ASCII
        kuk=[]
        for text in list:
            hash_value = 0
            for word in text:
                for char in word:
                    hash_value = (hash_value * base + ord(char))
            kuk.append(hash_value) #hash_value
        return kuk #kuk