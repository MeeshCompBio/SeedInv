from django.db import models
from django.utils import timezone
import datetime
# from django.core.validators import validate_slug, validate_email
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Create your models here


def validate_int(value):
    if type(value) == int or type(value) == float:
        raise ValidationError("Please use a valid integer")


# RegexValidator(
#            regex='^WOW',
#            message='Questions needs an underscore',
#            code='invalid_username')


class Question(models.Model):
    question_text = models.CharField(max_length=200,
                                     validators=[RegexValidator(
                                                   regex='^WOW',
                                                   message='Needs to start with WOW',
                                                   code='invalid')])
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


# Genotype database model
class Genotypes(models.Model):
    """list of current genotypes"""
    parent_f_row = models.CharField(max_length=200,
                                    validators=[],)
    parent_m_row = models.CharField(max_length=200,
                                    validators=[],)
    parent_f_geno = models.CharField(max_length=200,
                                     validators=[],)
    parent_m_geno = models.CharField(max_length=200,
                                     validators=[],)
    genotype = models.CharField(max_length=200,
                                validators=[],)
    seed_count = models.IntegerField(validators=[], default=0)
    actual_count = models.BooleanField(default=False)
    comments = models.CharField(max_length=200,
                                validators=[],
                                blank=True,)
    tissue_comments = models.CharField(max_length=200,
                                       validators=[],
                                       blank=True,)

    def __str__(self):
        return self.genotype

    class Meta:
        verbose_name_plural = "Genotypes"


class GenotypeUploads(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='additions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    name = models.CharField(max_length=500)
    filepath = models.FileField(upload_to='file/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.filepath)
