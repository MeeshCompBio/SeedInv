from django.contrib import admin
from Inventory.models import Genotypes, GenotypeUploads, GenotypeDownloads


class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']


class GenotypeAdmin(admin.ModelAdmin):
    list_display = ('genotype',
                    'parent_f_row',
                    'parent_m_row',
                    'parent_f_geno',
                    'parent_m_geno',
                    )


class GenotypeUploadsAdmin(admin.ModelAdmin):
    list_display = ('description',
                    'document',
                    'uploaded_at',
                    'issues',
                    )


class GenotypeDownloadsAdmin(admin.ModelAdmin):
    list_display = ('description',
                    'document',
                    'uploaded_at',
                    'issues',
                    )


admin.site.register(GenotypeUploads, GenotypeUploadsAdmin)
admin.site.register(GenotypeDownloads, GenotypeDownloadsAdmin)
admin.site.register(Genotypes, GenotypeAdmin)
