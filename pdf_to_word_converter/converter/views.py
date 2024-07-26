from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings
import os
import uuid
from pdf2docx import Converter

def convert_pdf_to_word(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        
        # Save the PDF file with a unique name
        fs = FileSystemStorage()
        unique_id = uuid.uuid4().hex
        filename = f"{unique_id}_{pdf_file.name}"
        file_path = fs.save(filename, pdf_file)
        file_path = fs.path(file_path)
        
        # Convert PDF to DOCX
        output_docx_path = os.path.join(settings.MEDIA_ROOT, f"{unique_id}.docx")
        convert_pdf_to_docx(file_path, output_docx_path)
        
        # Serve the DOCX file
        with open(output_docx_path, 'rb') as docx_file:
            response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={filename.replace(".pdf", ".docx")}'
            return response
    
    return render(request, 'upload.html')

def convert_pdf_to_docx(pdf_path, output_docx_path):
    cv = Converter(pdf_path)
    cv.convert(output_docx_path)
    cv.close()
