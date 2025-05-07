
class Preview:
    
    def __init__(self, tester_name, training_name, result, tester_dictionary_2):
        self.tester_name = tester_name
        self.training_name = training_name
        self.result = result
        self.tester_dictionary_2 = tester_dictionary_2
        
    def view(self):
        
        result_2 = {}
        
        for tester_file_name in self.tester_name:
            if tester_file_name not in result_2:
                result_2[tester_file_name] = {}
            
            if tester_file_name in self.result:
                for training_file_name in self.training_name:
                    if training_file_name in self.result[tester_file_name]: 
                        if training_file_name not in result_2[tester_file_name]:
                            result_2[tester_file_name][training_file_name] = {}
                        
                        posisi_list_code = self.result[tester_file_name][training_file_name]['posisi_list_code']
                        test_code_tester = self.tester_dictionary_2[tester_file_name]['list_code']
                        # list_same_code = self.get_same_string(test_code_tester, posisi_list_code)
                        list_same_code = self.code_paragraph(posisi_list_code, test_code_tester)
                        
                        # self.result[tester_file_name][training_file_name]['posisi_list_code']= list_same_code
                        
                        posisi_list_text = self.result[tester_file_name][training_file_name]['posisi_list_text']
                        test_text_tester = self.tester_dictionary_2[tester_file_name]['list_text']
                        # list_text = self.get_same_string(test_text_tester, posisi_list_text)
                        # list_same_text = self.join_text(list_text)
                        list_text = self.text_paragraph(posisi_list_text, test_text_tester)
                        list_same_text = self.join_text(list_text)
                        # self.result[tester_file_name][training_file_name]['posisi_list_text']= list_same_text

                        result_2[tester_file_name][training_file_name] = {
                            'code_result': self.result[tester_file_name][training_file_name]['code_result'], 
                            'list_same_code': list_same_code, 
                            'text_result': self.result[tester_file_name][training_file_name]['text_result'], 
                            'list_same_text': list_same_text, 
                            'join_result': self.result[tester_file_name][training_file_name]['join_result']
                        }
                            
        return self.tester_name, self.training_name, result_2, test_text_tester
    
    def get_same_string(self, text_list, positions):
        same_string = []
        # print(text_list)
        for position in positions:  
            if 0 <= position < len(text_list):          
                same_string.append(text_list[position])
        return same_string
    
    def code_paragraph(self, positions, tokenize_list):
        join_list = []
        i = 0
        while i < len(positions):        
            code_join = tokenize_list[positions[i]]
            k = i
            while k + 1 < len(positions) and positions[k] - positions[k + 1] == -1:
                code_join +=  '<br>' + tokenize_list[positions[k + 1]]
                k += 1
            i = k + 1
            join_list.append(code_join)
        return join_list

    
    def text_paragraph(self, positions, tokenize_list):
        join_list = []
        i = 0
        while i < len(positions):        
            text_join = tokenize_list[positions[i]]
            k = i
            while k + 1 < len(positions) and positions[k] - positions[k + 1] == -1:
                text_join += (tokenize_list[positions[k + 1]][2],)
                k += 1
            i = k + 1
            join_list.append(text_join)
        return join_list
    
    def join_text(self, tokenize_list):
        join_list = []
        for token in tokenize_list:
            text_join = ' '.join(map(str, token))
            join_list.append(text_join)
        return join_list
    
    # def wkwkw(self, positions, tokenize_list):
    #     join_list = []
    #     for i in positions:
    #         if positions[i] - positions[i+3] == -3:
    #             text_join=tokenize_list[i] + tokenize_list[i+3]
    #             i+3
    #             join_list.append(text_join)
    #         elif positions[i] - positions[i+2] == -2:
    #             token1 = (tokenize_list[i+2][1], tokenize_list[i+2][2])
    #             text_join=tokenize_list[i] + token1
    #             i+2
    #             join_list.append(text_join)
    #         elif positions[i] - positions[i+1] == -1:
    #             token1 = (tokenize_list[i+2][2])
    #             text_join=tokenize_list[i] + token1
    #             i+2
    #             join_list.append(text_join)
    #         else:
    #             continue
    #     return join_list
    



