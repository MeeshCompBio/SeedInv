from django.shortcuts import render
from .models import Question, Genotypes, GenotypeUploads
from django.utils import timezone
from .forms import QuestionForm, FileForm, GenotypesUploadForm
from django.shortcuts import render
from django.shortcuts import redirect
from .tables import GenotypesTable, UploadRecords
from django_tables2.config import RequestConfig
from django.http import HttpResponseRedirect
from django.conf import settings
from .filters import GenoFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableView


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
    RequestConfig(request).configure(table)

    form = GenotypesUploadForm(request.POST or None, request.FILES or None)
    if form.is_valid():

        # Grab the file and open it
        data = request.FILES.get('document', None)
        # Go through each line of the file
        for line in data:
            line = line.decode().strip()
            # check to see if there is header line or skip
            if line.startswith("parent"):
                continue
            else:
                fields = line.split(",")
                print(fields)
                if fields[6] == "TRUE":
                    fields[6] = True
                elif fields[6] == "FALSE":
                    fields[6] = False
                NewGeno = Genotypes(parent_f_row=fields[0],
                                    parent_m_row=fields[1],
                                    parent_f_geno=fields[2],
                                    parent_m_geno=fields[3],
                                    genotype=fields[4],
                                    seed_count=fields[5],
                                    actual_count=fields[6],
                                    comments=fields[7],
                                    tissue_comments=fields[8],
                                    )
                NewGeno.save()
        # print(data)
        # print(data)
        # for line in data:
        #     print(line)

        form.save()
        # print(form)
        # media_url = settings.MEDIA_URL
        # path_to_file = media_url + "/" + GenotypesUploadForm.document
        # file = open(path_to_file, "r")
        # for line in file:
        #     print(line)
        # This will clear out our form upon submission
        form = GenotypesUploadForm()
        # This will refresh the page so people don't double post
        return HttpResponseRedirect('/add_inventory')

    return render(request, 'Inventory/add_inventory.html', {'table': table,
                                                    'filter': f,
                                                   'GenotypesUploadForm': GenotypesUploadForm})


def upload(request):
        return render(request, 'Inventory/upload.html', {})


def showfile(request):
    allfiles = GenotypeUploads.objects.all()
    table = UploadRecords(allfiles)
    RequestConfig(request).configure(table)
    return render(request, 'Inventory/records.html',
                  {'allfiles': allfiles, 'table': table})


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
