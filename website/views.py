from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FollowedProgramForm
from django.db.models import Q
from .models import RealEstateProgram
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import RealEstateProgram, FollowedProgram
from forum.models import UserProfile
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import RealEstateProgram
from .forms import RealEstateProgramForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Article, Section,Category
from django.shortcuts import render, get_object_or_404
from .models import Article



def home(request):
    articles = Article.objects.all().prefetch_related('section_set')[:3]
    for article in articles:
        article.main_image = article.section_set.filter(type="image", image_position="title").first()
    return render(request, 'home.html', {'articles': articles})



def ProgramSearchView(request):
    query = request.GET.get('q', '')
    search_performed = bool(query)
    if search_performed:
        results = RealEstateProgram.objects.filter(Q(name__icontains=query) | Q(address__city__name__icontains=query), validated=True)
    else:
        results = RealEstateProgram.objects.filter(validated=True).order_by('?')[:10]

    title = "Résultats de recherche" if search_performed else "Programmes"
    return render(request, 'program_search_results.html', {'results': results, 'query': query, 'search_performed': search_performed, 'title': title})


class ProgramDetailView(DetailView):
    model = RealEstateProgram
    template_name = 'program_detail.html'
    context_object_name = 'program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = self.request.user.userprofile
            program_is_followed = FollowedProgram.objects.filter(user_profile=user_profile, real_estate_program=self.object).exists()
            context['program_is_followed'] = program_is_followed
        else:
            context['program_is_followed'] = False
        return context


@login_required
def follow_program_view(request, program_id):
    program = RealEstateProgram.objects.get(id=program_id)
    user_profile = request.user.userprofile
    if not FollowedProgram.objects.filter(user_profile=user_profile, real_estate_program=program).exists():
        return redirect('program_register', program_id=program.id)  # redirect to the form view
    else:
        return redirect('program_details', program_id=program.id)  # if the user already follows the program, redirect back to the program details page
    
class FollowedProgramView(FormView):
    template_name = 'program_register.html'
    form_class = FollowedProgramForm
    success_url = reverse_lazy('followed-program-confirmation')  # Définir success_url ici


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.program = RealEstateProgram.objects.get(id=self.kwargs['program_id'])
        user = self.request.user.userprofile
        kwargs.update({'program': self.program, 'user': user})
        return kwargs

    def form_valid(self, form):
        form.save()
        # Here you can handle your form after it has been validated
        # For example, you can save the instance of your FollowedProgramForm

        # Then, render your template with the program name in the context
        # Store the program ID in the session
        self.request.session['program_id'] = self.program.id
        return super().form_valid(form) 

class FollowedProgramConfirmationView(TemplateView):
    template_name = 'followedprogram_confirmation.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the program ID from the session
        program_id = self.request.session.get('program_id')
            
        # If a program ID was stored in the session, get the corresponding program
        if program_id is not None:
            program = RealEstateProgram.objects.get(id=program_id)
            context['program'] = program
    
        return context
    
def create_program(request):
    if request.method == "POST":
        form = RealEstateProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('program_search')
    else:
        form = RealEstateProgramForm()
    return render(request, 'create_program.html', {'form': form})  

@login_required
def my_programs(request):
    user_profile = UserProfile.objects.get(user=request.user)
    followed_programs = FollowedProgram.objects.filter(user_profile=user_profile)
    return render(request, 'my_programs.html', {'followed_programs': followed_programs})

class ProgrammesSuivisView(LoginRequiredMixin, generic.ListView):
    model = RealEstateProgram
    template_name = "programmes_suivis.html"
    
    def get_queryset(self):
        user_profile = self.request.user.userprofile  # Obtention de l'objet UserProfile associé à cet utilisateur
        return user_profile.followed_programs.all()
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = Section.objects.filter(article=self.object)
        return context

def category_articles(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    articles = Article.objects.filter(category=category)
    
    return render(request, 'category_articles.html', {
        'category': category,
        'articles': articles,
    })


