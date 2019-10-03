import io
from django.db import models
from fpdf import FPDF
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Create your models here.
class CreatePDF(models.Model):

    sender = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)

    '''
    def __init__(self, sender, subject, message):
        super.__init__(self)
        self.sender = sender
        self.subject = subject
        self.message = message
        self.date_added = datetime.now()
    '''
    '''
        def assemble(self):
        text = self.sender + '\n' + self.subject + '\n' + self.message

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=text, ln=1, align="L")
        pdf.output("./simple_demo.pdf")
    '''

    def report(self):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()
        dt = datetime.now()
        # date = str(dt.day) + "." + str(dt.month) + "." + str(dt.year)
        date = dt.strftime("%d.%m.%Y")
        time = dt.strftime("%H:%M:%S")
        filename = str(self.id) + "_" + self.sender + "_" + date + ".pdf"

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        p.setFont('FreeSans', 12)
        p.setLineWidth(.3)
        # p.setFont('Helvetica', 12)

        p.drawString(30, 750, "Отправитель: ")
        p.drawString(120, 750, self.sender)

        p.drawString(30, 735, "Тема: ")
        p.drawString(120, 735, self.subject)

        p.drawString(30, 720, "Описание: ")
        p.drawString(30, 705, self.message)

        p.drawString(500, 750, date)
        p.line(480, 747, 580, 747)

        # text = self.sender + '\n' + self.subject + '\n' + self.message
        # p.drawString(100, 100, text)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer, filename

    def __str__(self):
        return self.sender + " " + self.subject + " " + self.message[:20]

