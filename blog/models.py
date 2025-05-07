# blog/models.py

import os
from django.db import models

# untuk training111111111111111111111111111111111111111111111111111

def upload_training(instance, filename):
    return f'pdftraining/{filename}'

class PDFTraining(models.Model):
    title = models.CharField(max_length=200, default='Default Training')
    file = models.FileField(upload_to=upload_training) #asli
    # file = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
    
    # def delete(self, *args, **kwargs):
    #     if self.file:
    #         try:
    #             if os.path.isfile(self.file.path):
    #                 os.remove(self.file.path)
    #         except Exception as e:
    #             # Log the error
    #             print(f"Error deleting file: {e}")
    #     super().delete(*args, **kwargs)

# untuk tester22222222222222222222222222222222222222222222

def upload_tester(instance, filename):
    return f'pdftester/{filename}'

class PDFTester(models.Model):
    title = models.CharField(max_length=200, default='Default Tester')
    file = models.FileField(upload_to=upload_tester) #asli
    # file = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
        
    # def delete(self, *args, **kwargs):
    #     if self.file:
    #         try:
    #             if os.path.isfile(self.file.path):
    #                 os.remove(self.file.path)
    #         except Exception as e:
    #             # Log the error
    #             print(f"Error deleting file: {e}")
    #     super().delete(*args, **kwargs)
    
# class PlagiarismResult(models.Model):

class PlagiarismResult(models.Model):
    tester_file_name = models.CharField(max_length=255)
    training_file_name = models.CharField(max_length=255)
    code_result_percent = models.CharField(max_length=10)
    list_same_code = models.JSONField()
    text_result_percent = models.CharField(max_length=10)
    list_same_text = models.JSONField()
    join_result_percent = models.CharField(max_length=10)

