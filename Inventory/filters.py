import django_filters

from Inventory.models import Genotypes, GenotypeUploads, GenotypeDownloads


class GenoFilter(django_filters.FilterSet):

    class Meta:
        model = Genotypes
        fields = {'parent_f_row': ['icontains'],
                  'parent_m_row': ['icontains'],
                  'parent_f_geno': ['icontains'],
                  'parent_m_geno': ['icontains'],
                  'genotype': ['icontains'],
                  'seed_count': ['lt', 'gt']}


class GenoUploadsFilter(django_filters.FilterSet):

    class Meta:
        model = GenotypeUploads
        fields = {'description': ['icontains']}


class GenoDownloadsFilter(django_filters.FilterSet):

    class Meta:
        model = GenotypeDownloads
        fields = {'description': ['icontains']}