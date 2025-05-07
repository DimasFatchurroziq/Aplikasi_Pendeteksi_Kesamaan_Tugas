# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import FileFieldForm, UploadFileForm
from .models import PDFTraining, PDFTester
import io

def view_pdf_training(request, pdf_id):
    pdf = get_object_or_404(PDFTraining, pk=pdf_id)  # Mengganti dengan model yang Anda gunakan
    response = HttpResponse(pdf.file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{pdf.title}.pdf"'
    return response

def download_pdf_training(request, pdf_id):
    pdf = get_object_or_404(PDFTraining, pk=pdf_id)
    response = HttpResponse(pdf.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf.title}.pdf"'
    return response

def delete_pdf_training(request, pdf_id):
    document = get_object_or_404(PDFTraining, pk=pdf_id)
    document.delete()
    return redirect('upload_multiple_pdfs')

# untuk tester

def view_pdf_tester(request, pdf_id):
    pdf = get_object_or_404(PDFTester, pk=pdf_id)  # Mengganti dengan model yang Anda gunakan
    response = HttpResponse(pdf.file, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{pdf.title}.pdf"'
    return response

def download_pdf_tester(request, pdf_id):
    pdf = get_object_or_404(PDFTester, pk=pdf_id)
    response = HttpResponse(pdf.file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf.title}.pdf"'
    return response

def delete_pdf_tester(request, pdf_id):
    document = get_object_or_404(PDFTester, pk=pdf_id)
    document.delete()
    return redirect('upload_pdf')

# 33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333

def handle_uploaded_file(file, category):
    if category == 'training':
        PDFTraining.objects.create(file=file, title=file.name)
    elif category == 'tester':
        PDFTester.objects.create(file=file, title=file.name)
        
        
def upload_pdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for file in files:
                handle_uploaded_file(file, 'tester')
            return redirect('upload_multiple_pdfs')  # Redirect ke halaman yang sama atau ke halaman lain
    else:
        form = UploadFileForm()
    tester_documents = PDFTester.objects.all()
    training_documents = PDFTraining.objects.all()
    return render(request, 'upload_multiple_pdfs.html', {'form': form, 'tester_documents': tester_documents, 'training_documents': training_documents})

def upload_multiple_pdfs(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            for file in files:
                handle_uploaded_file(file, 'training')
            return redirect('upload_multiple_pdfs')  # Redirect ke halaman yang sama atau ke halaman lain
    else:
        form = UploadFileForm()
    tester_documents = PDFTester.objects.all()
    training_documents = PDFTraining.objects.all()
    return render(request, 'upload_multiple_pdfs.html', {'form': form, 'tester_documents': tester_documents, 'training_documents': training_documents})

# 4444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444

# blog/views.py
from django.shortcuts import render
from .models import PDFTraining, PDFTester
import time
from .excecute.preprocessing import Preprocessing
from .excecute.classification import Classification
from .excecute.checkplagiat import Checkplagiat
from .excecute.extraction import Extraction
from .excecute.preview import Preview
from .models import PlagiarismResult
# detail_check = []

def run_plagiarism_check(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        start_time = time.time()
        
        global detail_check
        # Mengambil data PDF dari database
        tester_pdfs = PDFTester.objects.all()
        training_pdfs = PDFTraining.objects.all()

        # Membaca file PDF dan judulnya ke dalam memori
        tester_data = []
        for pdf in tester_pdfs:
            # Membaca file menggunakan file.read()
            with pdf.file.open('rb') as file_stream:
                title = pdf.title
                content = file_stream.read()
                tester_data.append((title, content))

        training_data = []
        for pdf in training_pdfs:
            # Membaca file menggunakan file.read()
            with pdf.file.open('rb') as file_stream:
                title = pdf.title
                content = file_stream.read()
                training_data.append((title, content))

        # Ekstraksi konten dari memori
        extractor = Extraction(tester_data=tester_data, training_data=training_data, from_memory=True)
        tester_name, training_name, tester_result, training_result = extractor.extract()

        # klasifikasi
        model_path = 'best_model.keras'
        tokenizer_path = 'tokenizer.json'
        dataset_path = r'C:\Users\Dimas Fatchurroziq\Downloads\dataset1.csv'

        text_model = Classification(model_path, tokenizer_path, tester_name, training_name, tester_result, training_result)
        tester_name, training_name, tester_dictionary, training_dictionary = text_model.input()
        
        # Pra-pemrosesan konten yang diekstrak
        preprocessor = Preprocessing(tester_name, training_name, tester_dictionary, training_dictionary)
        tester_name, training_name, tester_dictionary_2, training_dictionary_2 = preprocessor.input()

        # Memeriksa plagiarisme
        plagiarism = Checkplagiat(tester_name, training_name, tester_dictionary_2, training_dictionary_2) 
        tester_name, training_name, result = plagiarism.satuvssemua()
        # print(result)
        
        lihat = Preview(tester_name, training_name, result, tester_dictionary_2) 
        tester_name, training_name, result_2, w = lihat.view()
        # print(result_2)
        
        
        # Menyiapkan hasil untuk rendering
        combined_results = []
        # detail_check = []
        for index, tester_file_name in enumerate(tester_name):
            if tester_file_name in result_2:
                for training_file_name in training_name:
                    if training_file_name in result_2[tester_file_name]: 
                        code_result = result_2[tester_file_name][training_file_name]['code_result']
                        code_result_percent = f"{code_result * 100:.1f}"  
                        
                        list_same_code = result_2[tester_file_name][training_file_name]['list_same_code']
                        
                        text_result = result_2[tester_file_name][training_file_name]['text_result']
                        text_result_percent = f"{text_result * 100:.1f}" 
                        
                        list_same_text = result_2[tester_file_name][training_file_name]['list_same_text']
                        
                        join_result = result_2[tester_file_name][training_file_name]['join_result']
                        join_result_percent = f"{join_result * 100:.1f}" 
                        
                        combined_results.append([index, tester_file_name, training_file_name, code_result_percent, text_result_percent, join_result_percent])
                        PlagiarismResult.objects.create(
                            tester_file_name=tester_file_name,
                            training_file_name=training_file_name,
                            code_result_percent=code_result_percent,
                            list_same_code=list_same_code,
                            text_result_percent=text_result_percent,
                            list_same_text=list_same_text,
                            join_result_percent=join_result_percent
                        )
        name = tester_name[0]
        end_time = time.time()
        execution_time = end_time - start_time
        results = list(PlagiarismResult.objects.values())
        # Mengirim hasil dan waktu eksekusi ke template
        data = {
            'results': results,
            'execution_time': execution_time,
            # 'name' : name,\
            'tester_name': name,
        }
        return JsonResponse(data)

    return render(request, 'run_plagiarism_check.html')

from django.http import HttpResponseRedirect
from django.urls import reverse




#wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww



def detail_view(request, result_id):
    # Mendapatkan detail berdasarkan result_id
    result = get_object_or_404(PlagiarismResult, id=result_id)

    context = {
        'result5': result.list_same_code,
        'result6': result.list_same_text,
    }
    return render(request, 'preview_check.html', context)

#hapus semua

def delete_all(request):
    # Hapus semua file di PDFTraining
    for training in PDFTraining.objects.all():
        if training.file:
            training.file.delete()
        training.delete()

    # Hapus semua file di PDFTester
    for tester in PDFTester.objects.all():
        if tester.file:
            tester.file.delete()
        tester.delete()
        
    # Hapus semua data di PlagiarismResult
    PlagiarismResult.objects.all().delete()

    return redirect('upload_pdf')


def coba(request):
    return render(request, 'wkwk.html')

def upload_multiple(request):
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        category = request.POST.get('category')
        if form.is_valid():
            for file in files:
                handle_uploaded_file(file, category)
            return redirect('upload_multiple_pdfs')
    else:
        form = FileFieldForm()
    
    tester_documents = PDFTester.objects.all()
    training_documents = PDFTraining.objects.all()
    return render(request, 'upload_multiple_pdfs.html', {'form': form, 'tester_documents': tester_documents, 'training_documents': training_documents})