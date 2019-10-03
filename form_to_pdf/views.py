import urllib, json
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect, FileResponse
from .forms import PDFform
from .models import CreatePDF
import io
from reportlab.pdfgen import canvas


# Create your views here.
def index(request):
    error = 'None'
    if request.method == 'POST':
        form = PDFform(request.POST)
        if form.is_valid():

            sender = request['sender']
            subject = request['subject']
            message = request['message']
            # success = True
            # form.save()
            new_PDF = CreatePDF(sender, subject, message)
            # new_PDF.assemble()
            # buffer = new_PDF.report()
            # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
            return render(request, 'form_to_pdf/index2.html', {'success': True})

        # if a GET (or any other method) we'll create a blank form
    else:
        form = PDFform()

    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'form_to_pdf/index2.html', context)


def report(request):
    error = 'None'
    if request.method == 'POST':
        form = PDFform(request.POST)
        if form.is_valid():
            new_PDF = form.save()
            buffer, filename = new_PDF.report()
            return FileResponse(buffer, as_attachment=True, filename=filename)
        else:
            error = 'Invalid form'
        # if a GET (or any other method) we'll create a blank form
    else:
        form = PDFform()

    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'form_to_pdf/index2.html', context)
    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def test(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


def test2(request):
    error = 'None'
    form = PDFform()
    context = {
        'form': form,
        'error': error,
    }
    if request.method == 'POST':
        sender = request.POST['sender']
        subject = request.POST['subject']
        message = request.POST['message']
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setLineWidth(.3)
        p.setFont('Helvetica', 12)
        p.drawString(30, 750, sender)
        # p.drawString(500, 750, date)
        p.line(480, 747, 580, 747)

        p.drawString(30, 735, subject)
        p.drawString(30, 720, message)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    else:
        return render(request, 'form_to_pdf/index.html', context)
