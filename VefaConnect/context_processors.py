# articles/context_processors.py

from website.models import Category

def categories(request):
    return {
        'categories': Category.objects.all()
    }
