from django.shortcuts import render
from django.db.models import Q
from .models import RealEstateProgram
from django.views.generic import DetailView


# Create your views here.

def home(request):
    return render(request, 'home.html')


def ProgramSearchView(request):
    query = request.GET.get('q', '')
    search_performed = bool(query)
    if search_performed:
        results = RealEstateProgram.objects.filter(Q(name__icontains=query) | Q(address__city__name__icontains=query))
    else:
        results = RealEstateProgram.objects.order_by('?')[:10]

    title = "Résultats de recherche" if search_performed else "Programmes"
    return render(request, 'program_search_results.html', {'results': results, 'query': query, 'search_performed': search_performed, 'title': title})


class ProgramDetailView(DetailView):
    model = RealEstateProgram
    template_name = 'program_detail.html'
    context_object_name = 'program'