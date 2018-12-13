import django_tables2 as tables
from .models import Genotypes, GenotypeUploads, GenotypeDownloads


class GenotypesTable(tables.Table):
    export_formats = ['tsv']

    class Meta:
        model = Genotypes
        template_name = 'django_tables2/bootstrap.html'


class UploadRecords(tables.Table):
    class Meta:
        model = GenotypeUploads
        template_name = 'django_tables2/bootstrap.html'


class DownloadRecords(tables.Table):
    class Meta:
        model = GenotypeDownloads
        template_name = 'django_tables2/bootstrap.html'
