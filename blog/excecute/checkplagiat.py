from itertools import combinations

class Checkplagiat:
    
    def __init__(self, tester_name, training_name, tester_dictionary_2, training_dictionary_2):
        self.tester_name = tester_name
        self.training_name = training_name
        self.tester_dictionary_2 = tester_dictionary_2
        self.training_dictionary_2 = training_dictionary_2
    
    # def satuvssatu(self):
    #     for i in range(len(self.list)):
    #         for n in range(i,len(self.list)):
    #             if i != n:
    #                 self.a=self.list[i]
    #                 self.b=self.list[n]
    #                 content_check = self.check(self.a, self.b)
    #                 content_jaccard = self.jaccard(self.a, self.b, content_check)
    #                 print(content_jaccard)
    
    def satuvssemua(self):
        result = {}

        for tester_file_name in self.tester_name:
            if tester_file_name in self.tester_dictionary_2:
                if tester_file_name not in result:
                    result[tester_file_name] = {}
                for training_file_name in self.training_name:  
                    if training_file_name in self.training_dictionary_2:  
                        if training_file_name not in result[tester_file_name]:
                            result[tester_file_name][training_file_name] = {'code_result': None, 'posisi_list_code':None, 'text_result': None, 'posisi_list_text':None, 'join_result': None}
                        
                        tester_code = self.tester_dictionary_2[tester_file_name]['tester_code_result']
                        training_code = self.training_dictionary_2[training_file_name]['training_code_result']
                        content_check_code, posisi_list_code = self.check(tester_code, training_code)
                        content_jaccard_code = self.jaccard(tester_code, training_code, content_check_code)
                        
                        result[tester_file_name][training_file_name]['code_result'] = content_jaccard_code  #content_jaccard_code 
                        result[tester_file_name][training_file_name]['posisi_list_code'] = posisi_list_code             
                        # result['code_result'].append(content_jaccard_code)
                        
                        #########################################
                        
                        tester_text = self.tester_dictionary_2[tester_file_name]['tester_text_result']
                        training_text = self.training_dictionary_2[training_file_name]['training_text_result']
                        content_check_text, posisi_list_text = self.check(tester_text, training_text)
                        content_jaccard_text = self.jaccard(tester_text, training_text, content_check_text)

                        result[tester_file_name][training_file_name]['text_result'] = content_jaccard_text #content_jaccard_text
                        result[tester_file_name][training_file_name]['posisi_list_text'] = posisi_list_text    
                        # result['text_result'].append(content_jaccard_text)
                        
                        #########################################
                        
                        tester_join = tester_code + tester_text
                        training_join = training_code + training_text
                        content_check_join = content_check_code + content_check_text
                        content_jaccard_join = self.jaccard(tester_join, training_join, content_check_join)
                        
                        result[tester_file_name][training_file_name]['join_result'] = content_jaccard_join #content_jaccard_join
                        # result['join_result'].append(content_jaccard_join)
        
        return self.tester_name, self.training_name, result
    
    
    
                    
    def check(self,x,y):
        posisi_list=[]
        y_set = set(y)
        jumlah_nilai_sama = 0
        i=0
        for nilai in x:
            if nilai in y_set:
                jumlah_nilai_sama += 1
                posisi_list.append(i)
            i+=1
        return jumlah_nilai_sama, posisi_list

    def jaccard(self, x, y, z):
        jumlah = len(x) + len(y)
        gabungan = jumlah - z
        if jumlah != 0:
            jaccard = 2 * z / jumlah
        else:
            jaccard = 0  # atau nilai lain yang sesuai

        # jaccard = 2 * z / jumlah
        return jaccard

