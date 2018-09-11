from django import forms
from django.conf import settings
from .models import Question, Genotypes, File, GenotypeUploads


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text',)


class GenotypesForm(forms.ModelForm):

    class Meta:
        model = Genotypes
        fields = ['genotype',
                  'parent_f_row',
                  'parent_m_row',
                  'parent_f_geno',
                  'parent_m_geno',
                  'seed_count',
                  'actual_count',
                  'experiment',
                  'comments',
                  ]


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
                  'upload_fail', )


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ["name", "filepath"]
