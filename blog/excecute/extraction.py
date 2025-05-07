from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTFigure
import os
import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from io import BytesIO

class Extraction:
    def __init__(self, directory_tester=None, directory_training=None, tester_data=None, training_data=None, from_memory=False):
        self.directory_tester = directory_tester
        self.directory_training = directory_training
        self.tester_data = tester_data
        self.training_data = training_data
        self.from_memory = from_memory
        
    def extract(self):
        if self.from_memory:
            tester_name = [title for title, _ in self.tester_data]
            training_name = [title for title, _ in self.training_data]
            tester_result = [self.extract_text_from_memory(content) for _, content in self.tester_data]
            training_result = [self.extract_text_from_memory(content) for _, content in self.training_data]
        else:
            sample_tester = [os.path.join(self.directory_tester, doc) for doc in os.listdir(self.directory_tester) if doc.endswith('.pdf')]
            sample_training = [os.path.join(self.directory_training, doc) for doc in os.listdir(self.directory_training) if doc.endswith('.pdf')]
            tester_name = []
            training_name = []
            tester_result = []
            training_result = []
            for x in range(2):   
                if x == 0:
                    for file in sample_tester:
                        names = os.path.basename(file)
                        tester_name.append(names)
                        text = self.extract_text(file)
                        tester_result.append(text)
                elif x == 1:
                    for file in sample_training:
                        names = os.path.basename(file)
                        training_name.append(names)
                        text = self.extract_text(file)
                        training_result.append(text)
                else:
                    continue
        return tester_name, training_name, tester_result, training_result

    def extract_text(self, file):
        get_image = self.extract_image(file)
        ext_element = self.extract_elements(file)
        get_all_text = self.extract_element(ext_element, get_image)
        return get_all_text

    def extract_text_from_memory(self, file):
        file_stream = BytesIO(file)
        get_image = self.extract_image(file_stream)
        ext_element = self.extract_elements(file_stream)
        get_all_text = self.extract_element(ext_element, get_image)
        return get_all_text
        
    def extract_image(self, file_path):
        # Handle both file path and BytesIO object
        if isinstance(file_path, (str, bytes, os.PathLike)):
            pdf_document = fitz.open(file_path)
        else:
            pdf_document = fitz.open(stream=file_path, filetype="pdf")

        images_info = []
        for page_index in range(len(pdf_document)):
            page = pdf_document.load_page(page_index)
            image_list = page.get_images(full=True)
            for img in image_list:
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                images_info.append(image_bytes)
        pdf_document.close()
        return images_info
    
    # def extract_element(self, file_path):
    #     all_pages_sorted_elements = []
    #     # Handle both file path and BytesIO object
    #     if isinstance(file_path, (str, bytes, os.PathLike)):
    #         pdf_stream = file_path
    #     else:
    #         pdf_stream = BytesIO(file_path.read())
    #     for page_layout in extract_pages(pdf_stream):
    #         page_elements = []
    #         for element in page_layout:
    #             page_elements.append(element)
    #         sorted_elements = self.sort_elements(page_elements)
    #         all_pages_sorted_elements.append(sorted_elements)
    #     return all_pages_sorted_elements
            
    def extract_elements(self, file_path):
        all_pages_sorted_elements = []
        pdf_document = None  # Inisialisasi variabel untuk menyimpan referensi ke objek pdf_document
        
        try:
            # Handle both file path and BytesIO object
            if isinstance(file_path, (str, bytes, os.PathLike)):
                pdf_stream = file_path
                pdf_document = fitz.open(file_path)
            else:
                pdf_stream = BytesIO(file_path.read())
                pdf_document = fitz.open(stream=file_path, filetype="pdf")
            
            for page_layout in extract_pages(pdf_stream):
                page_elements = []
                for element in page_layout:
                    page_elements.append(element)
                sorted_elements = self.sort_elements(page_elements)
                all_pages_sorted_elements.append(sorted_elements)
        finally:
            if pdf_document:
                pdf_document.close()  # Pastikan file ditutup bahkan jika terjadi exception
        
        return all_pages_sorted_elements
        
    @staticmethod
    def sort_elements(elements):
        return sorted(elements, key=lambda e: (e.bbox[1], e.bbox[0]))
    
    def extract_element(self, all_pages_sorted_elements, images_info):
        all_text = []
        img_index = 0
        for sorted_elements in all_pages_sorted_elements:
            for element in sorted_elements:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text()
                    lines = text.split('\n')
                    lines = [line.strip() for line in lines if line.strip()]
                    all_text.extend(lines)
                elif isinstance(element, LTFigure) and img_index < len(images_info):
                    image = Image.open(BytesIO(images_info[img_index]))
                    ocr_text = pytesseract.image_to_string(image)
                    lines = ocr_text.split('\n')
                    lines = [line.strip() for line in lines if line.strip()]
                    all_text.extend(lines)
                    img_index += 1
        return all_text
