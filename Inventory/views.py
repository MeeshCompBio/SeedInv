from django.shortcuts import render
from .models import Question, Genotypes, GenotypeUploads, GenotypeDownloads
from django.utils import timezone
from .forms import QuestionForm, GenotypesUploadForm, GenotypesDownloadForm
from django.shortcuts import redirect
from .tables import GenotypesTable, UploadRecords, DownloadRecords
from django_tables2.config import RequestConfig
from django.http import HttpResponseRedirect
from .filters import GenoFilter, GenoUploadsFilter, GenoDownloadsFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableView
from django_tables2.export.export import TableExport
from .upload_checks import additions_upload, subtractions_download
from django.conf import settings
from django.shortcuts import render
from qr_code.qrcode.utils import QRCodeOptions
from django.shortcuts import render
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF
from django.contrib import messages


# Create your views here.
def post_list(request):
    questions = Question.objects.all()
    return render(request,
                  'Inventory/inventory.html',
                  {'questions': questions})


def Question_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = QuestionForm()
    return render(request,
                  'Inventory/question_edit.html',
                  {'form': form})


def test(request):
        return render(request, 'Inventory/test.html', {})


def inventory_list(request):
    genotypes = Genotypes.objects.all()
    return render(request,
                  'Inventory/test.html',
                  {'genotypes': genotypes})


def add_inventory(request):
    queryset = GenotypeUploads.objects.all()
    f = GenoUploadsFilter(request.GET, queryset=queryset)
    table = UploadRecords(f.qs, order_by="-uploaded_at")
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

# Check to see if form is valid, even though we will reinitialize it after
# getting a set of log files created
    form = GenotypesUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        # Grab the file and open it
        data = request.FILES.get('document', None)
        # Go through each line of the file
        log_files = additions_upload(data)

        # reinitialize the upload form with the parse out temp file names
        form = GenotypesUploadForm(request.POST or None,
                                   request.FILES or None,
                                   initial={
                                           'upload_pass': 'logs/'+log_files[0],
                                           'upload_fail': 'logs/'+log_files[1],
                                            })
        # fake save to initialize num issues only to replace with log_file val
        form = form.save(commit=False)
        form.issues = log_files[2]
        form.save()

        # This will clear out our form upon submission
        form = GenotypesUploadForm()
        # This will refresh the page so people don't double post
        if int(log_files[2]) == 0:
            return HttpResponseRedirect('/SeedInv')
        else:
            return HttpResponseRedirect('/SeedInv/add_inventory')

    return render(request, 'Inventory/add_inventory.html',
                           {
                            'table': table,
                            'filter': f,
                            'GenotypesUploadForm': GenotypesUploadForm
                            })


def withdraw_inventory(request):
    queryset = GenotypeDownloads.objects.all()
    f = GenoDownloadsFilter(request.GET, queryset=queryset)
    table = DownloadRecords(f.qs, order_by="-uploaded_at")
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

# Check to see if form is valid, even though we will reinitialize it after
# getting a set of log files created
    form = GenotypesDownloadForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        # Grab the file and open it
        data = request.FILES.get('document', None)
        # Go through each line of the file
        log_files = subtractions_download(data)

        # reinitialize the Download form with the parse out temp file names
        form = GenotypesDownloadForm(
                                 request.POST or None,
                                 request.FILES or None,
                                 initial={
                                         'download_pass': 'logs/'+log_files[0],
                                         'download_fail': 'logs/'+log_files[1],
                                    })

        # fake save to initialize num issues only to replace with log_file val
        form = form.save(commit=False)
        form.issues = log_files[2]
        form.save()

        # This will clear out our form upon submission
        form = GenotypesDownloadForm()
        # This will refresh the page so people don't double post
        if int(log_files[2]) == 0:
            return HttpResponseRedirect('/SeedInv')
        else:
            return HttpResponseRedirect('/SeedInv/withdraw_inventory')

    return render(request, 'Inventory/withdraw_inventory.html',
                           {
                            'table': table,
                            'filter': f,
                            'GenotypesDownloadForm': GenotypesDownloadForm
                            })


def upload(request):
        return render(request, 'Inventory/upload.html', {})


def showfile(request):
    allfiles = GenotypeUploads.objects.all()
    table = UploadRecords(allfiles, order_by="-uploaded_at")
    RequestConfig(request).configure(table)

    return render(request, 'Inventory/records.html',
                  {
                   'allfiles': allfiles,
                   'table': table
                   })


def InventoryTable(request):
    queryset = Genotypes.objects.all()
    f = GenoFilter(request.GET, queryset=queryset)
    table = GenotypesTable(f.qs)
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('table.{}'.format(export_format))

    return render(request, 'Inventory/index.html',
                           {
                            'table': table,
                            'filter': f,
                            })


def qr_code(request):
    # Build context for rendering QR codes.
    context = dict(
        my_options=QRCodeOptions(size='t', border=6, error_correction='L'),
    )

    # Render the view.
    return render(request, 'Inventory/qr_code.html', context=context)


def qr_code_result(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

#     # Start writing the PDF here
#     p.setFont("Helvetica", 10)
#     p.drawString(110, 790, 'Range')
#     p.drawString(150, 790, 'Row')
#     p.drawString(110, 780, 'RowID')
#     p.drawString(110, 770, 'Entry')
#     p.drawString(110, 760, 'Source')
#     # End writing
#     qr_code = qr.QrCodeWidget('Range_Row_RowID_Enrty_Source')
#     bounds = qr_code.getBounds()
#     width = bounds[2] - bounds[0]
#     height = bounds[3] - bounds[1]
#     d = Drawing(50, 50, transform=[50./width,0,0,50./height,0,0])
#     d.add(qr_code)
#     renderPDF.draw(d, p, 50, 755)
# ##################################
#     p.setFont("Helvetica", 10)
#     p.drawString(110, 740, 'Range')
#     p.drawString(150, 740, 'Row')
#     p.drawString(110, 730, 'RowID')
#     p.drawString(110, 720, 'Entry')
#     p.drawString(110, 710, 'Source')

    C = 110
    for j in range(3):
        H = 790
        for i in range(15):
            p.setFont("Helvetica", 10)
            p.drawString(C, H, 'Range')
            p.drawString((C+40), H, 'Row')
            p.drawString(C, (H-10), 'RowID')
            p.drawString(C, (H-20), 'Entry')
            p.drawString(C, (H-30), 'Source')
            # End writing
            qr_code = qr.QrCodeWidget('Range_Row_RowID_Enrty_Source')
            bounds = qr_code.getBounds()
            width = bounds[2] - bounds[0]
            height = bounds[3] - bounds[1]
            d = Drawing(50, 50, transform=[50./width,0,0,50./height,0,0])
            d.add(qr_code)
            renderPDF.draw(d, p, (C-60), (H-35))
            H -= 50
        C+=175





    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

# def showfile(request):
#     f = GenoFilter(request.GET, queryset=Genotypes.objects.all())
#     allfiles = File.objects.all()

#     # lastfile = File.objects.last()
#     # filepath = lastfile.filepath
#     # filename = lastfile.name
#     # context = {'filepath': filepath,
#     #            'form': form,
#     #            'filename': filename
#     #            }

#     form = FileForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         form.save()
#         # This will clear out our form upon submission
#         form = FileForm()
#         # This will refresh the page so people don't double post
#         return HttpResponseRedirect('/records')

#     return render(request, 'Inventory/records.html',
#                   {'allfiles': allfiles, 'form': form, 'filter': f})
