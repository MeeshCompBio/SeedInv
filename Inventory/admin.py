from django.contrib import admin
from Inventory.models import Question, Genotypes


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']


class Genotype(admin.ModelAdmin):
    fields = ['genotype',
              'parent_f_row',
              'parent_m_row',
              'parent_f_geno',
              'parent_m_geno',
              'seed_count',
              'actual_count',
              'experiment'
              'comments',
              ]


admin.site.register(Question)
admin.site.register(Genotypes)
