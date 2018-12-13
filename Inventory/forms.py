from django import forms
from django.conf import settings
from .models import Question, Genotypes, File, GenotypeUploads, GenotypeDownloads


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text',)


class GenotypesForm(forms.ModelForm):

        model = Genotypes
        fields = ('parent_f_row',
                  'parent_m_row',
                  'parent_f_geno',
                  'parent_m_geno',
                  'genotype',
                  'seed_count',
                  'actual_count',
                  'experiment',
                  'comments',
                  )


class GenotypesUploadForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Insert a decription of the file to be uploaded'
        }
        ))

    class Meta:
        model = GenotypeUploads
        fields = ('description',
                  'document',
                  'upload_pass',
                  'upload_fail',
                  'issues',
                  )


class GenotypesDownloadForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Insert a decription of the file to be downloaded'
        }
        ))

    class Meta:
        model = GenotypeDownloads
        fields = ('description',
                  'document',
                  'download_pass',
                  'download_fail',
                  'issues',
                  )


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ["name", "filepath"]
