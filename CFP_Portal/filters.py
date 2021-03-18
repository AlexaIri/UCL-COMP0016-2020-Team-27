import django_filters

from .models import *

class ProjectFilter(django_filters.FilterSet):
    
    name = django_filters.CharFilter(lookup_expr='startswith')
    surname = django_filters.CharFilter(lookup_expr='startswith')
    project_title = django_filters.CharFilter(lookup_expr='startswith')
    department = django_filters.CharFilter(lookup_expr='startswith')
    organisation = django_filters.CharFilter(lookup_expr='startswith')
    expertiseskills= django_filters.CharFilter(lookup_expr='startswith')
    tags__name = django_filters.CharFilter(lookup_expr='startswith')
    challenge = django_filters.CharFilter(lookup_expr='startswith')
    class Meta:
        model = Person
        
        fields = ['name','surname','project_title', 'project_complexity', 'source_type', 'status','department','organisation', 'expertiseskills','id','tags__name','challenge','NICEtier']

        