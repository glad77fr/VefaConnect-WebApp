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
from django.http import JsonResponse
from .models import State, City
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import ProgramPhoto

def home(request):
    articles = Article.objects.all().order_by('-publication_date').prefetch_related('section_set')[:6]
    realEstatesPrograms = RealEstateProgram.objects.filter(validated=True).order_by('-date_added')[:6]

    # Initialisation d'une liste vide pour les programmes suivis par l'utilisateur
    user_programs = []

    # Vérifie si l'utilisateur est connecté
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile  # accède au profil de l'utilisateur
            user_programs = profile.followed_programs.all().order_by('-date_added')[:6]
        except UserProfile.DoesNotExist:
            pass  # le profil n'existe pas pour cet utilisateur

    for article in articles:
        article.main_image = article.section_set.filter(type="image", image_position="title").first()
    
    return render(request, 'home.html', {'articles': articles, 'realEstatesPrograms': realEstatesPrograms, 'user_programs': user_programs})


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

        # Mise à jour des querysets pour 'city' et 'states'
        form.fields['city'].queryset = City.objects.filter(id=request.POST.get('city', 0))
        form.fields['states'].queryset = State.objects.filter(id=request.POST.get('states', 0))

        if form.is_valid():
            form.save()
            messages.success(request, "Votre demande d'ajout de programme a bien été soumise, elle va être à présent validée. Vous serez notifié de sa validation.")
            return redirect('home')
            
        else:
            # Afficher les erreurs de validation
            print("Erreurs du formulaire :", form.errors)
            # Affichage des valeurs soumises pour débogage
            print("Valeurs soumises pour city:", request.POST.get('city'))  
            print("Valeurs soumises pour states:", request.POST.get('states'))
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
    articles = Article.objects.filter(category=category).order_by('-publication_date').prefetch_related('section_set')
    articles_with_title_images = []

    for article in articles:
        title_image_section = article.section_set.filter(image_position='title').first()  # Obtenez l'image de titre de l'article
        section_text = article.section_set.filter(type='text').first()
        articles_with_title_images.append((article, title_image_section, section_text))

    return render(request, 'category_articles.html', {
        'category': category,
        'articles_with_title_images': articles_with_title_images,
        'section_text': section_text,
    })

def load_states(request):
    country_id = request.GET.get('country')
    states = State.objects.filter(country_id=country_id).order_by('name')
    #print(list(states.values('id', 'name')))
    return JsonResponse(list(states.values('id', 'name')), safe=False)

def load_cities(request):
    state_id = request.GET.get('states')  # Récupération de l'ID de l'état sélectionné
    cities = City.objects.filter(state_id=state_id).order_by('name')  # Filtrage des villes par l'état sélectionné
    return JsonResponse(list(cities.values('id', 'name')), safe=False)  # Envoi des villes au format JSON

@login_required
@require_POST  # S'assure que la vue ne peut être accédée que via POST
def unfollow_program(request, program_id):
    # Récupère l'objet RealEstateProgram ou renvoie une erreur 404 si non trouvé
    program = get_object_or_404(RealEstateProgram, pk=program_id)

    # Supprime le lien entre l'utilisateur et le programme
    FollowedProgram.objects.filter(
        user_profile=request.user.userprofile, 
        real_estate_program=program  # Utilisation du champ correct
    ).delete()

    # Ajoute un message d'information à afficher à l'utilisateur
    messages.info(request, "Vous avez cessé de suivre le programme.")

    # Redirection vers la page d'accueil ou toute autre page souhaitée
    return redirect('home')

def all_photos_view(request):
    photos = ProgramPhoto.objects.all()  # Cela respectera l'ordre défini dans la classe Meta du modèle
    return render(request, 'all_photos.html', {'photos': photos})