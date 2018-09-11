from django.shortcuts import render
from .models import Question, Genotypes, GenotypeUploads
from django.utils import timezone
from .forms import QuestionForm, GenotypesUploadForm
from django.shortcuts import redirect
from .tables import GenotypesTable, UploadRecords
from django_tables2.config import RequestConfig
from django.http import HttpResponseRedirect
from .filters import GenoFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableView
from django_tables2.export.export import TableExport
from .upload_checks import additions_upload
from django.conf import settings


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


def gtable(request):
    queryset = Genotypes.objects.all()
    f = GenoFilter(request.GET, queryset=queryset)
    table = GenotypesTable(f.qs)
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
        form = GenotypesUploadForm(request.POST or None,request.FILES or None,
                                   initial={'upload_pass': 'logs/'+log_files[0],
                                            'upload_fail': 'logs/'+log_files[1],
                                            })
        form = form.save(commit=False)
        form.issues = log_files[2]
        form.save()

        # This will clear out our form upon submission
        form = GenotypesUploadForm()
        # This will refresh the page so people don't double post
        return HttpResponseRedirect('/records')

    return render(request, 'Inventory/add_inventory.html',
                           {
                            'table': table,
                            'filter': f,
                            'GenotypesUploadForm': GenotypesUploadForm
                            })


def upload(request):
        return render(request, 'Inventory/upload.html', {})


def showfile(request):
    allfiles = GenotypeUploads.objects.all()
    table = UploadRecords(allfiles)
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
