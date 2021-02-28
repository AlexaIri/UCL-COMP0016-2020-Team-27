import django_filters

from .models import *

class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    surname = django_filters.CharFilter(lookup_expr='icontains')
    project_title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Person
        
        fields = ['name','surname','project_title', 'project_complexity', 'source_type']

        